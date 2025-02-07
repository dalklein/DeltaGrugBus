#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pprint, time, sys, serial, socket, traceback, struct, datetime, logging, math, traceback, collections

# Modbus stuff
import pymodbus, asyncio, signal, uvloop
from pathlib import Path
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock
from pymodbus.server import StartAsyncSerialServer
# from pymodbus.transaction import ModbusRtuFramer  # removed in pymodbus 3.7.3
from pymodbus.exceptions import ModbusException

# import aiohttp
# from gmqtt import Client as MQTTClient

# Device wrappers
import grugbus
from misc import *
from grugbus.devices import Acrel_AGF_AE_D
import config

# pymodbus.pymodbus_apply_logging_config( logging.DEBUG )
logging.basicConfig( encoding='utf-8', 
                     level=logging.INFO,
                     format='[%(asctime)s] %(levelname)s:%(message)s',
                     handlers=[logging.FileHandler(filename=Path(__file__).stem+'.log'), 
                            logging.StreamHandler(stream=sys.stdout)])
log = logging.getLogger(__name__)

# set max reconnect wait time for Fronius
# Remove or modify this line
# pymodbus.constants.Defaults.ReconnectDelayMax = 60000   # in milliseconds

# Instead, set the reconnect delay directly in the client configuration if applicable
#client = AsyncModbusTcpClient(..., reconnect_delay=60)  # Example for TCP client

# After logging setup
log.info("Logging initialized")
logging.getLogger().handlers[0].flush()

"""

    EXAMPLE MITM SCRIPT

    This simplified script creates a fake Acrel ACR10R smartmeter as modbus server.
    It queries data from a real Acrel ACR10R meter and copies it to the fake one.
    See config.py for serial port names and other options.


#### WARNING ####
This file is both the example code and the manual.
==================================================

RS485 ports
- Master:       Solis inverters COM port + Meter attached to inverter
- Slave:        Inverter 1 fake meter
- Slave:        Inverter 2 fake meter
- Master:       Main smartmeter (gets its own interface cause it has to be fast, for power routing)

How to prevent USB serial ports from changing names: use /dev/serial/by-id/ names, not /dev/ttywhoknows

#####   Sign of power
When power can flow one way, always positive (example: PV power)
When Power can flow both ways, positive sign is always consumed power
  If something_power is positive, that something is drawing power or current
  If something_power is negative, that something is producing power
This is sometimes not intuitive, but at least it's the same convention everywhere!
    Inverter grid port power 
        positive if it is consuming power (to charge batteries for example)
        negative means it's producing
    Battery power is positive if it is charging
    Backup port power is power consumed by backup loads, always positive
    Grid side meter is positive if the house is consuming power
    etc
"""

#
#   Housekeeping for async multitasking:
#   If one thread coroutine abort(), fire STOP event to allow program exit
#   and set STILL_ALIVE to False to stop all other threads.
#
STILL_ALIVE = True
STOP = asyncio.Event()
def abort():
    STOP.set()
    global STILL_ALIVE
    STILL_ALIVE = False

# Helper to abort program when the coroutine passed as parameter exits
async def abort_on_exit( awaitable ):
    await awaitable
    log.info("*** Exited: %s", awaitable)
    return abort()

###########################################################################################
#
#       Fake smartmeter
#       Modbus server emulating a fake smartmeter to feed data to inverter via meter port
#
#       https://pymodbus.readthedocs.io/en/v1.3.2/examples/asynchronous-server.html
#
###########################################################################################
#
#   Modbus server is a slave (client is master)
#   pymodbus requires ModbusSlaveContext which contains data to serve
#   This ModbusSlaveContext has a hook to generate values on the fly when requested
#
class HookModbusSlaveContext(ModbusSlaveContext):
    def getValues(self, fc_as_hex, address, count=1):
        if self._on_getValues( fc_as_hex, address, count, self ):
            return super().getValues( fc_as_hex, address, count )


###########################################################################################
#   
#   Fake meter emulator
#
#   Base class is grugbus.LocalServer which extends pymodbus server class to allow
#   registers to be accessed by name with full type conversion, instead of just
#   address and raw data.
#   
###########################################################################################
#   Delta ExTLUS w/ Acrel AGF-AE-D meter & LG battery on RGM rs485 bus
#        inverter reads meter id2 func 3, addr 40018-40022 for self consumption power control
#       inverter also requests id3 with different registers for AC solar power data. 
#    Caution: If the AC coupled option is enabled and 2nd SysProductionMeterIDSet is done, 
#       the inverter will set the meter to use id3, even though you may only have the one
#       meter installed at grid location, so that hoses the normal control.
#
#   GridMeter id2 is queried every second maybe 10Hz, not sure Acrel AGF-AE-D meter is that fast

class FakeMeter1( grugbus.LocalServer ):
    #
    #   port    serial port name
    #   key     machine readable name for logging, like "fake_meter_1", 
    #   name    human readable name like "Fake SDM120 for Inverter 1"
    #
    def __init__( self, port, key, name, modbus_address=2 ):
        self.port = port

        # Create slave context for our local server
        slave_ctxs = {}
        # Create datastore corresponding to registers available in meter
        data_store = ModbusSequentialDataBlock( 40000, [0]*121 )   
        slave_ctx = HookModbusSlaveContext(
            di = ModbusSequentialDataBlock( 0, [0] ), # Discrete Inputs  (not used, so just one zero register)
            co = ModbusSequentialDataBlock( 0, [0] ), # Coils            (not used, so just one zero register)
            hr = data_store, # Holding Registers, we will write fake values to this datastore
            ir = data_store  # Input Registers (use the same datastore, so we don't have to check the opcode)
        )
        slave_ctx._on_getValues = self._on_getValues # hook to update datastore when we get a request
        slave_ctx.modbus_address = modbus_address
        slave_ctxs[modbus_address] = slave_ctx

        # Create Server context and assign previously created datastore to smartmeter_modbus_address
        self.server_ctx = ModbusServerContext( slave_ctxs, single=False )
        super().__init__( slave_ctxs[modbus_address],   # Use modbus_address here
              modbus_address, key, name, 
            Acrel_AGF_AE_D.MakeRegisters() ) # build our registers
        self.last_request_time = time.time()    # for stats
        self.data_request_timestamp = 0
        self.power_offset = 0
        self.power_elimit = 2000
        self.export_mode = 0

    # This is called when the inverter sends a request to this server
    def _on_getValues( self, fc_as_hex, address, count, ctx ):

        #   The main meter is read in another coroutine, so data is already available and up to date
        #   but we still have to check if the meter is actually working
        #
        #   TODO: get data from your data source and check if it is online
        meter = mgr.meter
        if not meter.is_online:
            log.warning( "FakeSmartmeter cannot reply to client: real smartmeter offline" )
            # return value is False so pymodbus server will abort the request, which the inverter
            # correctly interprets as the meter being offline
            return False

        # TODO: fill this with your data
        # Delta inverter requests 40018-40022, real power registers, for control loop, 
        #   Could get other data, but don't have a need, yet.
        try:    # Fill our registers with up-to-date data
            self.total_real_power                .value = meter.total_real_power              .value
            self.watts_phase_a                .value = meter.watts_phase_a              .value
            self.watts_phase_b                .value = meter.watts_phase_b              .value
            self.watts_phase_c                .value = meter.watts_phase_c              .value
            self.real_power_scale_factor         .value = meter.real_power_scale_factor       .value

        except TypeError:   # if one of the registers was None because it wasn't read yet
            log.warning( "FakeSmartmeter cannot reply to client: real smartmeter missing fields" )
            return

        self.write_regs_to_context() # write data to modbus server context, so it can be served to inverter

        # logging
        # t = time.time()
        # # s = "query _on_getValues fc %3d addr %5d count %3d dt %f" % (fc_as_hex, address, count, t-self.last_request_time)
        # # log.debug(s); 
        # self.last_request_time = t
        # if meter.data_timestamp:    # how fresh is this data?
        #     mqtt.publish( "pv/solis1/fakemeter/", {
        #         "lag": round( t-meter.data_timestamp, 2 ), # lag between getting data from the real meter and forwarding it to the inverter
        #         self.active_power.key: self.active_power.format_value(), # log what we sent to the inverter
        #         "offset": int(self.power_offset)
        #         })
        return True

    # This function starts and runs the modbus server, and never returns as long as the server is running.
    # Before starting it, communication with the real meter should be initiated, registers read,
    # dummy registers in this object populated with correct values, and write_regs_to_context() called
    # to setup the server context, so that we serve correct value to the inverter when it makes a request.
    async def start_server( self ):
        self.server = await StartAsyncSerialServer( context=self.server_ctx, 
            #framer          = ModbusRtuFramer,
            ignore_missing_slaves = True,
            auto_reconnect = True,
            port            = self.port,
            timeout         = 0.3,      # parameters used by inverter on meter port
            baudrate        = 9600,
            bytesize        = 8,
            parity          = "N",
            stopbits        = 1,
            strict = False,
            )
        await self.server.start()

########################################################################################
#
#       Main meter, grid side of Delta inverter, meters total power for solar+home
#   (in this case, 'grid' is the AC1 port of SMA SI6048US inverters, behind which the
#    Delta battery inverter is AC coupled and set for self-consumption, controlling
#    to keep 'grid' powerflow minimized close to zero.)
#
########################################################################################
class GridMeter( grugbus.SlaveDevice ):
    def __init__( self ):
        log.info("Initializing GridMeter...")
        super().__init__( 
            AsyncModbusSerialClient(
                port            = config.RGM_PORT_METER,
                timeout         = 0.3,
                retries         = config.MODBUS_RETRIES_SOLIS,
                baudrate        = 9600,
                bytesize        = 8,
                parity          = "N",
                stopbits        = 1
            ),
            1,          # Modbus address
            "meter", "Acrel_AGFAED", 
            Acrel_AGF_AE_D.MakeRegisters() )
        self.is_online = False
        log.info("GridMeter initialized")

    async def read_coroutine( self ):
        log.info("Starting GridMeter read coroutine...")
        regs_to_read = (
            self.total_real_power         ,    
            self.watts_phase_a            ,  
            self.watts_phase_b            ,   
            self.watts_phase_c            ,   
            self.real_power_scale_factor         
        )

        tick = Metronome(config.POLL_PERIOD_METER)
        while STILL_ALIVE:
            try:
                if not self.modbus.connected:
                    log.info("Attempting modbus connection...")
                    await self.modbus.connect()
                    log.info("Modbus connected successfully")

                try:
                    regs = await self.read_regs( regs_to_read )
                    if not self.is_online:
                        log.info("GridMeter is now online")
                    self.is_online = True
                except asyncio.exceptions.TimeoutError:
                    if self.is_online:
                        log.warning("GridMeter went offline - timeout")
                    self.is_online = False
                except Exception as e:
                    if self.is_online:
                        log.error(f"GridMeter went offline - {str(e)}")
                    self.is_online = False
                    raise
            except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
                log.info("GridMeter read coroutine received shutdown signal")
                return abort()
            except Exception as e:
                log.error(f"Error in GridMeter read loop: {str(e)}")
                s = traceback.format_exc()
                log.error(s)
                await asyncio.sleep(0.5)
            await tick.wait()

########################################################################################
#
#       Put it all together
#
########################################################################################
class DeltaManager():
    def __init__( self ):
        self.total_real_power = 0
        self.watts_phase_a            = 0 
        self.watts_phase_b            = 0   
        self.watts_phase_c            = 0   
        self.real_power_scale_factor  = 0   # Acrel AGF-AE-D reg 40022. If 0, coeff=1. If 1, coeff=10.
        self.is_online = False
        log.info("DeltaManager initialized")

    async def initialize_meters(self):
        log.info("Initializing meters...")
        self.meter = GridMeter()
        self.fake_meter = FakeMeter1( config.RGM_PORT_FAKE_METER1, "fake_meter_1", "Fake Acrel AGF-AE-D for Inv1" )
        log.info("Meters initialized successfully")

    ########################################################################################
    #   Start async processes
    ########################################################################################

    def start( self ):
        log.info("Starting DeltaManager...")
        if sys.version_info >= (3, 11):
            log.info("Using Python 3.11+ runner with uvloop")
            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(self.astart())
        else:
            log.info("Using legacy asyncio.run with uvloop")
            uvloop.install()
            asyncio.run(self.astart())

    async def astart( self ):
        log.info("Setting up async tasks...")
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT,  abort)
        loop.add_signal_handler(signal.SIGTERM, abort)

        await self.initialize_meters()

        log.info("Starting server and monitoring tasks...")
        asyncio.create_task( self.fake_meter.start_server() )
        asyncio.create_task( abort_on_exit( self.meter.read_coroutine() ))
        asyncio.create_task( self.display_coroutine() )
        log.info("All tasks started, waiting for STOP event")

        await STOP.wait()
        log.info("STOP event received, shutting down...")

    ########################################################################################
    #   Local display
    ########################################################################################

    async def display_coroutine( self ):
        while STILL_ALIVE:
            try:
                for reg in (
                    self.total_real_power         ,    
                    self.watts_phase_a            ,  
                    self.watts_phase_b            ,   
                    self.watts_phase_c            ,   
                    self.real_power_scale_factor  ,                     
                    ):
                    # try: 
                    if reg.value is not None:  # Now this should work
                        print(f"{reg.key}: {reg.value}")
                    # except:
                    #     print(f"Register value: {reg}")
                    if isinstance( reg, str ):
                        print(reg)
                    else:
                        try:
                            if reg.value != None:
                                print( "%40s %10s %10s" % (reg.key, reg.device.key, reg.format_value() ) )
                        except:
                            print(reg)
            except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
                return abort()
            except:
                log.error(traceback.format_exc())


if __name__ == "__main__":
    log.info("Starting main program")
    mgr = DeltaManager()
    mgr.start()
    log.info("Program ended")

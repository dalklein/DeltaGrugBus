# DeltaGrugBus
Adaptation of GrugBus for Delta Ex-TL-US battery inverter, Acrel AGF-AE-D meter, LG Resu Prime battery communication and system control over rs485 Modbus RTU. 

Grug is a small, striped creature with feet, a nose, and big eyes. He is fascinated by the world around him and solves problems creatively. As such, he strives to control and optimize the collection of solar and battery equipment within his reach. GrugBus is Grug's brain.

Please refer to the very impressive original, [/peufeu2/GrugBus](https://github.com/peufeu2/GrugBus), which is for managing a grid-tied system with Solis battery inverter, Fronius AC coupled PV inverter, and several power meters. 

DeltaGrugBus will use the /grugbus library, likely no changes. Due to differences in my PV system and all different components, I will use other parts from GrugBus only as I figure them out bit by bit. More about my system and recent additions: https://diysolarforum.com/threads/growatt-min-tl-xh-us-or-delta-e6-tl-us-ac-coupled-behind-sma-si6048us.95069/

Goals:  
-similar to GrugBus pv_controller.py, performing MITM between the meter and inverter, to enable some control of the inverter. Initially only a fixed offset watts to the 'grid' power, later take input from node-red or mqtt.

-record and reverse engineer LG Resu10H Prime rs485 communications.

-reverse engineer the Delta inverter outside communication port, I'm not even sure it is active. Tried a number of Delta inverter projects based on the previous generation inverters, but can't get a response.




Setup notes required since Grug's memory is better than mine:
  git repo is cloned to /home/pi/DeltaGrugBus, 
  sshfs the /home/pi folder to /IOT_RPi folder on PC
  from cursor on PC, access the folder from /IOT_RPi/DeltaGrug, open terminal and ssh to pi
  

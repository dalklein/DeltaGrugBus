#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#   Register data from datasheet PDF
#   Extracted from Acrel_AGF_AE_D.csv
#

from grugbus.registers import *

def MakeRegisters():
    return (
    RegU16( (3, 16),     1, 1, 'rwr_id_baud'                        , None, None  , 'int'  , 0, 'ID_baud'                        , ''),
    RegU16( (3, 16), 40108, 1, 'rwr_allows_clearing_of_energy_flags', None, None  , 'int'  , 0, 'Allows clearing of energy flags', ''),
    RegU16( (3, 16), 40109, 1, 'rwr_clear_all_power'                , None, None  , 'int'  , 0, 'Clear all power'                , ''),
    RegU16(          4, 40000, 1, 'id_sunspec'                         , None, None  , 'int'  , 0, 'ID_sunspec'                     , ''),
    RegU16(          4, 40001, 1, 'length_sunspec'                     , None, None  , 'int'  , 0, 'Length_sunspec'                 , ''),
    RegS16(          4, 40002, 1, 'amps'                               ,    1, 'A'   , 'float', 2, 'Amps'                           , ''),
    RegS16(          4, 40003, 1, 'amps_phase_a'                       ,    1, 'A'   , 'float', 2, 'Amps Phase A'                   , ''),
    RegS16(          4, 40004, 1, 'amps_phase_b'                       ,    1, 'A'   , 'float', 2, 'Amps Phase B'                   , ''),
    RegS16(          4, 40005, 1, 'amps_phase_c'                       ,    1, 'A'   , 'float', 2, 'Amps Phase C'                   , ''),
    RegS16(          4, 40006, 1, 'current_scale_factor'               , None, None  , 'int'  , 0, 'Current scale factor'           , ''),
    RegU16(          4, 40007, 1, 'voltage_ln'                         ,    1, 'V'   , 'float', 1, 'Voltage LN'                     , ''),
    RegU16(          4, 40008, 1, 'phase_voltage_an'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage AN'               , ''),
    RegU16(          4, 40009, 1, 'phase_voltage_bn'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage BN'               , ''),
    RegU16(          4, 40010, 1, 'phase_voltage_cn'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage CN'               , ''),
    RegU16(          4, 40011, 1, 'voltage_ll'                         ,    1, 'V'   , 'float', 1, 'Voltage LL'                     , ''),
    RegU16(          4, 40012, 1, 'phase_voltage_ab'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage AB'               , ''),
    RegU16(          4, 40013, 1, 'phase_voltage_bc'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage BC'               , ''),
    RegU16(          4, 40014, 1, 'phase_voltage_ca'                   ,    1, 'V'   , 'float', 1, 'Phase Voltage CA'               , ''),
    RegS16(          4, 40015, 1, 'voltage_scale_factor'               , None, None  , 'int'  , 0, 'Voltage scale factor'           , ''),
    RegU16(          4, 40016, 1, 'frequency'                          ,    1, 'Hz'  , 'float', 2, 'Frequency'                      , ''),
    RegS16(          4, 40017, 1, 'frequency_scale_factor'             , None, None  , 'int'  , 0, 'Frequency scale factor'         , ''),
    RegU16(          3, 40018, 1, 'total_real_power'                   ,    1, 'W'   , 'float', 1, 'Total Real Power'               , ''),
    RegU16(          3, 40019, 1, 'watts_phase_a'                      ,    1, 'W'   , 'float', 1, 'Watts phase A'                  , ''),
    RegU16(          3, 40020, 1, 'watts_phase_b'                      ,    1, 'W'   , 'float', 1, 'Watts phase B'                  , ''),
    RegU16(          3, 40021, 1, 'watts_phase_c'                      ,    1, 'W'   , 'float', 1, 'Watts phase C'                  , ''),
    RegS16(          3, 40022, 1, 'real_power_scale_factor'            , None, None  , 'int'  , 0, 'Real Power Scale Factor'        , ''),
    RegU16(          4, 40023, 1, 'va'                                 ,    1, 'VA'  , 'float', 1, 'VA'                             , ''),
    RegU16(          4, 40024, 1, 'va_phase_a'                         ,    1, 'VA'  , 'float', 1, 'VA phase A'                     , ''),
    RegU16(          4, 40025, 1, 'va_phase_b'                         ,    1, 'VA'  , 'float', 1, 'VA phase B'                     , ''),
    RegU16(          4, 40026, 1, 'va_phase_c'                         ,    1, 'VA'  , 'float', 1, 'VA phase C'                     , ''),
    RegS16(          4, 40027, 1, 'apparent_power_scale_factor'        , None, None  , 'int'  , 0, 'Apparent Power scale factor'    , ''),
    RegU16(          4, 40028, 1, 'var'                                ,    1, 'VAR' , 'float', 1, 'VAR'                            , ''),
    RegU16(          4, 40029, 1, 'var_phase_a'                        ,    1, 'VAR' , 'float', 1, 'VAR phase A'                    , ''),
    RegU16(          4, 40030, 1, 'var_phase_b'                        ,    1, 'VAR' , 'float', 1, 'VAR phase B'                    , ''),
    RegU16(          4, 40031, 1, 'var_phase_c'                        ,    1, 'VAR' , 'float', 1, 'VAR phase C'                    , ''),
    RegS16(          4, 40032, 1, 'var_sf'                             , None, None  , 'int'  , 0, 'VAR_SF'                         , ''),
    RegU16(          4, 40033, 1, 'pf'                                 ,    1, 'Pct' , 'float', 2, 'PF'                             , ''),
    RegU16(          4, 40034, 1, 'pf_phase_a'                         ,    1, 'Pct' , 'float', 2, 'PF phase A'                     , ''),
    RegU16(          4, 40035, 1, 'pf_phase_b'                         ,    1, 'Pct' , 'float', 2, 'PF phase B'                     , ''),
    RegU16(          4, 40036, 1, 'pf_phase_c'                         ,    1, 'Pct' , 'float', 2, 'PF phase C'                     , ''),
    RegS16(          4, 40037, 1, 'power_factor_scale_factor'          , None, None  , 'int'  , 0, 'Power Factor scale factor'      , ''),
    RegS32(          4, 40038, 1, 'totwhexp'                           ,    1, 'Wh'  , 'float', 1, 'TotWhExp'                       , ''),
    RegS32(          4, 40040, 1, 'totwhexppha'                        ,    1, 'Wh'  , 'float', 1, 'TotWhExpPhA'                    , ''),
    RegS32(          4, 40042, 1, 'totwhexpphb'                        ,    1, 'Wh'  , 'float', 1, 'TotWhExpPhB'                    , ''),
    RegS32(          4, 40044, 1, 'totwhexpphc'                        ,    1, 'Wh'  , 'float', 1, 'TotWhExpPhC'                    , ''),
    RegS32(          4, 40046, 1, 'totwhimp'                           ,    1, 'Wh'  , 'float', 1, 'TotWhImp'                       , ''),
    RegS32(          4, 40048, 1, 'totwhimppha'                        ,    1, 'Wh'  , 'float', 1, 'TotWhImpPhA'                    , ''),
    RegS32(          4, 40050, 1, 'totwhimpphb'                        ,    1, 'Wh'  , 'float', 1, 'TotWhImpPhB'                    , ''),
    RegS32(          4, 40052, 1, 'totwhimpphc'                        ,    1, 'Wh'  , 'float', 1, 'TotWhImpPhC'                    , ''),
    RegS16(          4, 40054, 1, 'real_energy_scale_factor'           , None, None  , 'int'  , 0, 'Real Energy scale factor'       , ''),
    RegS32(          4, 40055, 1, 'totvahexp'                          ,    1, 'Vah' , 'float', 1, 'TotVAhExp'                      , ''),
    RegS32(          4, 40057, 1, 'totvahexppha'                       ,    1, 'Vah' , 'float', 1, 'TotVAhExpPhA'                   , ''),
    RegS32(          4, 40059, 1, 'totvahexpphb'                       ,    1, 'Vah' , 'float', 1, 'TotVAhExpPhB'                   , ''),
    RegS32(          4, 40061, 1, 'totvahexpphc'                       ,    1, 'Vah' , 'float', 1, 'TotVAhExpPhC'                   , ''),
    RegS32(          4, 40063, 1, 'totvahimp'                          ,    1, 'Vah' , 'float', 1, 'TotVAhImp'                      , ''),
    RegS32(          4, 40065, 1, 'totvahimppha'                       ,    1, 'Vah' , 'float', 1, 'TotVAhImpPhA'                   , ''),
    RegS32(          4, 40067, 1, 'totvahimpphb'                       ,    1, 'Vah' , 'float', 1, 'TotVAhImpPhB'                   , ''),
    RegS32(          4, 40069, 1, 'totvahimpphc'                       ,    1, 'Vah' , 'float', 1, 'TotVAhImpPhC'                   , ''),
    RegS16(          4, 40071, 1, 'apparent_energy_scale_factor'       , None, None  , 'int'  , 0, 'Apparent Energy scale factor'   , ''),
    RegS32(          4, 40072, 1, 'totvarhimpq1'                       ,    1, 'varh', 'float', 1, 'TotVArhImpQ1'                   , ''),
    RegS32(          4, 40074, 1, 'totvarhimpq1pha'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ1PhA'                , ''),
    RegS32(          4, 40076, 1, 'totvarhimpq1phb'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ1PhB'                , ''),
    RegS32(          4, 40078, 1, 'totvarhimpq1phc'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ1PhC'                , ''),
    RegS32(          4, 40080, 1, 'totvarhimpq2'                       ,    1, 'varh', 'float', 1, 'TotVArhImpQ2'                   , ''),
    RegS32(          4, 40082, 1, 'totvarhimpq2pha'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ2PhA'                , ''),
    RegS32(          4, 40084, 1, 'totvarhimpq2phb'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ2PhB'                , ''),
    RegS32(          4, 40086, 1, 'totvarhimpq2phc'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ2PhC'                , ''),
    RegS32(          4, 40088, 1, 'totvarhimpq3'                       ,    1, 'varh', 'float', 1, 'TotVArhImpQ3'                   , ''),
    RegS32(          4, 40090, 1, 'totvarhimpq3pha'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ3PhA'                , ''),
    RegS32(          4, 40092, 1, 'totvarhimpq3phb'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ3PhB'                , ''),
    RegS32(          4, 40094, 1, 'totvarhimpq3phc'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ3PhC'                , ''),
    RegS32(          4, 40096, 1, 'totvarhimpq4'                       ,    1, 'varh', 'float', 1, 'TotVArhImpQ4'                   , ''),
    RegS32(          4, 40098, 1, 'totvarhimpq4pha'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ4PhA'                , ''),
    RegS32(          4, 40100, 1, 'totvarhimpq4phb'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ4PhB'                , ''),
    RegS32(          4, 40102, 1, 'totvarhimpq4phc'                    ,    1, 'varh', 'float', 1, 'TotVArhImpQ4PhC'                , ''),
    RegS16(          4, 40104, 1, 'totvarh_sf'                         , None, None  , 'int'  , 0, 'TotVArh_SF'                     , ''),
    RegU16(          4, 40105, 3, 'evt'                                , None, None  , 'int'  , 0, 'Evt'                            , ''),
    RegU16(          4, 40110, 1, 'a_phase_volt_thd'                   , None, None  , 'float', 1, 'A phase volt THD'               , ''),
    RegU16(          4, 40111, 1, 'b_phase_volt_thd'                   , None, None  , 'float', 1, 'B phase volt THD'               , ''),
    RegU16(          4, 40112, 1, 'c_phase_volt_thd'                   , None, None  , 'float', 1, 'C phase volt THD'               , ''),
    RegU16(          4, 40113, 1, 'a_phase_curr_thd'                   , None, None  , 'float', 1, 'A phase Curr THD'               , ''),
    RegU16(          4, 40114, 1, 'b_phase_curr_thd'                   , None, None  , 'float', 1, 'B phase Curr THD'               , ''),
    RegU16(          4, 40115, 1, 'c_phase_curr_thd'                   , None, None  , 'float', 1, 'C phase Curr THD'               , ''),
    RegU16(          4, 40117, 1, 'barcode_a'                          , None, None  , 'int'  , 0, 'Barcode A'                      , ''),
    RegU16(          4, 40118, 1, 'barcode_b'                          , None, None  , 'int'  , 0, 'Barcode B'                      , ''),
    RegU16(          4, 40119, 1, 'barcode_c'                          , None, None  , 'int'  , 0, 'Barcode C'                      , ''),
    RegU16(          4, 40120, 1, 'version'                            , None, None  , 'int'  , 0, 'Version'                        , ''),
    RegU16(          4, 40121, 1, 'software_identification_number'     , None, None  , 'int'  , 0, 'Software Identification Number' , ''))
if __name__ == "__main__":
    MakeRegisters()


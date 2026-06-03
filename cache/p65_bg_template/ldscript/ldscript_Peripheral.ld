MEMORY
{
  ADCARESULT    : ORIGIN = 0x01000000, LENGTH = 0x1000
  ADCBRESULT    : ORIGIN = 0x01001000, LENGTH = 0x1000
  ADCCRESULT    : ORIGIN = 0x01002000, LENGTH = 0x1000
  ADCDRESULT    : ORIGIN = 0x01003000, LENGTH = 0x1000
  ADCERESULT    : ORIGIN = 0x01004000, LENGTH = 0x1000
  ADCFRESULT    : ORIGIN = 0x01005000, LENGTH = 0x1000
  ADCGRESULT    : ORIGIN = 0x01006000, LENGTH = 0x1000
  ADCHRESULT    : ORIGIN = 0x01007000, LENGTH = 0x1000
  DCSM_Z1_OTP   : ORIGIN = 0x01009000, LENGTH = 0x800
  DCSMBANK0_Z1_OTP   : ORIGIN = 0x01009800, LENGTH = 0x800
  DCSM_Z2_OTP   : ORIGIN = 0x0100A000, LENGTH = 0x800

  EPWM1         : ORIGIN = 0x01010000, LENGTH = 0x1000
  EPWM2         : ORIGIN = 0x01011000, LENGTH = 0x1000
  EPWM3         : ORIGIN = 0x01012000, LENGTH = 0x1000
  EPWM4         : ORIGIN = 0x01013000, LENGTH = 0x1000
  EPWM5         : ORIGIN = 0x01014000, LENGTH = 0x1000
  EPWM6         : ORIGIN = 0x01015000, LENGTH = 0x1000
  EPWM7         : ORIGIN = 0x01016000, LENGTH = 0x1000
  EPWM8         : ORIGIN = 0x01017000, LENGTH = 0x1000
  EPWM9         : ORIGIN = 0x01018000, LENGTH = 0x1000
  EPWM10        : ORIGIN = 0x01019000, LENGTH = 0x1000
  EPWM11        : ORIGIN = 0x0101A000, LENGTH = 0x1000
  EPWM12        : ORIGIN = 0x0101B000, LENGTH = 0x1000
  EPWM13        : ORIGIN = 0x0101C000, LENGTH = 0x1000
  EPWM14        : ORIGIN = 0x0101C000, LENGTH = 0x1000
  EPWM15        : ORIGIN = 0x0101C000, LENGTH = 0x1000
  EPWM16        : ORIGIN = 0x0101C000, LENGTH = 0x1000
  EPWM17        : ORIGIN = 0x0101C000, LENGTH = 0x1000
  EPWM18        : ORIGIN = 0x0101C000, LENGTH = 0x1000

  ECAP1         : ORIGIN = 0x01020000, LENGTH = 0x1000
  ECAP2         : ORIGIN = 0x01021000, LENGTH = 0x1000
  ECAP3         : ORIGIN = 0x01022000, LENGTH = 0x1000
  ECAP4         : ORIGIN = 0x01023000, LENGTH = 0x1000
  ECAP5         : ORIGIN = 0x01024000, LENGTH = 0x1000
  ECAP6         : ORIGIN = 0x01025000, LENGTH = 0x1000
  ECAP7         : ORIGIN = 0x01026000, LENGTH = 0x1000

  SFO           : ORIGIN = 0x01027000, LENGTH = 0x100
  HRPWMCAL2     : ORIGIN = 0x01027100, LENGTH = 0x100
  HRPWMCAL3     : ORIGIN = 0x01027200, LENGTH = 0x100
  SFOHHR        : ORIGIN = 0x01027400, LENGTH = 0x100
  HHRPWMCAL2    : ORIGIN = 0x01027500, LENGTH = 0x100
  HHRPWMCAL3    : ORIGIN = 0x01027600, LENGTH = 0x100
  HRCAP6        : ORIGIN = 0x01028000, LENGTH = 0x1000
  HRCAP7        : ORIGIN = 0x01029000, LENGTH = 0x1000

  EQEP1         : ORIGIN = 0x0102a000, LENGTH = 0x1000
  EQEP2         : ORIGIN = 0x0102b000, LENGTH = 0x1000
  EQEP3         : ORIGIN = 0x0102c000, LENGTH = 0x1000
  EQEP4         : ORIGIN = 0x0102d000, LENGTH = 0x1000
  EQEP5         : ORIGIN = 0x0102e000, LENGTH = 0x1000
  EQEP6         : ORIGIN = 0x0102f000, LENGTH = 0x1000

  CMPSS1        : ORIGIN = 0x01030000, LENGTH = 0x1000
  CMPSS2        : ORIGIN = 0x01031000, LENGTH = 0x1000
  CMPSS3        : ORIGIN = 0x01032000, LENGTH = 0x1000
  CMPSS4        : ORIGIN = 0x01033000, LENGTH = 0x1000
  CMPSS5        : ORIGIN = 0x01034000, LENGTH = 0x1000
  CMPSS6        : ORIGIN = 0x01035000, LENGTH = 0x1000
  CMPSS7        : ORIGIN = 0x01036000, LENGTH = 0x1000
  CMPSS8        : ORIGIN = 0x01037000, LENGTH = 0x1000
  CMPSS9        : ORIGIN = 0x01038000, LENGTH = 0x1000
  CMPSS10       : ORIGIN = 0x01039000, LENGTH = 0x1000
  CMPSS11       : ORIGIN = 0x0103a000, LENGTH = 0x1000

  DAC_A         : ORIGIN = 0x0103b000, LENGTH = 0x1000
  DAC_C         : ORIGIN = 0x0103c000, LENGTH = 0x1000

  SPIA          : ORIGIN = 0x01040000, LENGTH = 0x1000
  SPIB          : ORIGIN = 0x01041000, LENGTH = 0x1000
  SPIC          : ORIGIN = 0x01042000, LENGTH = 0x1000
  SPID          : ORIGIN = 0x01043000, LENGTH = 0x1000
  
  SDFM1         : ORIGIN = 0x01044000, LENGTH = 0x1000
  SDFM2         : ORIGIN = 0x01045000, LENGTH = 0x1000
  SDFM3         : ORIGIN = 0x01046000, LENGTH = 0x1000
  SDFM4         : ORIGIN = 0x01047000, LENGTH = 0x1000

  DMADW         : ORIGIN = 0x01048000, LENGTH = 0x1000
  DMACH1        : ORIGIN = 0x01048100, LENGTH = 0x100
  DMACH2        : ORIGIN = 0x01048200, LENGTH = 0x100
  DMACH3        : ORIGIN = 0x01048300, LENGTH = 0x100
  DMACH4        : ORIGIN = 0x01048400, LENGTH = 0x100
  DMACH5        : ORIGIN = 0x01048500, LENGTH = 0x100
  DMACH6        : ORIGIN = 0x01048600, LENGTH = 0x100
  DMA           : ORIGIN = 0x0104A000, LENGTH = 0x1000

  ADC_A         : ORIGIN = 0x01050000, LENGTH = 0x1000
  ADC_B         : ORIGIN = 0x01051000, LENGTH = 0x1000
  ADC_C         : ORIGIN = 0x01052000, LENGTH = 0x1000
  ADC_D         : ORIGIN = 0x01053000, LENGTH = 0x1000
  ADC_E         : ORIGIN = 0x01054000, LENGTH = 0x1000
  ADC_F         : ORIGIN = 0x01055000, LENGTH = 0x1000
  ADC_G         : ORIGIN = 0x01056000, LENGTH = 0x1000
  ADC_H         : ORIGIN = 0x01057000, LENGTH = 0x1000

  INPUTXBAR     : ORIGIN = 0x01060000, LENGTH = 0x1000
  EPWMXBARA     : ORIGIN = 0x01061000, LENGTH = 0x1000
  EPWMXBARB     : ORIGIN = 0x01062000, LENGTH = 0x1000
  CLBXBAR       : ORIGIN = 0x01064000, LENGTH = 0x1000
  OUTPUTXBAR    : ORIGIN = 0x01066000, LENGTH = 0x1000
  XBAR          : ORIGIN = 0x01069000, LENGTH = 0x1000
  GPIOCTRL      : ORIGIN = 0x0106B000, LENGTH = 0x1000
  GPIODATA      : ORIGIN = 0x0100C000, LENGTH = 0x1000
  GPIODATA_READ : ORIGIN = 0x0100C0A0, LENGTH = 0x1000
  DEVCFG        : ORIGIN = 0x01070000, LENGTH = 0x200
  SYNCSOC       : ORIGIN = 0x01070130, LENGTH = 0x100
  CLKCFG        : ORIGIN = 0x01071000, LENGTH = 0x1000
  CPUSYS        : ORIGIN = 0x01072000, LENGTH = 0x1000
  ANALOGSUBSYS  : ORIGIN = 0x01073000, LENGTH = 0x1000
  MEM_CFG       : ORIGIN = 0x01078000, LENGTH = 0x1000
  DCSM_Z1       : ORIGIN = 0x01079000, LENGTH = 0x1000
  DCSM_COMMON   : ORIGIN = 0x0107A000, LENGTH = 0x1000
  DCSM_Z2       : ORIGIN = 0x0107B000, LENGTH = 0x1000
  TRIM          : ORIGIN = 0x0107C000, LENGTH = 0x1000
  NMIINTRUPT    : ORIGIN = 0x0107D000, LENGTH = 0x1000
  SYSERR        : ORIGIN = 0x0107E000, LENGTH = 0x1000
  XINT          : ORIGIN = 0x0107F000, LENGTH = 0x1000
  CANA          : ORIGIN = 0x01080000, LENGTH = 0x1000
  CANB          : ORIGIN = 0x01081000, LENGTH = 0x1000
  CANC          : ORIGIN = 0x01082000, LENGTH = 0x1000
  UART_A        : ORIGIN = 0x01088000, LENGTH = 0x1000
  UART_B        : ORIGIN = 0x01089000, LENGTH = 0x1000
  I2CA          : ORIGIN = 0x0108A000, LENGTH = 0x1000
  I2CB          : ORIGIN = 0x0108B000, LENGTH = 0x1000
  LINA          : ORIGIN = 0x0108C000, LENGTH = 0x1000
  LINB          : ORIGIN = 0x0108D000, LENGTH = 0x1000
  CLB1_CFG      : ORIGIN = 0x01090000, LENGTH = 0x0100
  CLB1_CTRL     : ORIGIN = 0x01090100, LENGTH = 0x0080
  CLB1_EXCH     : ORIGIN = 0x01090180, LENGTH = 0x0210
  CLB2_CFG      : ORIGIN = 0x01091000, LENGTH = 0x0100
  CLB2_CTRL     : ORIGIN = 0x01091100, LENGTH = 0x0080
  CLB2_EXCH     : ORIGIN = 0x01091180, LENGTH = 0x0210
  CLB3_CFG      : ORIGIN = 0x01092000, LENGTH = 0x0100
  CLB3_CTRL     : ORIGIN = 0x01092100, LENGTH = 0x0080
  CLB3_EXCH     : ORIGIN = 0x01092180, LENGTH = 0x0210
  CLB4_CFG      : ORIGIN = 0x01093000, LENGTH = 0x0100
  CLB4_CTRL     : ORIGIN = 0x01093100, LENGTH = 0x0080
  CLB4_EXCH     : ORIGIN = 0x01093180, LENGTH = 0x0210
  CLB5_CFG      : ORIGIN = 0x01094000, LENGTH = 0x0100
  CLB5_CTRL     : ORIGIN = 0x01094100, LENGTH = 0x0080
  CLB5_EXCH     : ORIGIN = 0x01094180, LENGTH = 0x0210
  CLB6_CFG      : ORIGIN = 0x01095000, LENGTH = 0x0100
  CLB6_CTRL     : ORIGIN = 0x01095100, LENGTH = 0x0080
  CLB6_EXCH     : ORIGIN = 0x01095180, LENGTH = 0x0210
  SCIA          : ORIGIN = 0x01096000, LENGTH = 0x1000
  SCIB          : ORIGIN = 0x01097000, LENGTH = 0x1000
  FSITXA        : ORIGIN = 0x01099000, LENGTH = 0x1000
  FSIRXA        : ORIGIN = 0x0109A000, LENGTH = 0x1000
  FSITXB        : ORIGIN = 0x0109B000, LENGTH = 0x1000
  FSIRXB        : ORIGIN = 0x0109C000, LENGTH = 0x1000
  FSIRXC        : ORIGIN = 0x0109D000, LENGTH = 0x1000
  FSIRXD        : ORIGIN = 0x0109E000, LENGTH = 0x1000

  PMBUSA        : ORIGIN = 0x0109F000, LENGTH = 0x1000

  CPU1TOCPU2IPC : ORIGIN = 0x00200000, LENGTH = 0x1000
  CPU1TOCLA1IPC : ORIGIN = 0x00201000, LENGTH = 0x1000
  CLA1TOCPU1IPC : ORIGIN = 0x00202000, LENGTH = 0x1000
  CPU2TOCPU1IPC : ORIGIN = 0x00203000, LENGTH = 0x1000
  CPU2TOCLA2IPC : ORIGIN = 0x00204000, LENGTH = 0x1000
  CLA2TOCPU2IPC : ORIGIN = 0x00205000, LENGTH = 0x1000
  FLASH0CTRL    : ORIGIN = 0x010A0000, LENGTH = 0x1000
  EMIF          : ORIGIN = 0x20000000, LENGTH = 0x1000
  USB           : ORIGIN = 0x30300000, LENGTH = 0x1000
  PIECTRL       : ORIGIN = 0x007F0100, LENGTH = 0x100
  DEBUG         : ORIGIN = 0x007F0200, LENGTH = 0x100
  CPUTIMER0     : ORIGIN = 0x007F0300, LENGTH = 0x20
  CPUTIMER1     : ORIGIN = 0x007F0320, LENGTH = 0x20
  CPUTIMER2     : ORIGIN = 0x007F0340, LENGTH = 0x20
  CR            : ORIGIN = 0x007F0400, LENGTH = 0x100
  GR            : ORIGIN = 0x007F0500, LENGTH = 0x100
  MOB           : ORIGIN = 0x007F0600, LENGTH = 0x100
  EXP           : ORIGIN = 0x007F0700, LENGTH = 0x100
  WD            : ORIGIN = 0x007F0800, LENGTH = 0x100
  VCU           : ORIGIN = 0x007F0B00, LENGTH = 0x100
  TRACE_BUFFER  : ORIGIN = 0x007F0C00, LENGTH = 0x100
  WATCH_POINT   : ORIGIN = 0x007F0D00, LENGTH = 0x100
  ECC           : ORIGIN = 0x007F0E00, LENGTH = 0x100
  ERADGLOBAL    : ORIGIN = 0x007F0F00, LENGTH = 0x100
  ERADHWBP1     : ORIGIN = 0x007F1000, LENGTH = 0x100
  ERADHWBP2     : ORIGIN = 0x007F1100, LENGTH = 0x100
  ERADHWBP3     : ORIGIN = 0x007F1200, LENGTH = 0x100
  ERADHWBP4     : ORIGIN = 0x007F1300, LENGTH = 0x100
  ERADHWBP5     : ORIGIN = 0x007F1400, LENGTH = 0x100
  ERADHWBP6     : ORIGIN = 0x007F1500, LENGTH = 0x100
  ERADHWBP7     : ORIGIN = 0x007F1600, LENGTH = 0x100
  ERADHWBP8     : ORIGIN = 0x007F1700, LENGTH = 0x100
  ERADCOUNTER1  : ORIGIN = 0x007F1800, LENGTH = 0x100
  ERADCOUNTER2  : ORIGIN = 0x007F1900, LENGTH = 0x100
  ERADCOUNTER3  : ORIGIN = 0x007F1A00, LENGTH = 0x100
  ERADCOUNTER4  : ORIGIN = 0x007F1B00, LENGTH = 0x100
  CLA1          : ORIGIN = 0x007F1C00, LENGTH = 0x100
  ERADCRCGLOBAL : ORIGIN = 0x007F1D00, LENGTH = 0x100
}

SECTIONS
{
    AdcaResultRegsFile(NOLOAD)    : { KEEP(*(AdcaResultRegsFile)) }    > ADCARESULT
    AdcbResultRegsFile(NOLOAD)    : { KEEP(*(AdcbResultRegsFile)) }    > ADCBRESULT
    AdccResultRegsFile(NOLOAD)    : { KEEP(*(AdccResultRegsFile)) }    > ADCCRESULT
    AdcdResultRegsFile(NOLOAD)    : { KEEP(*(AdcdResultRegsFile)) }    > ADCDRESULT
    AdceResultRegsFile(NOLOAD)    : { KEEP(*(AdceResultRegsFile)) }    > ADCERESULT
    AdcfResultRegsFile(NOLOAD)    : { KEEP(*(AdcfResultRegsFile)) }    > ADCFRESULT
    AdcgResultRegsFile(NOLOAD)    : { KEEP(*(AdcgResultRegsFile)) }    > ADCGRESULT
    AdchResultRegsFile(NOLOAD)    : { KEEP(*(AdchResultRegsFile)) }    > ADCHRESULT
    DcsmZ1RegsFile(NOLOAD)        : { KEEP(*(DcsmZ1RegsFile)) }        > DCSM_Z1
    DcsmZ2RegsFile(NOLOAD)        : { KEEP(*(DcsmZ2RegsFile)) }        > DCSM_Z2
    DcsmCommonRegsFile(NOLOAD)    : { KEEP(*(DcsmCommonRegsFile)) }    > DCSM_COMMON
    EPwm1RegsFile(NOLOAD)         : { KEEP(*(EPwm1RegsFile)) }         > EPWM1
    EPwm2RegsFile(NOLOAD)         : { KEEP(*(EPwm2RegsFile)) }         > EPWM2
    EPwm3RegsFile(NOLOAD)         : { KEEP(*(EPwm3RegsFile)) }         > EPWM3
    EPwm4RegsFile(NOLOAD)         : { KEEP(*(EPwm4RegsFile)) }         > EPWM4
    EPwm5RegsFile(NOLOAD)         : { KEEP(*(EPwm5RegsFile)) }         > EPWM5
    EPwm6RegsFile(NOLOAD)         : { KEEP(*(EPwm6RegsFile)) }         > EPWM6
    EPwm7RegsFile(NOLOAD)         : { KEEP(*(EPwm7RegsFile)) }         > EPWM7
    EPwm8RegsFile(NOLOAD)         : { KEEP(*(EPwm8RegsFile)) }         > EPWM8
    EPwm9RegsFile(NOLOAD)         : { KEEP(*(EPwm9RegsFile)) }         > EPWM9
    EPwm10RegsFile(NOLOAD)        : { KEEP(*(EPwm10RegsFile)) }        > EPWM10
    EPwm11RegsFile(NOLOAD)        : { KEEP(*(EPwm11RegsFile)) }        > EPWM11
    EPwm12RegsFile(NOLOAD)        : { KEEP(*(EPwm12RegsFile)) }        > EPWM12
    EPwm13RegsFile(NOLOAD)        : { KEEP(*(EPwm13RegsFile)) }        > EPWM13
    EPwm14RegsFile(NOLOAD)        : { KEEP(*(EPwm14RegsFile)) }        > EPWM14
    EPwm15RegsFile(NOLOAD)        : { KEEP(*(EPwm15RegsFile)) }        > EPWM15
    EPwm16RegsFile(NOLOAD)        : { KEEP(*(EPwm16RegsFile)) }        > EPWM16
    EPwm17RegsFile(NOLOAD)        : { KEEP(*(EPwm17RegsFile)) }        > EPWM17
    EPwm18RegsFile(NOLOAD)        : { KEEP(*(EPwm18RegsFile)) }        > EPWM18
    EQep1RegsFile(NOLOAD)         : { KEEP(*(EQep1RegsFile)) }         > EQEP1
    EQep2RegsFile(NOLOAD)         : { KEEP(*(EQep2RegsFile)) }         > EQEP2
    EQep3RegsFile(NOLOAD)         : { KEEP(*(EQep3RegsFile)) }         > EQEP3
    EQep4RegsFile(NOLOAD)         : { KEEP(*(EQep4RegsFile)) }         > EQEP4
    EQep5RegsFile(NOLOAD)         : { KEEP(*(EQep5RegsFile)) }         > EQEP5
    EQep6RegsFile(NOLOAD)         : { KEEP(*(EQep6RegsFile)) }         > EQEP6
    ECap1RegsFile(NOLOAD)         : { KEEP(*(ECap1RegsFile)) }         > ECAP1
    ECap2RegsFile(NOLOAD)         : { KEEP(*(ECap2RegsFile)) }         > ECAP2
    ECap3RegsFile(NOLOAD)         : { KEEP(*(ECap3RegsFile)) }         > ECAP3
    ECap4RegsFile(NOLOAD)         : { KEEP(*(ECap4RegsFile)) }         > ECAP4
    ECap5RegsFile(NOLOAD)         : { KEEP(*(ECap5RegsFile)) }         > ECAP5
    ECap6RegsFile(NOLOAD)         : { KEEP(*(ECap6RegsFile)) }         > ECAP6
    ECap7RegsFile(NOLOAD)         : { KEEP(*(ECap7RegsFile)) }         > ECAP7
    SFORegsFile(NOLOAD)           : { KEEP(*(SFORegsFile)) }           > SFO
    SFOHHRRegsFile(NOLOAD)        : { KEEP(*(SFOHHRRegsFile)) }        > SFOHHR
    Cmpss1RegsFile(NOLOAD)        : { KEEP(*(Cmpss1RegsFile)) }        > CMPSS1
    Cmpss2RegsFile(NOLOAD)        : { KEEP(*(Cmpss2RegsFile)) }        > CMPSS2
    Cmpss3RegsFile(NOLOAD)        : { KEEP(*(Cmpss3RegsFile)) }        > CMPSS3
    Cmpss4RegsFile(NOLOAD)        : { KEEP(*(Cmpss4RegsFile)) }        > CMPSS4
    Cmpss5RegsFile(NOLOAD)        : { KEEP(*(Cmpss5RegsFile)) }        > CMPSS5
    Cmpss6RegsFile(NOLOAD)        : { KEEP(*(Cmpss6RegsFile)) }        > CMPSS6
    Cmpss7RegsFile(NOLOAD)        : { KEEP(*(Cmpss7RegsFile)) }        > CMPSS7
    Cmpss8RegsFile(NOLOAD)        : { KEEP(*(Cmpss8RegsFile)) }        > CMPSS8
    Cmpss9RegsFile(NOLOAD)        : { KEEP(*(Cmpss9RegsFile)) }        > CMPSS9
    Cmpss10RegsFile(NOLOAD)       : { KEEP(*(Cmpss10RegsFile)) }       > CMPSS10
    Cmpss11RegsFile(NOLOAD)       : { KEEP(*(Cmpss11RegsFile)) }       > CMPSS11
    DacaRegsFile(NOLOAD)          : { KEEP(*(DacaRegsFile)) }          > DAC_A
    DaccRegsFile(NOLOAD)          : { KEEP(*(DaccRegsFile)) }          > DAC_C
    SpiaRegsFile(NOLOAD)          : { KEEP(*(SpiaRegsFile)) }          > SPIA
    SpibRegsFile(NOLOAD)          : { KEEP(*(SpibRegsFile)) }          > SPIB
    SpicRegsFile(NOLOAD)          : { KEEP(*(SpicRegsFile)) }          > SPIC
    SpidRegsFile(NOLOAD)          : { KEEP(*(SpidRegsFile)) }          > SPID
    Sdfm1RegsFile(NOLOAD)         : { KEEP(*(Sdfm1RegsFile)) }         > SDFM1
    Sdfm2RegsFile(NOLOAD)         : { KEEP(*(Sdfm2RegsFile)) }         > SDFM2
    Sdfm3RegsFile(NOLOAD)         : { KEEP(*(Sdfm3RegsFile)) }         > SDFM3
    Sdfm4RegsFile(NOLOAD)         : { KEEP(*(Sdfm4RegsFile)) }         > SDFM4
    DmaDwRegsFile(NOLOAD)         : { KEEP(*(DmaDwRegsFile)) }         > DMADW
    DmaCh1RegsFile(NOLOAD)        : { KEEP(*(DmaCH1RegsFile)) }        > DMACH1
    DmaCh2RegsFile(NOLOAD)        : { KEEP(*(DmaCH2RegsFile)) }        > DMACH2
    DmaCh3RegsFile(NOLOAD)        : { KEEP(*(DmaCH3RegsFile)) }        > DMACH3
    DmaCh4RegsFile(NOLOAD)        : { KEEP(*(DmaCH4RegsFile)) }        > DMACH4
    DmaCh5RegsFile(NOLOAD)        : { KEEP(*(DmaCH5RegsFile)) }        > DMACH5
    DmaCh6RegsFile(NOLOAD)        : { KEEP(*(DmaCH6RegsFile)) }        > DMACH6
    DmaRegsFile(NOLOAD)           : { KEEP(*(DmaRegsFile)) }           > DMA
    AdcaRegsFile(NOLOAD)          : { KEEP(*(AdcaRegsFile)) }          > ADC_A
    AdcbRegsFile(NOLOAD)          : { KEEP(*(AdcbRegsFile)) }          > ADC_B
    AdccRegsFile(NOLOAD)          : { KEEP(*(AdccRegsFile)) }          > ADC_C
    AdcdRegsFile(NOLOAD)          : { KEEP(*(AdcdRegsFile)) }          > ADC_D
    AdceRegsFile(NOLOAD)          : { KEEP(*(AdceRegsFile)) }          > ADC_E
    AdcfRegsFile(NOLOAD)          : { KEEP(*(AdcfRegsFile)) }          > ADC_F
    AdcgRegsFile(NOLOAD)          : { KEEP(*(AdcgRegsFile)) }          > ADC_G
    AdchRegsFile(NOLOAD)          : { KEEP(*(AdchRegsFile)) }          > ADC_H
    EPwmXbaraRegsFile(NOLOAD)     : { KEEP(*(EPwmXbaraRegsFile)) }     > EPWMXBARA
    EPwmXbarbRegsFile(NOLOAD)     : { KEEP(*(EPwmXbarbRegsFile)) }     > EPWMXBARB
    InputXbarRegsFile(NOLOAD)     : { KEEP(*(InputXbarRegsFile)) }     > INPUTXBAR
    XbarRegsFile(NOLOAD)          : { KEEP(*(XbarRegsFile)) }          > XBAR
    ClbXbarRegsFile(NOLOAD)       : { KEEP(*(ClbXbarRegsFile)) }       > CLBXBAR
    OutputXbarRegsFile(NOLOAD)    : { KEEP(*(OutputXbarRegsFile)) }    > OUTPUTXBAR
    GpioCtrlRegsFile(NOLOAD)      : { KEEP(*(GpioCtrlRegsFile)) }      > GPIOCTRL
    DevCfgRegsFile(NOLOAD)        : { KEEP(*(DevCfgRegsFile)) }        > DEVCFG
    SyncSocRegsFile(NOLOAD)       : { KEEP(*(SyncSocRegsFile)) }       > SYNCSOC
    ClkCfgRegsFile(NOLOAD)        : { KEEP(*(ClkCfgRegsFile)) }        > CLKCFG
    CpuSysRegsFile(NOLOAD)        : { KEEP(*(CpuSysRegsFile)) }        > CPUSYS
    AnalogSubsysRegsFile(NOLOAD)  : { KEEP(*(AnalogSubsysRegsFile)) }  > ANALOGSUBSYS
    MemCfgRegsFile(NOLOAD)        : { KEEP(*(MemCfgRegsFile)) }        > MEM_CFG
    TrimRegsFile(NOLOAD)          : { KEEP(*(TrimRegsFile)) }          > TRIM
    NmiIntruptRegsFile(NOLOAD)    : { KEEP(*(NmiIntruptRegsFile)) }    > NMIINTRUPT
    SysErrRegsFile(NOLOAD)        : { KEEP(*(SysErrRegsFile)) }        > SYSERR
    EmifRegsFile(NOLOAD)          : { KEEP(*(EmifRegsFile)) }          > EMIF
    CanaRegsFile(NOLOAD)          : { KEEP(*(CanaRegsFile)) }          > CANA
    CanbRegsFile(NOLOAD)          : { KEEP(*(CanbRegsFile)) }          > CANB
    CancRegsFile(NOLOAD)          : { KEEP(*(CancRegsFile)) }          > CANC
    SciaRegsFile(NOLOAD)          : { KEEP(*(SciaRegsFile)) }          > SCIA
    ScibRegsFile(NOLOAD)          : { KEEP(*(ScibRegsFile)) }          > SCIB
    I2caRegsFile(NOLOAD)          : { KEEP(*(I2caRegsFile)) }          > I2CA
    I2cbRegsFile(NOLOAD)          : { KEEP(*(I2cbRegsFile)) }          > I2CB
    Clb1LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb1LogicCfgRegsFile)) }  > CLB1_CFG
    Clb1LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb1LogicCtrlRegsFile)) } > CLB1_CTRL
    Clb1DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb1DataExchRegsFile)) }  > CLB1_EXCH
    Clb2LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb2LogicCfgRegsFile)) }  > CLB2_CFG
    Clb2LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb2LogicCtrlRegsFile)) } > CLB2_CTRL
    Clb2DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb2DataExchRegsFile)) }  > CLB2_EXCH
    Clb3LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb3LogicCfgRegsFile)) }  > CLB3_CFG
    Clb3LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb3LogicCtrlRegsFile)) } > CLB3_CTRL
    Clb3DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb3DataExchRegsFile)) }  > CLB3_EXCH
    Clb4LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb4LogicCfgRegsFile)) }  > CLB4_CFG
    Clb4LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb4LogicCtrlRegsFile)) } > CLB4_CTRL
    Clb4DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb4DataExchRegsFile)) }  > CLB4_EXCH
    Clb5LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb5LogicCfgRegsFile)) }  > CLB5_CFG
    Clb5LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb5LogicCtrlRegsFile)) } > CLB5_CTRL
    Clb5DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb5DataExchRegsFile)) }  > CLB5_EXCH
    Clb6LogicCfgRegsFile(NOLOAD)  : { KEEP(*(Clb6LogicCfgRegsFile)) }  > CLB6_CFG
    Clb6LogicCtrlRegsFile(NOLOAD) : { KEEP(*(Clb6LogicCtrlRegsFile)) } > CLB6_CTRL
    Clb6DataExchRegsFile(NOLOAD)  : { KEEP(*(Clb6DataExchRegsFile)) }  > CLB6_EXCH
    Cpu1toCpu2IpcRegsFile(NOLOAD) : { KEEP(*(Cpu1toCpu2IpcRegsFile)) } > CPU1TOCPU2IPC
    Cpu1toCla1IpcRegsFile(NOLOAD) : { KEEP(*(Cpu1toCla1IpcRegsFile)) } > CPU1TOCLA1IPC
    Cla1toCpu1IpcRegsFile(NOLOAD) : { KEEP(*(Cla1toCpu1IpcRegsFile)) } > CLA1TOCPU1IPC
    Cpu2toCpu1IpcRegsFile(NOLOAD) : { KEEP(*(Cpu2toCpu1IpcRegsFile)) } > CPU2TOCPU1IPC
    Cpu2toCla2IpcRegsFile(NOLOAD) : { KEEP(*(Cpu2toCla2IpcRegsFile)) } > CPU2TOCLA2IPC
    Cla2toCpu2IpcRegsFile(NOLOAD) : { KEEP(*(Cla2toCpu2IpcRegsFile)) } > CLA2TOCPU2IPC
    Flash0CtrlRegsFile(NOLOAD)    : { KEEP(*(Flash0CtrlRegsFile)) }    > FLASH0CTRL
    EmifCtrlRegsFile(NOLOAD)      : { KEEP(*(EmifCtrlRegsFile)) }      > EMIF
    GpioDataRegsFile(NOLOAD)      : { KEEP(*(GpioDataRegsFile)) }      > GPIODATA
    PieCtrlRegsFile(NOLOAD)       : { KEEP(*(PieCtrlRegsFile)) }       > PIECTRL
    CpuTimer0RegsFile(NOLOAD)     : { KEEP(*(CpuTimer0RegsFile)) }     > CPUTIMER0
    CpuTimer1RegsFile(NOLOAD)     : { KEEP(*(CpuTimer1RegsFile)) }     > CPUTIMER1
    CpuTimer2RegsFile(NOLOAD)     : { KEEP(*(CpuTimer2RegsFile)) }     > CPUTIMER2
    ExpRegsFile(NOLOAD)           : { KEEP(*(ExpRegsFile)) }           > EXP
    WdRegsFile(NOLOAD)            : { KEEP(*(WdRegsFile)) }            > WD
    TraceBufferRegsFile(NOLOAD)   : { KEEP(*(TraceBufferRegsFile)) }   > TRACE_BUFFER
    WatchPointRegsFile(NOLOAD)    : { KEEP(*(WatchPointRegsFile)) }    > WATCH_POINT
    EccRegsFile(NOLOAD)           : { KEEP(*(EccRegsFile)) }           > ECC
    EradGlobalRegsFile(NOLOAD)    : { KEEP(*(EradGlobalRegsFile)) }    > ERADGLOBAL
    EradHWBP1RegsFile(NOLOAD)     : { KEEP(*(EradHWBP1RegsFile)) }     > ERADHWBP1
    EradHWBP2RegsFile(NOLOAD)     : { KEEP(*(EradHWBP2RegsFile)) }     > ERADHWBP2
    EradHWBP3RegsFile(NOLOAD)     : { KEEP(*(EradHWBP3RegsFile)) }     > ERADHWBP3
    EradHWBP4RegsFile(NOLOAD)     : { KEEP(*(EradHWBP4RegsFile)) }     > ERADHWBP4
    EradHWBP5RegsFile(NOLOAD)     : { KEEP(*(EradHWBP5RegsFile)) }     > ERADHWBP5
    EradHWBP6RegsFile(NOLOAD)     : { KEEP(*(EradHWBP6RegsFile)) }     > ERADHWBP6
    EradHWBP7RegsFile(NOLOAD)     : { KEEP(*(EradHWBP7RegsFile)) }     > ERADHWBP7
    EradHWBP8RegsFile(NOLOAD)     : { KEEP(*(EradHWBP8RegsFile)) }     > ERADHWBP8
    EradCounter1RegsFile(NOLOAD)  : { KEEP(*(EradCounter1RegsFile)) }  > ERADCOUNTER1
    EradCounter2RegsFile(NOLOAD)  : { KEEP(*(EradCounter2RegsFile)) }  > ERADCOUNTER2
    EradCounter3RegsFile(NOLOAD)  : { KEEP(*(EradCounter3RegsFile)) }  > ERADCOUNTER3
    EradCounter4RegsFile(NOLOAD)  : { KEEP(*(EradCounter4RegsFile)) }  > ERADCOUNTER4
    Cla1RegsFile(NOLOAD)          : { KEEP(*(Cla1RegsFile)) }          > CLA1
}

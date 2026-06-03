MEMORY
{
  PIECTRL       : ORIGIN = 0x007F0100, LENGTH = 0x100
  DEBUG         : ORIGIN = 0x007F0200, LENGTH = 0x100
  CPUTIMER0     : ORIGIN = 0x007F0300, LENGTH = 0x14
  CPUTIMER1     : ORIGIN = 0x007F0314, LENGTH = 0x14
  CPUTIMER2     : ORIGIN = 0x007F0328, LENGTH = 0x14
  CPUTIMERSYS   : ORIGIN = 0x007F03A0, LENGTH = 0x0C
  CPUTIMER0LC2  : ORIGIN = 0x007F03B0, LENGTH = 0x04
  CPUTIMER1LC2  : ORIGIN = 0x007F03B4, LENGTH = 0x04
  CPUTIMER2LC2  : ORIGIN = 0x007F03B8, LENGTH = 0x04
  CR            : ORIGIN = 0x007F0400, LENGTH = 0x100
  GR            : ORIGIN = 0x007F0500, LENGTH = 0x100
  MOB           : ORIGIN = 0x007F0600, LENGTH = 0x100
  EXP           : ORIGIN = 0x007F0700, LENGTH = 0x100
  WD            : ORIGIN = 0x007F0800, LENGTH = 0x100
  IPCEVENT      : ORIGIN = 0x007F0900, LENGTH = 0x100
  IPCCMD        : ORIGIN = 0x007F0A00, LENGTH = 0x100
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
  CLKCFG        : ORIGIN = 0x01000000, LENGTH = 0x200
  CPUSYS        : ORIGIN = 0x01001000, LENGTH = 0x400
  DEVCFG        : ORIGIN = 0x01001000, LENGTH = 0x400
  XINT          : ORIGIN = 0x010011B0, LENGTH = 0x50
  NMIINTRUPT    : ORIGIN = 0x01001200, LENGTH = 0x100
  DCC0          : ORIGIN = 0x01002000, LENGTH = 0x1000
  GPIOCTRL      : ORIGIN = 0x01003000, LENGTH = 0x1000
  GPIODATA      : ORIGIN = 0x01004000, LENGTH = 0x1000
  INPUTXBAR     : ORIGIN = 0x01005000, LENGTH = 0x1000
  EPWMXBAR      : ORIGIN = 0x01006000, LENGTH = 0x1000
  OUTPUTXBAR    : ORIGIN = 0x01007000, LENGTH = 0x1000
  XBAR          : ORIGIN = 0x01008000, LENGTH = 0x1000
  DMA           : ORIGIN = 0x01009000, LENGTH = 0x1000
  DMACH1        : ORIGIN = 0x01009100, LENGTH = 0x100
  DMACH2        : ORIGIN = 0x01009200, LENGTH = 0x100
  DMACH3        : ORIGIN = 0x01009300, LENGTH = 0x100
  DMACH4        : ORIGIN = 0x01009400, LENGTH = 0x100
  DMACH5        : ORIGIN = 0x01009500, LENGTH = 0x100
  DMACH6        : ORIGIN = 0x01009600, LENGTH = 0x100
  ANALOGSUBSYS  : ORIGIN = 0x0100A000, LENGTH = 0x1000
  ADC_A         : ORIGIN = 0x0100B000, LENGTH = 0x100
  ADCARESULT    : ORIGIN = 0x0100B100, LENGTH = 0x100
  ADC_B         : ORIGIN = 0x0100B200, LENGTH = 0x100
  ADCBRESULT    : ORIGIN = 0x0100B300, LENGTH = 0x100
  ADC_C         : ORIGIN = 0x0100B400, LENGTH = 0x100
  ADCCRESULT    : ORIGIN = 0x0100B500, LENGTH = 0x100
  PGA1          : ORIGIN = 0x0100C000, LENGTH = 0x20
  PGA2          : ORIGIN = 0x0100C020, LENGTH = 0x20
  PGA3          : ORIGIN = 0x0100C040, LENGTH = 0x20
  PGA4          : ORIGIN = 0x0100C060, LENGTH = 0x20
  PGA5          : ORIGIN = 0x0100C080, LENGTH = 0x20
  PGA6          : ORIGIN = 0x0100C0A0, LENGTH = 0x20
  PGA7          : ORIGIN = 0x0100C0C0, LENGTH = 0x20
  DAC_A         : ORIGIN = 0x0100D000, LENGTH = 0x40
  DAC_B         : ORIGIN = 0x0100D040, LENGTH = 0x40
  CMPSS1        : ORIGIN = 0x0100E000, LENGTH = 0x100
  CMPSS2        : ORIGIN = 0x0100E100, LENGTH = 0x100
  CMPSS3        : ORIGIN = 0x0100E200, LENGTH = 0x100
  CMPSS4        : ORIGIN = 0x0100E300, LENGTH = 0x100
  CMPSS5        : ORIGIN = 0x0100E400, LENGTH = 0x100
  CMPSS6        : ORIGIN = 0x0100E500, LENGTH = 0x100
  CMPSS7        : ORIGIN = 0x0100E600, LENGTH = 0x100
  SDFM          : ORIGIN = 0x0100F000, LENGTH = 0x1000
  ECAP1         : ORIGIN = 0x01010000, LENGTH = 0x80
  ECAP2         : ORIGIN = 0x01010080, LENGTH = 0x80
  ECAP3         : ORIGIN = 0x01010100, LENGTH = 0x80
  ECAP4         : ORIGIN = 0x01010180, LENGTH = 0x80
  ECAP5         : ORIGIN = 0x01010200, LENGTH = 0x80
  ECAP6         : ORIGIN = 0x01010280, LENGTH = 0x40
  ECAP7         : ORIGIN = 0x01010300, LENGTH = 0x40
  HRCAP6        : ORIGIN = 0x010102C0, LENGTH = 0x40
  HRCAP7        : ORIGIN = 0x01010340, LENGTH = 0x40
  SYNCSOC       : ORIGIN = 0x01010380, LENGTH = 0x80
  SFO           : ORIGIN = 0x01010400, LENGTH = 0x80
  SFOHHR        : ORIGIN = 0x01010480, LENGTH = 0x80
  EPWM9         : ORIGIN = 0x01010600, LENGTH = 0x200
  EPWM10        : ORIGIN = 0x01010800, LENGTH = 0x200
  EPWM11        : ORIGIN = 0x01010A00, LENGTH = 0x200
  EPWM12        : ORIGIN = 0x01010C00, LENGTH = 0x200
  EPWM1         : ORIGIN = 0x01011000, LENGTH = 0x200
  EPWM2         : ORIGIN = 0x01011200, LENGTH = 0x200
  EPWM3         : ORIGIN = 0x01011400, LENGTH = 0x200
  EPWM4         : ORIGIN = 0x01011600, LENGTH = 0x200
  EPWM5         : ORIGIN = 0x01011800, LENGTH = 0x200
  EPWM6         : ORIGIN = 0x01011A00, LENGTH = 0x200
  EPWM7         : ORIGIN = 0x01011C00, LENGTH = 0x200
  EPWM8         : ORIGIN = 0x01011E00, LENGTH = 0x200
  EQEP1         : ORIGIN = 0x01012000, LENGTH = 0x800
  EQEP2         : ORIGIN = 0x01012800, LENGTH = 0x800
  SPIA          : ORIGIN = 0x01013000, LENGTH = 0x1000
  SPIB          : ORIGIN = 0x01014000, LENGTH = 0x1000
  SCIA          : ORIGIN = 0x01015000, LENGTH = 0x1000
  SCIB          : ORIGIN = 0x01016000, LENGTH = 0x1000
  I2CA          : ORIGIN = 0x01017000, LENGTH = 0x1000
  PMBUSA        : ORIGIN = 0x01018000, LENGTH = 0x1000
  LINA          : ORIGIN = 0x01019000, LENGTH = 0x1000
  FSITXA        : ORIGIN = 0x0101A000, LENGTH = 0x1000
  FSIRXA        : ORIGIN = 0x0101B000, LENGTH = 0x1000
  REGFILE       : ORIGIN = 0x0101C000, LENGTH = 0x1000
  CANFDA        : ORIGIN = 0x01052000, LENGTH = 0x1000
  CANFDB        : ORIGIN = 0x01053000, LENGTH = 0x1000
  HRADC_A       : ORIGIN = 0x01054000, LENGTH = 0x100
  HRADCARESULT  : ORIGIN = 0x01054100, LENGTH = 0x300
  HRADC_B       : ORIGIN = 0x01054400, LENGTH = 0x100
  HRADCBRESULT  : ORIGIN = 0x01054500, LENGTH = 0x300
  HRADC_C       : ORIGIN = 0x01054800, LENGTH = 0x100
  HRADCCRESULT  : ORIGIN = 0x01054900, LENGTH = 0x300
  FLASH0CTRL    : ORIGIN = 0x01040000, LENGTH = 0x1000
  XINTFA        : ORIGIN = 0x20000000, LENGTH = 0x1000
}

SECTIONS
{
    PieCtrlRegsFile(NOLOAD)       : { *(PieCtrlRegsFile) }       > PIECTRL
    CpuTimer0RegsFile(NOLOAD)     : { *(CpuTimer0RegsFile) }     > CPUTIMER0
    CpuTimer1RegsFile(NOLOAD)     : { *(CpuTimer1RegsFile) }     > CPUTIMER1
    CpuTimer2RegsFile(NOLOAD)     : { *(CpuTimer2RegsFile) }     > CPUTIMER2
    CpuTimerSysRegsFile(NOLOAD)   : { *(CpuTimerSysRegsFile) }   > CPUTIMERSYS
    CpuTimer0LC2RegsFile(NOLOAD)  : { *(CpuTimer0LC2RegsFile) }  > CPUTIMER0LC2
    CpuTimer1LC2RegsFile(NOLOAD)  : { *(CpuTimer1LC2RegsFile) }  > CPUTIMER1LC2
    CpuTimer2LC2RegsFile(NOLOAD)  : { *(CpuTimer2LC2RegsFile) }  > CPUTIMER2LC2
    ExpRegsFile(NOLOAD)           : { *(ExpRegsFile) }           > EXP
    WdRegsFile(NOLOAD)            : { *(WdRegsFile) }            > WD
    IpcEventRegsFile(NOLOAD)      : { *(IpcEventRegsFile) }      > IPCEVENT
    IpcCmdRegsFile(NOLOAD)        : { *(IpcCmdRegsFile) }        > IPCCMD
    TraceBufferRegsFile(NOLOAD)   : { *(TraceBufferRegsFile) }   > TRACE_BUFFER
    WatchPointRegsFile(NOLOAD)    : { *(WatchPointRegsFile) }    > WATCH_POINT
    EccRegsFile(NOLOAD)           : { *(EccRegsFile) }           > ECC
    EradGlobalRegsFile(NOLOAD)    : { *(EradGlobalRegsFile) }    > ERADGLOBAL
    EradHWBP1RegsFile(NOLOAD)     : { *(EradHWBP1RegsFile) }     > ERADHWBP1
    EradHWBP2RegsFile(NOLOAD)     : { *(EradHWBP2RegsFile) }     > ERADHWBP2
    EradHWBP3RegsFile(NOLOAD)     : { *(EradHWBP3RegsFile) }     > ERADHWBP3
    EradHWBP4RegsFile(NOLOAD)     : { *(EradHWBP4RegsFile) }     > ERADHWBP4
    EradHWBP5RegsFile(NOLOAD)     : { *(EradHWBP5RegsFile) }     > ERADHWBP5
    EradHWBP6RegsFile(NOLOAD)     : { *(EradHWBP6RegsFile) }     > ERADHWBP6
    EradHWBP7RegsFile(NOLOAD)     : { *(EradHWBP7RegsFile) }     > ERADHWBP7
    EradHWBP8RegsFile(NOLOAD)     : { *(EradHWBP8RegsFile) }     > ERADHWBP8
    EradCounter1RegsFile(NOLOAD)  : { *(EradCounter1RegsFile) }  > ERADCOUNTER1
    EradCounter2RegsFile(NOLOAD)  : { *(EradCounter2RegsFile) }  > ERADCOUNTER2
    EradCounter3RegsFile(NOLOAD)  : { *(EradCounter3RegsFile) }  > ERADCOUNTER3
    EradCounter4RegsFile(NOLOAD)  : { *(EradCounter4RegsFile) }  > ERADCOUNTER4
    ClkCfgRegsFile(NOLOAD)        : { *(ClkCfgRegsFile) }        > CLKCFG
    CpuSysRegsFile(NOLOAD)        : { *(CpuSysRegsFile) }        > CPUSYS
    DevCfgRegsFile(NOLOAD)        : { *(DevCfgRegsFile) }        > DEVCFG
    XintRegsFile(NOLOAD)          : { *(XintRegsFile) }          > XINT
    NmiIntruptRegsFile(NOLOAD)    : { *(NmiIntruptRegsFile) }    > NMIINTRUPT
    Dcc0RegsFile(NOLOAD)          : { *(Dcc0RegsFile) }          > DCC0
    GpioCtrlRegsFile(NOLOAD)      : { *(GpioCtrlRegsFile) }      > GPIOCTRL
    GpioDataRegsFile(NOLOAD)      : { *(GpioDataRegsFile) }      > GPIODATA
    InputXbarRegsFile(NOLOAD)     : { *(InputXbarRegsFile) }     > INPUTXBAR
    EPwmXbarRegsFile(NOLOAD)      : { *(EPwmXbarRegsFile) }      > EPWMXBAR
    OutputXbarRegsFile(NOLOAD)    : { *(OutputXbarRegsFile) }    > OUTPUTXBAR
    XbarRegsFile(NOLOAD)          : { *(XbarRegsFile) }          > XBAR
    DmaRegsFile(NOLOAD)           : { *(DmaRegsFile) }           > DMA
    DmaCh1RegsFile(NOLOAD)        : { *(DmaCH1RegsFile) }        > DMACH1
    DmaCh2RegsFile(NOLOAD)        : { *(DmaCH2RegsFile) }        > DMACH2
    DmaCh3RegsFile(NOLOAD)        : { *(DmaCH3RegsFile) }        > DMACH3
    DmaCh4RegsFile(NOLOAD)        : { *(DmaCH4RegsFile) }        > DMACH4
    DmaCh5RegsFile(NOLOAD)        : { *(DmaCH5RegsFile) }        > DMACH5
    DmaCh6RegsFile(NOLOAD)        : { *(DmaCH6RegsFile) }        > DMACH6
    AnalogSubsysRegsFile(NOLOAD)  : { *(AnalogSubsysRegsFile) }  > ANALOGSUBSYS
    AdcaRegsFile(NOLOAD)          : { *(AdcaRegsFile) }          > ADC_A
    AdcaResultRegsFile(NOLOAD)    : { *(AdcaResultRegsFile) }    > ADCARESULT
    AdcbRegsFile(NOLOAD)          : { *(AdcbRegsFile) }          > ADC_B
    AdcbResultRegsFile(NOLOAD)    : { *(AdcbResultRegsFile) }    > ADCBRESULT
    AdccRegsFile(NOLOAD)          : { *(AdccRegsFile) }          > ADC_C
    AdccResultRegsFile(NOLOAD)    : { *(AdccResultRegsFile) }    > ADCCRESULT
    Pga1RegsFile(NOLOAD)          : { *(Pga1RegsFile) }          > PGA1
    Pga2RegsFile(NOLOAD)          : { *(Pga2RegsFile) }          > PGA2
    Pga3RegsFile(NOLOAD)          : { *(Pga3RegsFile) }          > PGA3
    Pga4RegsFile(NOLOAD)          : { *(Pga4RegsFile) }          > PGA4
    Pga5RegsFile(NOLOAD)          : { *(Pga5RegsFile) }          > PGA5
    Pga6RegsFile(NOLOAD)          : { *(Pga6RegsFile) }          > PGA6
    Pga7RegsFile(NOLOAD)          : { *(Pga7RegsFile) }          > PGA7
    DacaRegsFile(NOLOAD)          : { *(DacaRegsFile) }          > DAC_A
    DacbRegsFile(NOLOAD)          : { *(DacbRegsFile) }          > DAC_B
    Cmpss1RegsFile(NOLOAD)        : { *(Cmpss1RegsFile) }        > CMPSS1
    Cmpss2RegsFile(NOLOAD)        : { *(Cmpss2RegsFile) }        > CMPSS2
    Cmpss3RegsFile(NOLOAD)        : { *(Cmpss3RegsFile) }        > CMPSS3
    Cmpss4RegsFile(NOLOAD)        : { *(Cmpss4RegsFile) }        > CMPSS4
    Cmpss5RegsFile(NOLOAD)        : { *(Cmpss5RegsFile) }        > CMPSS5
    Cmpss6RegsFile(NOLOAD)        : { *(Cmpss6RegsFile) }        > CMPSS6
    Cmpss7RegsFile(NOLOAD)        : { *(Cmpss7RegsFile) }        > CMPSS7
    Sdfm1RegsFile(NOLOAD)         : { *(Sdfm1RegsFile) }         > SDFM
    ECap1RegsFile(NOLOAD)         : { *(ECap1RegsFile) }         > ECAP1
    ECap2RegsFile(NOLOAD)         : { *(ECap2RegsFile) }         > ECAP2
    ECap3RegsFile(NOLOAD)         : { *(ECap3RegsFile) }         > ECAP3
    ECap4RegsFile(NOLOAD)         : { *(ECap4RegsFile) }         > ECAP4
    ECap5RegsFile(NOLOAD)         : { *(ECap5RegsFile) }         > ECAP5
    ECap6RegsFile(NOLOAD)         : { *(ECap6RegsFile) }         > ECAP6
    ECap7RegsFile(NOLOAD)         : { *(ECap7RegsFile) }         > ECAP7
    HRCap6RegsFile(NOLOAD)        : { *(HRCap6RegsFile) }        > HRCAP6
    HRCap7RegsFile(NOLOAD)        : { *(HRCap7RegsFile) }        > HRCAP7
    SyncSocRegsFile(NOLOAD)       : { *(SyncSocRegsFile) }       > SYNCSOC
    SFORegsFile(NOLOAD)           : { *(SFORegsFile) }           > SFO
    SFOHHRRegsFile(NOLOAD)        : { *(SFOHHRRegsFile) }        > SFOHHR
    EPwm9RegsFile(NOLOAD)         : { *(EPwm9RegsFile) }         > EPWM9
    EPwm10RegsFile(NOLOAD)        : { *(EPwm10RegsFile) }        > EPWM10
    EPwm11RegsFile(NOLOAD)        : { *(EPwm11RegsFile) }        > EPWM11
    EPwm12RegsFile(NOLOAD)        : { *(EPwm12RegsFile) }        > EPWM12
    EPwm1RegsFile(NOLOAD)         : { *(EPwm1RegsFile) }         > EPWM1
    EPwm2RegsFile(NOLOAD)         : { *(EPwm2RegsFile) }         > EPWM2
    EPwm3RegsFile(NOLOAD)         : { *(EPwm3RegsFile) }         > EPWM3
    EPwm4RegsFile(NOLOAD)         : { *(EPwm4RegsFile) }         > EPWM4
    EPwm5RegsFile(NOLOAD)         : { *(EPwm5RegsFile) }         > EPWM5
    EPwm6RegsFile(NOLOAD)         : { *(EPwm6RegsFile) }         > EPWM6
    EPwm7RegsFile(NOLOAD)         : { *(EPwm7RegsFile) }         > EPWM7
    EPwm8RegsFile(NOLOAD)         : { *(EPwm8RegsFile) }         > EPWM8
    EQep1RegsFile(NOLOAD)         : { *(EQep1RegsFile) }         > EQEP1
    EQep2RegsFile(NOLOAD)         : { *(EQep2RegsFile) }         > EQEP2
    SpiaRegsFile(NOLOAD)          : { *(SpiaRegsFile) }          > SPIA
    SpibRegsFile(NOLOAD)          : { *(SpibRegsFile) }          > SPIB
    SciaRegsFile(NOLOAD)          : { *(SciaRegsFile) }          > SCIA
    ScibRegsFile(NOLOAD)          : { *(ScibRegsFile) }          > SCIB
    I2caRegsFile(NOLOAD)          : { *(I2caRegsFile) }          > I2CA
    PmbusaRegsFile(NOLOAD)        : { *(PmbusaRegsFile) }        > PMBUSA
    LinaRegsFile(NOLOAD)          : { *(LinaRegsFile) }          > LINA
    FsiRxaRegsFile(NOLOAD)        : { *(FsiRxaRegsFile) }        > FSIRXA
    FsiTxaRegsFile(NOLOAD)        : { *(FsiTxaRegsFile) }        > FSITXA
    CanFDaRegsFile(NOLOAD)        : { *(CanFDaRegsFile) }        > CANFDA
    CanFDbRegsFile(NOLOAD)        : { *(CanFDbRegsFile) }        > CANFDB
    HrAdcaRegsFile(NOLOAD)        : { *(HrAdcaRegsFile) }        > HRADC_A
    HrAdcaResultRegsFile(NOLOAD)  : { *(HrAdcaResultRegsFile) }  > HRADCARESULT
    HrAdcbRegsFile(NOLOAD)        : { *(HrAdcbRegsFile) }        > HRADC_B
    HrAdcbResultRegsFile(NOLOAD)  : { *(HrAdcbResultRegsFile) }  > HRADCBRESULT
    HrAdccRegsFile(NOLOAD)        : { *(HrAdccRegsFile) }        > HRADC_C
    HrAdccResultRegsFile(NOLOAD)  : { *(HrAdccResultRegsFile) }  > HRADCCRESULT
    Flash0CtrlRegsFile(NOLOAD)    : { *(Flash0CtrlRegsFile) }    > FLASH0CTRL
    XintfaRegsFile(NOLOAD)        : { *(XintfaRegsFile) }        > XINTFA
}

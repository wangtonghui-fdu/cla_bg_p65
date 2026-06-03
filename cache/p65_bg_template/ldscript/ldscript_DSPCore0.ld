OUTPUT_FORMAT("elf32-tradlittlemips", "elf32-tradbigmips", "elf32-tradlittlemips")

ENTRY(_dsp_start)

INCLUDE "ldscript_Memory.ld"

SECTIONS
{
  __data_start__ = ORIGIN(SRAM_CORE0_DATA);
  . = __data_start__;
  .rodata : { *(.rodata) *(.rodata.*) } > SRAM_CORE0_DATA
  .data   : { *(.data)   *(.data.*)   } > SRAM_CORE0_DATA
  .sdata  : { *(.sdata)  *(.sdata.*)  } > SRAM_CORE0_DATA
  __bss_start = .;
  .sbss   : { *(.sbss) *(.sbss.*) *(.scommon) } > SRAM_CORE0_DATA
  .bss    : { *(.bss)  *(.bss.*)  *(COMMON)   } > SRAM_CORE0_DATA
  __data_end__ = .;

  /* for fake bootloader when debugging on RAM */
  .text.qxbootdebug : {
    KEEP(*(.text.qxboot0debug))
    . = ALIGN(0x10);
  } > BOOT_RAM_CORE0 =0x00000080

  __text_start__ = ORIGIN(SRAM_CORE0_INST);
  . = __text_start__;
  .text : {
    KEEP(*(.text.interrupt.vector))
    KEEP(*(.text.interrupt.routine))
    *(.text)
    *(.text.*)
    . = ALIGN(0x10);
  } > SRAM_CORE0_INST =0x00000080
  __text_end__ = .;

  /*
   * CLA instruction and data
   */
  __cla_data_start__ = ORIGIN(SRAM_CORE0_CLA_DATA);
  . = __cla_data_start__;
  .cla.rodata : { *(.cla_rodata) *(.cla_rodata.*) } > SRAM_CORE0_CLA_DATA
  .cla.data   : { *(.cla_data)   *(.cla_data.*)   } > SRAM_CORE0_CLA_DATA
  __cla_bss_start = .;
  .cla.bss    : { *(.cla_bss)    *(.cla_bss.*)    } > SRAM_CORE0_CLA_DATA
  __cla_data_end__ = .;

  __cla_text_start__ = ORIGIN(SRAM_CORE0_CLA_INST);
  . = __cla_text_start__;
  .cla.text   : {
    KEEP(*(.cla_text.interrupt.vector))
    KEEP(*(.cla_text))
    *(.cla_text.*)
    . = ALIGN(0x10);
  } > SRAM_CORE0_CLA_INST =0x00000080
  __cla_text_end__ = .;
  
  .cla.cpu2cla.data : { KEEP(*(.cpu2cla_data)) } > SRAM_CPU0_2_CLA0
  .cla.cla2cpu.data : { KEEP(*(.cla2cpu_data)) } > SRAM_CLA0_2_CPU0


  PIEVECTTABLE_BASE = ORIGIN(SRAM_CORE0_IVEC);

  PROVIDE(_DSP_STACK_TOP = ORIGIN(SRAM_CORE0_DATA) + LENGTH(SRAM_CORE0_DATA));
  PROVIDE(_CLA_STACK_TOP = ORIGIN(SRAM_CORE0_CLA_DATA) + LENGTH(SRAM_CORE0_CLA_DATA));
  
  PROVIDE(_core0_exp_start     = (ORIGIN(SRAM_CORE0_INST)     >> 15) & 0x3F);
  PROVIDE(_core1_exp_start     = (ORIGIN(SRAM_CORE1_INST)     >> 15) & 0x3F);
  PROVIDE(_core0_cla_exp_start = (ORIGIN(SRAM_CORE0_CLA_INST) >> 15) & 0x3F);

  PROVIDE(__end = __data_end__);
  PROVIDE(__stack_end = ORIGIN(SRAM_CORE0_DATA) + LENGTH(SRAM_CORE0_DATA) - LENGTH(STACK_CORE0));
}

INCLUDE "ldscript_Peripheral.ld"
INCLUDE "ldscript_DebugInfo.ld"

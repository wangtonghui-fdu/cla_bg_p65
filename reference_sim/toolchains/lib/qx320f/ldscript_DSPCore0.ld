OUTPUT_FORMAT("elf32-tradlittlemips", "elf32-tradbigmips", "elf32-tradlittlemips")

INPUT(../../lib/qx320f/startup.o)
INPUT(../../lib/qx320f/_main_chip.o)
ENTRY(_dsp_start)

INCLUDE "../../lib/qx320f/ldscript_Memory.ld"

SECTIONS
{
  __data_start__ = ORIGIN(GSD_RAM_RESERVED);
  . = __data_start__;
  .fill   : { LONG(0xDEADBEEF)        } > GSD_RAM_RESERVED
  .rodata : { *(.rodata) *(.rodata.*) } > GSD_RAM_CORE0_DATA
  .data   : { *(.data)   *(.data.*)   } > GSD_RAM_CORE0_DATA
  .sdata  : { *(.sdata)  *(.sdata.*)  } > GSD_RAM_CORE0_DATA
  __bss_start = .;
  .sbss   : { *(.sbss) *(.sbss.*) *(.scommon) } > GSD_RAM_CORE0_DATA
  .bss    : { *(.bss)  *(.bss.*)  *(COMMON)   } > GSD_RAM_CORE0_DATA
  __data_end__ = .;

  /DISCARD/ : { *(.gnu.warning.*) }

  /* for fake bootloader when debugging on RAM */
  .text.qxbootdebug : {
    KEEP(*(.text.qxbootdebug))
    . = ALIGN(0x10);
  } > BOOT_RAM =0x00000080

  __text_start__ = ORIGIN(GSI_RAM_CORE0);
  . = __text_start__;
  .text : {
    KEEP(*(.text.interrupt.vector))
    KEEP(*(.text.interrupt.routine))
    *(.text)
    *(.text.*)
    . = ALIGN(0x10);
  } > GSI_RAM_CORE0 =0x00000080
  __text_end__ = .;

  PROVIDE(_DSP_STACK_TOP = ORIGIN(GSD_RAM_CORE0_DATA) + LENGTH(GSD_RAM_CORE0_DATA));
  /* symbol names must be in lower case letters if to use them in assembly program to fit linker */
  PROVIDE(_dsp_stack_top_hi = ((_DSP_STACK_TOP >> 16) & 0xFFFF));
  PROVIDE(_dsp_stack_top_lo = ((_DSP_STACK_TOP >>  0) & 0xFFFF));

  PROVIDE(_dsp_bss_start_hi = ((__bss_start  >> 16) & 0xFFFF));
  PROVIDE(_dsp_bss_start_lo = ((__bss_start  >>  0) & 0xFFFF));
  PROVIDE(_dsp_data_end_hi  = ((__data_end__ >> 16) & 0xFFFF));
  PROVIDE(_dsp_data_end_lo  = ((__data_end__ >>  0) & 0xFFFF));

  PIEVECTTABLE_BASE = ORIGIN(GSD_RAM_CORE0_IVEC);
  PROVIDE(pievecttable_base_hi = ((PIEVECTTABLE_BASE >> 16) & 0xFFFF));
  PROVIDE(pievecttable_base_lo = ((PIEVECTTABLE_BASE >>  0) & 0xFFFF));

  PROVIDE(_core0_exp_start = (ORIGIN(GSI_RAM_CORE0) >> 15) & 0x7);
  PROVIDE(_core1_exp_start = (ORIGIN(GSI_RAM_CORE1) >> 15) & 0x7);

  PROVIDE(_CORE0_IRAM_START = ORIGIN(GSI_RAM_CORE0));
  PROVIDE(_CORE1_IRAM_START = ORIGIN(GSI_RAM_CORE1));

  PROVIDE(__end = __data_end__);
  PROVIDE(__stack_end = ORIGIN(GSD_RAM_CORE0_DATA) + LENGTH(GSD_RAM_CORE0_DATA) - LENGTH(STACK_CORE0));
}

INCLUDE "../../lib/qx320f/ldscript_Peripheral.ld"
INCLUDE "../../lib/qx320f/ldscript_DebugInfo.ld"

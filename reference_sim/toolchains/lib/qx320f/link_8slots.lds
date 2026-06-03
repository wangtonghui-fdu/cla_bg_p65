OUTPUT_FORMAT("elf32-dsp")
INPUT(_main_sim.o)
ENTRY(_main)
/*SEARCH_DIR("=/usr/local/lib"); SEARCH_DIR("=/lib"); SEARCH_DIR("=/usr/lib");
*/
SECTIONS
{
  . = 0x00000000 /* + SIZEOF_HEADERS*/;
  /*. = DATA_SEGMENT_ALIGN (CONSTANT (MAXPAGESIZE), CONSTANT (COMMONPAGESIZE));*/
  .rodata : {
    *(.rodata)
  }
  .data : {
    PROVIDE(_fdata = .);
    *(.data)
/*    SORT(CONSTRUCTORS)*/
  }
  . = .;
/*   HIDDEN (_gp = ALIGN (16) + 0x7ff0);*/
   /* .got			: { *(.got) }*/
  .sdata : {
    *(.sdata)
  }
  .lit8 : {
    *(.lit8)
  }
  .lit4 : {
    *(.lit4)
  }
   PROVIDE(_edata  =  .);
   PROVIDE(edata  = .);
   . = .;
   PROVIDE(__bss_start = .);
   PROVIDE(_fbss = .);
   .sbss : {
   *(.sbss)
   *(.scommon)
  }
   .bss : {
   *(.bss)
   *(COMMON)
  }
  PROVIDE(__bss_end = .);
  __end = .;
  
  /* . = STACK SPACE (.);*/
  
  
 /* . = DATA_SEGMENT_END (.);*/
  . = 0x00200000;
  __stack_end = .;
  __exp_end__ = 0x400;
  .text : {
    *(.interrupt)
	. = . + __exp_end__;
   PROVIDE(_ftext = .);
	*(.init)
    /* eprol  =  .;*/
    *(.text)
    *(.fini)
   }
   PROVIDE(etext = .);
   PROVIDE(_etext = .);
   PROVIDE(_end = .);
   PROVIDE(end = .);

  /* DWARF debug sections.
     Symbols in the DWARF debugging sections are relative to the beginning
     of the section so we begin them at 0.  */
  /* DWARF 1 */
  .debug          0 : { *(.debug) }
  .line           0 : { *(.line) }
  /* GNU DWARF 1 extensions */
  .debug_srcinfo  0 : { *(.debug_srcinfo) }
  .debug_sfnames  0 : { *(.debug_sfnames) }
  /* DWARF 1.1 and DWARF 2 */
  .debug_aranges  0 : { *(.debug_aranges) }
  .debug_pubnames 0 : { *(.debug_pubnames) }
  /* DWARF 2 */
  .debug_info     0 : { *(.debug_info .gnu.linkonce.wi.*) }
  .debug_abbrev   0 : { *(.debug_abbrev) }
  .debug_line     0 : { *(.debug_line .debug_line.* .debug_line_end ) }
  .debug_frame    0 : { *(.debug_frame) }
  .debug_str      0 : { *(.debug_str) }
  .debug_loc      0 : { *(.debug_loc) }
  .debug_macinfo  0 : { *(.debug_macinfo) }
  /* SGI/MIPS DWARF 2 extensions */
  .debug_weaknames 0 : { *(.debug_weaknames) }
  .debug_funcnames 0 : { *(.debug_funcnames) }
  .debug_typenames 0 : { *(.debug_typenames) }
  .debug_varnames  0 : { *(.debug_varnames) }
  /* DWARF 3 */
  .debug_pubtypes 0 : { *(.debug_pubtypes) }
  .debug_ranges   0 : { *(.debug_ranges) }
  /* DWARF Extension.  */
  .debug_macro    0 : { *(.debug_macro) }
  .gnu.attributes 0 : { KEEP (*(.gnu.attributes)) }
  .gptab.sdata : { *(.gptab.data) *(.gptab.sdata) }
  .gptab.sbss : { *(.gptab.bss) *(.gptab.sbss) }
  .mdebug.abi32 0 : { KEEP(*(.mdebug.abi32)) }
  .mdebug.abiN32 0 : { KEEP(*(.mdebug.abiN32)) }
  .mdebug.abi64 0 : { KEEP(*(.mdebug.abi64)) }
  .mdebug.abiO64 0 : { KEEP(*(.mdebug.abiO64)) }
  .mdebug.eabi32 0 : { KEEP(*(.mdebug.eabi32)) }
  .mdebug.eabi64 0 : { KEEP(*(.mdebug.eabi64)) }
  .gcc_compiled_long32 0 : { KEEP(*(.gcc_compiled_long32)) }
  .gcc_compiled_long64 0 : { KEEP(*(.gcc_compiled_long64)) }
  /DISCARD/ : { *(.note.GNU-stack) *(.gnu_debuglink) *(.gnu.lto_*) }
}

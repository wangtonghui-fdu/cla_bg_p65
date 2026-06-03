MEMORY
{
  /*
   * Part 1: memory Layout
   */

  /* Data RAM */
  GSD0_RAM         : ORIGIN = 0x00000000, LENGTH = 0x00010000
  GSD1_RAM         : ORIGIN = 0x00010000, LENGTH = 0x00010000
  GSD2_RAM         : ORIGIN = 0x00020000, LENGTH = 0x00010000
  GSD3_RAM         : ORIGIN = 0x00030000, LENGTH = 0x00010000

  /* Instruction RAM */
  GSI0_RAM         : ORIGIN = 0x00200000, LENGTH = 0x00010000
  GSI1_RAM         : ORIGIN = 0x00210000, LENGTH = 0x00010000
  GSI2_RAM         : ORIGIN = 0x00220000, LENGTH = 0x00010000
  GSI3_RAM         : ORIGIN = 0x00230000, LENGTH = 0x00010000

  /* RAM for bootloader */
  BOOT_RAM         : ORIGIN = 0x00280000, LENGTH = 0x00002000

  /* Flash Memory: store instruction and data, and copy to RAM by bootloader */
  FLASH_DATA       : ORIGIN = 0x30000000, LENGTH = 0x00100000


  /*
   * Part 2:  application symbols and notes
   */

  /* 1. GSD_RAM is allocated by 64KB blocks (0x10000)
   * 2. Allocate all GSD_RAM to CORE0 is allowed, if not using CORE1
   * 3. Reserve last 4KB of GSD_RAM of each CORE for interrupt vector
   * 4. Reserve 4 bytes at address 0x0 to support comparison with NULL pointer
   */
  GSD_RAM_RESERVED   : ORIGIN = 0x00000000, LENGTH = 0x00000004
  GSD_RAM_CORE0_DATA : ORIGIN = 0x00000004, LENGTH = 0x0001FBFC
  GSD_RAM_CORE0_IVEC : ORIGIN = 0x0001FC00, LENGTH = 0x00000400
  GSD_RAM_CORE1_DATA : ORIGIN = 0x00020000, LENGTH = 0x0001FC00
  GSD_RAM_CORE1_IVEC : ORIGIN = 0x0003FC00, LENGTH = 0x00000400

  /* 1. CORE1 instruction space MUST start from GSI0_RAM (address 0x00200000)
   * 2. GSI_RAM is allocated by 64KB blocks (0x10000)
   * 3. Allocate all GSI_RAM to CORE0 is allowed, if not using CORE1
   */
  GSI_RAM_CORE0    : ORIGIN = 0x00200000, LENGTH = 0x00040000
  GSI_RAM_CORE1    : ORIGIN = 0x00200000, LENGTH = 0x00000000

  /* Fake memory regions for specifying stack size */
  STACK_CORE0      : ORIGIN = 0x00000000, LENGTH = 0x00000400
  STACK_CORE1      : ORIGIN = 0x00000000, LENGTH = 0x00000400
}

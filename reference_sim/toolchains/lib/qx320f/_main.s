.extern _main
.extern main
.section .text
.global _main
_main:
movigl gr30 0x0||
movigh gr30 0x20||
movigh gr31 0x2f||
movigl gr31 0xfff0||
addi gr30 gr30 0xfe00||
||store32 gr31 gr30 0x7f
call main||
nop||
nop||
|load32 gr31 gr30 0x7f|
addi gr30 gr30 0x200||
ret||
nop||
nop||
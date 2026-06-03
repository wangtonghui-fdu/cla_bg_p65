.data


mydata:
.byte 0x00

.text
.globl  main
.type   main, @function            

main:

movigl GR1 0x0128||
movigh GR1 0x0107||
movigl GR2 0x0000||
movigh GR2 0x0000||
||store32 GR2 GR1 0x0000
movg2c GR2||

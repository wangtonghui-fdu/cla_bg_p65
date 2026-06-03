import binascii
import sys
import  subprocess as sp
import os
from pathlib import Path


#FIXME: rewrite this script
path = Path(sys.argv[2])
a = os.getcwd()
sourceFile = sys.argv[1]

print("source:",sourceFile)
if os.path.isfile(sourceFile) == False:
    print(sourceFile + " doesn't exist!",file=sys.stderr)
    os._exit(1)

objcopy_name="objcopy.exe" if sys.platform.startswith("win") else "objcopy.bin"
mipsel = str((path/objcopy_name).absolute())

print("objcopy:",mipsel)
if os.path.isfile(mipsel) == False:
    print(mipsel + " doesn't exist!",file=sys.stderr)
    os._exit(2)

outFile = sourceFile[:-4] + ".out"
datFileSim = sourceFile[:-4]
datFileRtl = sourceFile[:-4] + ".dat"

#os.system("mipsel-linux-objcopy -O binary "+ outFile + " " + datFileSim)
cmd = ["-O", "binary", outFile ,datFileSim]
sp.check_call([mipsel,*cmd])
if os.path.isfile(datFileSim) == False:
    print("Doesn't create "+datFileSim,file=sys.stderr)
    os._exit(1)
fb_s = open(datFileSim,'rb')
fb_d = open(datFileRtl,'w')

#process data segment
#1)a line in data segment file has 4 words (32bits per word),such as 1 2 3 4 ,reverse it to 4 3 2 1
#2)if encountering 9 consecutive 0 line in data segment
#  ignoring the left part of data segment
zero_count = 0
for i in range(0,65536*2):
    insnPack = fb_s.read(16)
    if(len(insnPack) != 16):
        break
#    if(insnPack == "0000000000000000"):
#        continue
    insnPack = binascii.b2a_hex(insnPack)
    if(insnPack == "00000000000000000000000000000000"):
        zero_count += 1
    else:
        zero_count = 0
#  do not print following zero lines after encounter 9 consecutive zero lines
#  but still reading and counting until a non-zero line, where clear zero_count
#  and restart print.
    if(zero_count > 9):
        continue
    insn0 = insnPack[0:8]
    insn1 = insnPack[8:16]
    insn2 = insnPack[16:24]
    insn3 = insnPack[24:32]
#    if(insn0 == "00000000" and insn1 == "00000000" and insn2 == "00000000" and insn3 == "00000000"):
#        continue
    insn0 = insn0[6:8]+insn0[4:6]+insn0[2:4]+insn0[0:2] + b'\n'
    insn1 = insn1[6:8]+insn1[4:6]+insn1[2:4]+insn1[0:2] + b'_'
    insn2 = insn2[6:8]+insn2[4:6]+insn2[2:4]+insn2[0:2] + b'_'
    insn3 = insn3[6:8]+insn3[4:6]+insn3[2:4]+insn3[0:2] + b'_'
    addr =  '{0:0>4}'.format(hex(i).replace("0x",''))
    #i#fb_d.write(addr + '\n')
    fb_d.write("32'h000" + addr + '0,\t' + "128'h" + insn3.decode() + insn2.decode() + insn1.decode() + insn0.decode())

#process code segment
#a line in code segment file has 4 instructions(32bits per instruction) so that 16 char (32 hexes) per line,
#reversing the sequence of 4 bytes in a instruction for the sake of transform little-endian to Big-endian,
#such as 0x12345678 switched to 0x78563412.
for i in range(0,32768):
    insnPack = fb_s.read(16)
    if(len(insnPack) != 16):
        break
    insnPack = binascii.b2a_hex(insnPack)
    insn0 = insnPack[0:8]
    insn1 = insnPack[8:16]
    insn2 = insnPack[16:24]
    insn3 = insnPack[24:32]
    insn0 = insn0[6:8]+insn0[4:6]+insn0[2:4]+insn0[0:2] + b'_'
    insn1 = insn1[6:8]+insn1[4:6]+insn1[2:4]+insn1[0:2] + b'_'
    insn2 = insn2[6:8]+insn2[4:6]+insn2[2:4]+insn2[0:2] + b'_'
    insn3 = insn3[6:8]+insn3[4:6]+insn3[2:4]+insn3[0:2] + b'\n'
    addr =  '{0:0>4}'.format(hex(i).replace("0x",''))
    #i#fb_d.write(addr + '\n')
    fb_d.write("32'h002" + addr + '0,\t' + "128'h" + insn0.decode() + insn1.decode() + insn2.decode() + insn3.decode())

insnPack = binascii.b2a_hex(insnPack)
if(len(insnPack) == 8):
    insn0 = insnPack[0:8]
    insn0 = insn0[6:8]+insn0[4:6]+insn0[2:4]+insn0[0:2] + b'_'
    insn3 = '80000000'
    addr =  '{0:0>4}'.format(hex(i).replace("0x",''))
    fb_d.write("32'h002" + addr + '0,\t' + "128'h" + insn0.decode() + insn3 + '_' + insn3 + '_' + insn3 + '\n')
elif(len(insnPack) == 16):
    insn0 = insnPack[0:8]
    insn1 = insnPack[8:16]
    insn0 = insn0[6:8]+insn0[4:6]+insn0[2:4]+insn0[0:2] + b'_'
    insn1 = insn1[6:8]+insn1[4:6]+insn1[2:4]+insn1[0:2] + b'_'
    insn3 = '80000000'
    addr =  '{0:0>4}'.format(hex(i).replace("0x",''))
    fb_d.write("32'h002" + addr + '0,\t' + "128'h" + insn0.decode() + insn1.decode() + insn3 + '_' + insn3 + '\n')
elif(len(insnPack) == 24):
    insn0 = insnPack[0:8]
    insn1 = insnPack[8:16]
    insn2 = insnPack[16:24]
    insn0 = insn0[6:8]+insn0[4:6]+insn0[2:4]+insn0[0:2] + b'_'
    insn1 = insn1[6:8]+insn1[4:6]+insn1[2:4]+insn1[0:2] + b'_'
    insn2 = insn2[6:8]+insn2[4:6]+insn2[2:4]+insn2[0:2] + b'_'
    insn3 = '80000000'
    addr =  '{0:0>4}'.format(hex(i).replace("0x",''))
    fb_d.write("32'h002" + addr + '0,\t' + "128'h" + insn0.decode() + insn1.decode() + insn2.decode() + insn3 + '\n')
elif(len(insnPack) != 0):
    print('error in length of instructions !')

fb_s.close()
fb_d.close()

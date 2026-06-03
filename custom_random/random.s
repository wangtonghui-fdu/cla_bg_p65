.global start
_begin:
start:
.text
#.ent main

boot:
.=1024


movigl GR1 0x0128||
movigh GR1 0x0107||
movigl GR2 0x0000||
movigh GR2 0x0000||
||store32 GR2 GR1 0x0000
movg2c GR2||



movigl GR24 0xBD38||
movigh GR24 0xBAD3||
movigl GR16 0xF1F3||
movigh GR16 0xC341||

#pc = 0x00030428  
movigl GR24 0xFF8C||
movigh GR24 0xFFFF||
movigl GR16 0xFF8C||
movigh GR16 0xFFFF||

#pc = 0x00030438  
le GR24 GR16||
testi GR16 0x0c||
movigl GR19 0x0F82||
movigh GR19 0x0005||

#pc = 0x00030448  
movigl GR9 0x6BA6||store8 GR24 GR19 0x08B
movigh GR9 0x0005|load8 GR5 GR19 0x08B|
movigl GR16 0x4001||
movigh GR16 0x0000||

#pc = 0x00030460  
movg2c GR16||
subc GR15 GR24 GR16||
fslt GR14 GR6||store8 GR15 GR9 0x194
ltu GR16 GR24||

#pc = 0x00030474  
movigl GR10 0xAB42||
movigh GR10 0x0003||
movigl GR3 0x5ED1||store16 GR16 GR10 0x0C1
movigh GR3 0x0005|loadu16 GR24 GR10 0x0C1|

#pc = 0x0003048C  
testi GR16 0x04||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR2||

#pc = 0x000304BC  
movigl GR2 0x0001||
movigh GR2 0x0000||
movigl GR16 0x4000||
movigh GR16 0x0000||

#pc = 0x000304CC  
movg2c GR16||storeu8 GR16 GR3 0x004
movigl GR16 0xA2CD||
movigh GR16 0x51A6||
movigl GR2 0xA2CD||

#pc = 0x000304E0  
movigh GR2 0x51A6||
fsle GR16 GR2||
ltu GR16 GR15||
movigl GR18 0x5AD0||

#pc = 0x000304F0  
movigh GR18 0x0007||
addi GR16 GR22 0x169||
movigl GR25 0x3078||store32 GR16 GR18 0x16E
movigh GR25 0x0005|load32 GR1 GR18 0x16E|

#pc = 0x00030508  
||store8 GR2 GR25 0x046
movigl GR16 0x14C4||
movigh GR16 0xA113||
fseisqrt GR22 GR16||

#pc = 0x00030518  
max GR15 GR15 GR2||
movigl GR8 0xFF6B||
movigh GR8 0xFFFF||
neqi GR8 0x193||

#pc = 0x00030528  
movigl GR17 0x4001||
movigh GR17 0x0000||
movg2c GR17||
addi GR8 GR7 0x27f||

#pc = 0x00030538  
cbw GR7 GR8||
movigl GR4 0xC940||
movigh GR4 0x0007||
movigl GR8 0x76D0||store32 GR8 GR4 0x160

#pc = 0x0003054C  
movigh GR8 0xA02D|loadu32 GR7 GR4 0x160|
movigl GR14 0x7844||
movigh GR14 0x5FD6||
add GR11 GR8 GR14||fsdiv GR20 GR22 GR16

#pc = 0x00030564  
and GR29 GR8 GR14||store8 GR8 GR11 0x14D
bfextu GR22 GR8 0x1f 0x0a||
movigl GR8 0x004B||
movigh GR8 0x0000||

#pc = 0x00030578  
neqi GR8 0x0b5||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR13||

#pc = 0x000305A8  
movigl GR13 0x0001||
movigh GR13 0x0000||
movigl GR22 0x4000||
movigh GR22 0x0000||

#pc = 0x000305B8  
movg2c GR22||
movigl GR8 0x426B||
movigh GR8 0x0FC6||
movigl GR22 0x426B||

#pc = 0x000305C8  
movigh GR22 0x0FC6||
neq GR8 GR22||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x000305FC  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x0003060C  
movg2c GR19||
movigl GR6 0xE002||
movigh GR6 0x1D3D||
movigl GR2 0x9340||

#pc = 0x0003061C  
movigh GR2 0xE2C8||
add GR27 GR6 GR2||
bclr GR6 0x1b||store16 GR27 GR27 0x18E
movigl GR10 0xFFF3|load16 GR8 GR27 0x18E|

#pc = 0x00030634  
movigh GR10 0x0003||fsmac GR28 GR2 GR6
subc GR13 GR2 GR6||store8 GR2 GR10 0x197
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR9||

#pc = 0x00030670  
movigl GR9 0x0001||
movigh GR9 0x0000||
movigl GR29 0x4000||
movigh GR29 0x0000||

#pc = 0x00030680  
movg2c GR29||
movigl GR13 0x4001||
movigh GR13 0x0000||
movg2c GR13||

#pc = 0x00030690  
addi GR9 GR1 0x2e8||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR16||

#pc = 0x000306C0  
movigl GR16 0x0001||
movigh GR16 0x0000||
movigl GR29 0x4000||
movigh GR29 0x0000||

#pc = 0x000306D0  
movg2c GR29||
leu GR16 GR15||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR15||

#pc = 0x00030704  
movigl GR15 0x0001||
movigh GR15 0x0000||
movigl GR13 0x4000||
movigh GR13 0x0000||

#pc = 0x00030714  
movg2c GR13||
addic GR22 GR23 0x4ca||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR17||

#pc = 0x00030748  
movigl GR17 0x0001||
movigh GR17 0x0000||
movigl GR16 0x4000||
movigh GR16 0x0000||

#pc = 0x00030758  
movg2c GR16||
movigl GR19 0x22F0||
movigh GR19 0x0007||
movigl GR26 0x8701||store32 GR22 GR19 0x081

#pc = 0x0003076C  
movigh GR26 0xE391|loadu32 GR9 GR19 0x081|
movigl GR6 0xF9C5||
movigh GR6 0xE38A||
sub GR25 GR26 GR6||

#pc = 0x00030780  
sub GR21 GR6 GR16||
movigl GR6 0x3B1B||store8 GR21 GR25 0x0D3
movigh GR6 0xB470||
movigl GR26 0xD021||

#pc = 0x00030794  
movigh GR26 0xBA37||
fsdiv GR12 GR6 GR26||
max GR22 GR18 GR7||
movigl GR3 0x0062||

#pc = 0x000307A4  
movigh GR3 0x0000||
lei GR3 0x1cf||
bfst GR7 GR12 0x1e 0x13||
xor GR8 GR3 GR12||

#pc = 0x000307B4  
movigl GR7 0x3430||
movigh GR7 0x0004||
movigl GR5 0xC885||store16 GR3 GR7 0x018
movigh GR5 0x0003|load16 GR13 GR7 0x018|fsabs GR6 GR1

#pc = 0x000307D0  
movigl GR21 0x0301||storeu8 GR3 GR5 0x02d
movigh GR21 0x05D2||
movigl GR22 0x0301||
movigh GR22 0x05D2||

#pc = 0x000307E4  
ltu GR21 GR22||
movigl GR4 0x00C7||
movigh GR4 0x0000||
lti GR4 0x1bc||

#pc = 0x000307F4  
add GR16 GR22 GR6||
movigl GR24 0x0005||
movigh GR24 0x0000||
sra GR8 GR6 GR24||

#pc = 0x00030804  
movigl GR14 0x19B4||
movigh GR14 0x5975||
movigl GR17 0x840D||
movigh GR17 0x5970||

#pc = 0x00030814  
xor GR6 GR14 GR17||
movigl GR11 0x4001||
movigh GR11 0x0000||
movg2c GR11||

#pc = 0x00030824  
addic GR17 GR18 0x7e3||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00030854  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR28 0x4000||
movigh GR28 0x0000||

#pc = 0x00030864  
movg2c GR28||store8 GR28 GR6 0x1E8
movigl GR16 0x0464|loadu8 GR8 GR6 0x1E8|
movigh GR16 0x0007||fsmac GR4 GR28 GR10
movigl GR18 0x362A||storeu32 GR28 GR16 0x03c

#pc = 0x00030884  
movigh GR18 0x44F0||
movigl GR28 0x362A||
movigh GR28 0x44F0||
le GR18 GR28||

#pc = 0x00030894  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR24||

#pc = 0x000308C0  
movigl GR24 0x0001||
movigh GR24 0x0000||
movigl GR20 0x4000||
movigh GR20 0x0000||

#pc = 0x000308D0  
movg2c GR20||
addi GR4 GR21 0x12e||
movigl GR19 0x0141||
movigh GR19 0x0000||

#pc = 0x000308E0  
lti GR19 0x14f||
movigl GR11 0x000A||
movigh GR11 0x0000||
gei GR11 0x041||

#pc = 0x000308F0  
movigl GR25 0xB256||
movigh GR25 0x0006||
movigl GR27 0x389A||store16 GR20 GR25 0x10C
movigh GR27 0x07ED|load16 GR23 GR25 0x10C|

#pc = 0x00030908  
movigl GR26 0xAFAA||
movigh GR26 0x07E5||
sub GR29 GR27 GR26||
fslt GR28 GR22||storeu16 GR19 GR29 0x076

#pc = 0x0003091C  
leu GR26 GR27||
addi GR26 GR24 0x030||
movigl GR2 0x818B||
movigh GR2 0x0003||

#pc = 0x0003092C  
movigl GR19 0xD7FE||store8 GR26 GR2 0x1D6
movigh GR19 0xFE73|loadu8 GR4 GR2 0x1D6|
movigl GR18 0xFCBD||
movigh GR18 0x018F||

#pc = 0x00030944  
and GR10 GR19 GR18||
movigl GR12 0xB35E||store32 GR26 GR10 0x13A
movigh GR12 0x3B55||
fseisqrt GR26 GR12||

#pc = 0x00030958  
gt GR12 GR19||
gtu GR18 GR19||
movigl GR13 0x0018||
movigh GR13 0x0000||

#pc = 0x00030968  
sl GR3 GR19 GR13||
movigl GR1 0x00B7||
movigh GR1 0x0000||
lti GR1 0x018||

#pc = 0x00030978  
movigl GR15 0x926E||
movigh GR15 0x0006||
movigl GR6 0xD277||store16 GR1 GR15 0x06F
movigh GR6 0x0007|loadu16 GR17 GR15 0x06F|

#pc = 0x00030990  
addi GR1 GR13 0x044||
fseq GR14 GR26||storeu8 GR1 GR6 0x142
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR20||

#pc = 0x000309C8  
movigl GR20 0x0001||
movigh GR20 0x0000||
movigl GR18 0x4000||
movigh GR18 0x0000||

#pc = 0x000309D8  
movg2c GR18||
movigl GR7 0x001F||
movigh GR7 0x0000||
sra GR20 GR19 GR7||

#pc = 0x000309E8  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR5||

#pc = 0x00030A14  
movigl GR5 0x0001||
movigh GR5 0x0000||
movigl GR11 0x4000||
movigh GR11 0x0000||

#pc = 0x00030A24  
movg2c GR11||
movigl GR7 0xFF91||
movigh GR7 0xFFFF||
movigl GR18 0xC991||

#pc = 0x00030A34  
movigh GR18 0x3964||
neq GR7 GR18||
eq GR24 GR11||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR1||

#pc = 0x00030A6C  
movigl GR1 0x0001||
movigh GR1 0x0000||
movigl GR7 0x4000||
movigh GR7 0x0000||

#pc = 0x00030A7C  
movg2c GR7||
movigl GR9 0xFFAE||
movigh GR9 0xFFFF||
gti GR9 0x121||

#pc = 0x00030A8C  
movigl GR26 0xDB3D||
movigh GR26 0x0005||
sub GR11 GR1 GR7||
movigl GR9 0x6836||store8 GR11 GR26 0x11F

#pc = 0x00030AA0  
movigh GR9 0x0006|loadu8 GR4 GR26 0x11F|
test GR12 GR7||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00030AD8  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR23 0x4000||
movigh GR23 0x0000||

#pc = 0x00030AE8  
movg2c GR23||store8 GR23 GR9 0x1A6
movigl GR8 0xB79C||
movigh GR8 0x621B||
fsabs GR24 GR8||

#pc = 0x00030AFC  
leu GR8 GR23||
ge GR8 GR23||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR18||

#pc = 0x00030B30  
movigl GR18 0x0001||
movigh GR18 0x0000||
movigl GR12 0x4000||
movigh GR12 0x0000||

#pc = 0x00030B40  
movg2c GR12||
subc GR8 GR8 GR12||
lt GR12 GR24||
movigl GR14 0x76E7||

#pc = 0x00030B50  
movigh GR14 0x0007||
addi GR24 GR21 0x071||
movigl GR3 0x483C||store8 GR24 GR14 0x027
movigh GR3 0x0007|loadu8 GR16 GR14 0x027|

#pc = 0x00030B68  
and GR10 GR25 GR24||
||store8 GR10 GR3 0x1D9
movigl GR24 0xE127||
movigh GR24 0x3C01||

#pc = 0x00030B78  
fcvtsf GR27 GR24||
and GR8 GR29 GR6||
max GR22 GR19 GR13||
movigl GR1 0x9501||

#pc = 0x00030B88  
movigh GR1 0x5B80||
movigl GR21 0xE4B9||
movigh GR21 0x5B79||
sub GR22 GR1 GR21||

#pc = 0x00030B98  
addic GR21 GR11 0x057||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR10||

#pc = 0x00030BC8  
movigl GR10 0x0001||
movigh GR10 0x0000||
movigl GR5 0x4000||
movigh GR5 0x0000||

#pc = 0x00030BD8  
movg2c GR5||store16 GR5 GR22 0x116
movigl GR15 0x1749|load16 GR18 GR22 0x116|
movigh GR15 0x0007||
addi GR13 GR15 0x32A||fseisqrt GR1 GR27

#pc = 0x00030BF4  
movigl GR25 0x00DA||storeu8 GR10 GR13 0x13a
movigh GR25 0x0000||
gei GR25 0x19e||
movigl GR7 0x380A||

#pc = 0x00030C08  
movigh GR7 0xB1DA||
movigl GR24 0xBBA5||
movigh GR24 0x4E29||
add GR7 GR7 GR24||

#pc = 0x00030C18  
movigl GR28 0xF9E2||store8 GR15 GR7 0x19F
movigh GR28 0x0007|load8 GR11 GR7 0x19F|
movigl GR1 0xC1E7||storeu8 GR24 GR28 0x074
movigh GR1 0x6BF1||

#pc = 0x00030C34  
fcvtsf GR6 GR1||
addc GR24 GR1 GR12||
and GR20 GR23 GR1||
movigl GR20 0x4001||

#pc = 0x00030C44  
movigh GR20 0x0000||
movg2c GR20||
addi GR6 GR15 0x289||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR17||

#pc = 0x00030C7C  
movigl GR17 0x0001||
movigh GR17 0x0000||
movigl GR1 0x4000||
movigh GR1 0x0000||

#pc = 0x00030C8C  
movg2c GR1||
movigl GR6 0x0000||
movigh GR6 0x0000||
movg2c GR6||

#pc = 0x00030C9C  
movigl GR3 0x6B27||
movigh GR3 0xCBFD||
movigl GR10 0xAB9D||
movigh GR10 0xCBF5||

#pc = 0x00030CAC  
subc GR16 GR3 GR10||
abs GR9 GR3||
movigl GR23 0xF5FA||store16 GR9 GR16 0x1C9
movigh GR23 0xC717|loadu16 GR5 GR16 0x1C9|

#pc = 0x00030CC4  
movigl GR14 0xBB3F||
movigh GR14 0x38ED||
and GR25 GR23 GR14||
fsge GR17 GR2||storeu16 GR10 GR25 0x12a

#pc = 0x00030CD8  
or GR14 GR4 GR23||
movigl GR4 0x0002||
movigh GR4 0x0000||
sra GR6 GR18 GR4||

#pc = 0x00030CE8  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR29||

#pc = 0x00030D14  
movigl GR29 0x0001||
movigh GR29 0x0000||
movigl GR15 0x4000||
movigh GR15 0x0000||

#pc = 0x00030D24  
movg2c GR15||
add GR27 GR10 GR15||
movigl GR7 0x2761||
movigh GR7 0x1E32||

#pc = 0x00030D34  
movigl GR26 0xA089||
movigh GR26 0x1E34||
xor GR15 GR7 GR26||
movigl GR17 0x2A1A||store16 GR21 GR15 0x017

#pc = 0x00030D48  
movigh GR17 0x0004|loadu16 GR10 GR15 0x017|
movigl BAR3 0x29F0||
movigh BAR3 0x0004||
movigl MR3 0x0062||

#pc = 0x00030D5C  
movigh MR3 0x0000||
movigl OFF3 0x000E||
movigh OFF3 0x0000||
movigl GR18 0x4001||storeo16 GR13 GR17 BAR3

#pc = 0x00030D70  
movigh GR18 0x0000||
movg2c GR18||
add GR11 GR29 GR11||
or GR9 GR18 GR24||storeo16 GR11 GR17 BAR3

#pc = 0x00030D84  
not GR3 GR20||storeo16 GR18 GR17 BAR3
movigl GR12 0x5A14||storeo16 GR9 GR17 BAR3
movigh GR12 0xFFA6||storeo16 GR8 GR17 BAR3
movigl GR29 0x5A14||storeo16 GR11 GR17 BAR3

#pc = 0x00030DA4  
movigh GR29 0xFFA6||storeo16 GR3 GR17 BAR3
fsge GR12 GR29||
ltu GR12 GR29||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR18||

#pc = 0x00030DE0  
movigl GR18 0x0001||
movigh GR18 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x00030DF0  
movg2c GR9||
movigl GR12 0xC0DD||
movigh GR12 0x64EC||
movigl GR9 0xC0DD||

#pc = 0x00030E00  
movigh GR9 0x64EC||
le GR12 GR9||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR22||

#pc = 0x00030E34  
movigl GR22 0x0001||
movigh GR22 0x0000||
movigl GR3 0x4000||
movigh GR3 0x0000||

#pc = 0x00030E44  
movg2c GR3||
movigl GR29 0x4968||
movigh GR29 0x0006||
movigl GR14 0x4034||store32 GR9 GR29 0x011

#pc = 0x00030E58  
movigh GR14 0x0007|load32 GR2 GR29 0x011|
movigl GR11 0x000B||
movigh GR11 0x0000||
sra GR20 GR7 GR11||

#pc = 0x00030E6C  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR5||

#pc = 0x00030E98  
movigl GR5 0x0001||
movigh GR5 0x0000||
movigl GR4 0x4000||
movigh GR4 0x0000||

#pc = 0x00030EA8  
movg2c GR4||storeu16 GR4 GR14 0x03d
movigl GR13 0x7C47||
movigh GR13 0x1F49||
fseq GR27 GR13||

#pc = 0x00030EBC  
movigl GR27 0x0004||
movigh GR27 0x0000||
srl GR15 GR5 GR27||
movigl GR12 0xFF82||

#pc = 0x00030ECC  
movigh GR12 0xFFFF||
eqi GR12 0x194||
eq GR1 GR27||
gtu GR12 GR27||

#pc = 0x00030EDC  
movigl GR20 0xB048||
movigh GR20 0x0003||
movigl BAR0 0xB03C||
movigh BAR0 0x0003||

#pc = 0x00030EEC  
movigl MR0 0x0018||
movigh MR0 0x0000||
movigl OFF0 0x0004||
movigh OFF0 0x0000||

#pc = 0x00030EFC  
addic GR12 GR13 0x72e||storeo32 GR12 GR20 BAR0
movigl GR11 0x4001||storeo32 GR12 GR20 BAR0
movigh GR11 0x0000||
movg2c GR11||

#pc = 0x00030F14  
sub GR5 GR11 GR12||
or GR17 GR6 GR11||storeo32 GR5 GR20 BAR0
movigl GR22 0x4000||storeo32 GR17 GR20 BAR0
movigh GR22 0x0000||

#pc = 0x00030F2C  
movg2c GR22||
subc GR7 GR11 GR15||
subc GR21 GR25 GR22||storeo32 GR7 GR20 BAR0
movigl GR23 0xB048||storeo32 GR21 GR20 BAR0

#pc = 0x00030F44  
movigh GR23 0x0003||
movigl GR13 0x0CF4|loado32 GR9 GR23 BAR0|
movigh GR13 0x0004|loado32 GR9 GR23 BAR0|
movigl GR19 0x0000|loado32 GR9 GR23 BAR0|

#pc = 0x00030F60  
movigh GR19 0x0000|loado32 GR9 GR23 BAR0|
or GR22 GR13 GR19|loado32 GR9 GR23 BAR0|
min GR24 GR28 GR19|loado32 GR9 GR23 BAR0|
movigl GR19 0xE148||storeu16 GR24 GR22 0x1b8

#pc = 0x00030F80  
movigh GR19 0x57BF||
movigl GR8 0x717F||
movigh GR8 0xD76E||
fsadd GR13 GR19 GR8||

#pc = 0x00030F90  
le GR7 GR19||
testi GR14 0x0c||
movigl GR18 0x0003||
movigh GR18 0x0000||

#pc = 0x00030FA0  
lei GR18 0x003||
movigl GR8 0x7C83||
movigh GR8 0x6F7B||
movigl GR6 0x7C83||

#pc = 0x00030FB0  
movigh GR6 0x6F7B||
le GR8 GR6||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00030FE4  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x00030FF4  
movg2c GR19||
movigl GR28 0xE37D||
movigh GR28 0x0004||
add GR18 GR6 GR29||

#pc = 0x00031004  
movigl GR15 0xB789||store8 GR18 GR28 0x1F7
movigh GR15 0x337C|loadu8 GR11 GR28 0x1F7|
movigl GR7 0xDB76||
movigh GR7 0xCC87||

#pc = 0x0003101C  
and GR15 GR15 GR7||
||storeu32 GR19 GR15 0x0dc
movigl GR10 0x1085||
movigh GR10 0xD006||

#pc = 0x0003102C  
movigl GR13 0x1CA6||
movigh GR13 0xB8BE||
movigl GR10 0x144F||
movigh GR10 0x2FB7||

#pc = 0x0003103C  
fsmax GR1 GR13 GR10||
gtu GR13 GR10||
movigl GR7 0x0E08||
movigh GR7 0x7A51||

#pc = 0x0003104C  
movigl GR10 0x0E08||
movigh GR10 0x7A51||
neq GR7 GR10||
testi GR16 0x0d||

#pc = 0x0003105C  
xor GR25 GR1 GR13||
movigl GR2 0xEBB7||
movigh GR2 0x0006||
movigl GR3 0x4000||

#pc = 0x0003106C  
movigh GR3 0x0000||
movg2c GR3||
addic GR10 GR18 0x392||
movigl GR9 0xD744||store8 GR10 GR2 0x1D3

#pc = 0x00031080  
movigh GR9 0x0006|loadu8 GR21 GR2 0x1D3|
movigl GR20 0x0340||
movigh GR20 0x0004||
or GR24 GR9 GR20||

#pc = 0x00031094  
||store8 GR10 GR24 0x198
movigl GR13 0x7CE3||
movigh GR13 0xB50B||
movigl GR6 0x167C||

#pc = 0x000310A4  
movigh GR6 0x4286||
movigl GR1 0xCD53||
movigh GR1 0x4D45||
movigl GR13 0x6A55||

#pc = 0x000310B4  
movigh GR13 0x316E||
fsmac GR6 GR1 GR13||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR9||

#pc = 0x000310E8  
movigl GR9 0x0001||
movigh GR9 0x0000||
movigl GR5 0x4000||
movigh GR5 0x0000||

#pc = 0x000310F8  
movg2c GR5||
movigl GR13 0x00A6||
movigh GR13 0x0000||
lti GR13 0x0e4||

#pc = 0x00031108  
gt GR6 GR1||
movigl GR6 0x39A9||
movigh GR6 0x041E||
movigl GR5 0xFFA9||

#pc = 0x00031118  
movigh GR5 0xFFFF||
le GR6 GR5||
or GR28 GR5 GR13||
movigl GR22 0x7CF3||

#pc = 0x00031128  
movigh GR22 0x74C7||
movigl GR27 0x4EA3||
movigh GR27 0x74C3||
xor GR9 GR22 GR27||

#pc = 0x00031138  
movigl GR14 0x00A4||store8 GR6 GR9 0x0C1
movigh GR14 0x0006|load8 GR7 GR9 0x0C1|fsadd GR12 GR27 GR22
nop||storeu8 GR22 GR14 0x13d
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR17||

#pc = 0x0003117C  
movigl GR17 0x0001||
movigh GR17 0x0000||
movigl GR15 0x4000||
movigh GR15 0x0000||

#pc = 0x0003118C  
movg2c GR15||
or GR5 GR17 GR12||
geu GR17 GR15||
movigl GR16 0x4000||

#pc = 0x0003119C  
movigh GR16 0x0000||
movg2c GR16||
subc GR29 GR15 GR17||
add GR11 GR15 GR16||

#pc = 0x000311AC  
movigl GR25 0xFD84||
movigh GR25 0x0005||
movigl GR29 0x24EE||store32 GR15 GR25 0x1EC
movigh GR29 0x0007|loadu32 GR10 GR25 0x1EC|

#pc = 0x000311C4  
abs GR2 GR3||
fsmin GR3 GR2 GR23||storeu8 GR2 GR29 0x05a
movigl GR12 0x4001||
movigh GR12 0x0000||

#pc = 0x000311D8  
movg2c GR12||
addic GR2 GR22 0x628||
movigl GR24 0x0003||
movigh GR24 0x0000||

#pc = 0x000311E8  
sra GR18 GR3 GR24||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR2||

#pc = 0x00031218  
movigl GR2 0x0001||
movigh GR2 0x0000||
movigl GR21 0x4000||
movigh GR21 0x0000||

#pc = 0x00031228  
movg2c GR21||
sub GR1 GR2 GR24||
movigl GR4 0x015F||
movigh GR4 0x0000||

#pc = 0x00031238  
lei GR4 0x15f||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR3||

#pc = 0x00031268  
movigl GR3 0x0001||
movigh GR3 0x0000||
movigl GR2 0x4000||
movigh GR2 0x0000||

#pc = 0x00031278  
movg2c GR2||
movigl GR18 0x05A8||
movigh GR18 0x0006||
testi GR2 0x18||store16 GR18 GR18 0x1EA

#pc = 0x0003128C  
movigl GR8 0x4D97|loadu16 GR13 GR18 0x1EA|
movigh GR8 0x0006||
movigl GR5 0x4001||
movigh GR5 0x0000||

#pc = 0x000312A0  
movg2c GR5||
addic GR3 GR17 0x0b7||
fseq GR15 GR23||store8 GR3 GR8 0x017
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR1||

#pc = 0x000312DC  
movigl GR1 0x0001||
movigh GR1 0x0000||
movigl GR24 0x4000||
movigh GR24 0x0000||

#pc = 0x000312EC  
movg2c GR24||
bclr GR24 0x19||
movigl GR24 0x019E||
movigh GR24 0x0000||

#pc = 0x000312FC  
lei GR24 0x0d1||
movigl GR1 0xBE63||
movigh GR1 0x2B70||
movigl GR5 0xBE63||

#pc = 0x0003130C  
movigh GR5 0x2B70||
geu GR1 GR5||
movigl GR2 0x5536||
movigh GR2 0x0006||

#pc = 0x0003131C  
add GR12 GR9 GR1||
movigl GR24 0xF5F3||store8 GR12 GR2 0x065
movigh GR24 0x0003|loadu8 GR5 GR2 0x065|
movigl GR6 0x0016||

#pc = 0x00031334  
movigh GR6 0x0000||
srl GR7 GR27 GR6||
||storeu8 GR7 GR24 0x193
movigl GR26 0x9E08||

#pc = 0x00031344  
movigh GR26 0xD478||
fcvtfs GR27 GR26||
movigl GR6 0x8BAC||
movigh GR6 0x580A||

#pc = 0x00031354  
movigl GR20 0x8BAC||
movigh GR20 0x580A||
ge GR6 GR20||
ltu GR27 GR29||

#pc = 0x00031364  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR3||

#pc = 0x00031390  
movigl GR3 0x0001||
movigh GR3 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x000313A0  
movg2c GR19||
xor GR22 GR6 GR3||
movigl GR14 0x1F29||
movigh GR14 0x0007||

#pc = 0x000313B0  
subc GR7 GR20 GR29||
movigl GR20 0xDDEF||store8 GR7 GR14 0x1F4
movigh GR20 0x0007|load8 GR25 GR14 0x1F4|
sub GR29 GR19 GR11||

#pc = 0x000313C8  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR21||

#pc = 0x000313F4  
movigl GR21 0x0001||
movigh GR21 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x00031404  
movg2c GR9||storeu8 GR9 GR20 0x11a
movigl GR27 0xCB47||
movigh GR27 0x6C83||
fcvtsu GR6 GR27||

#pc = 0x00031418  
min GR22 GR27 GR9||
bclr GR28 0x1e||
movigl GR15 0x46CC||
movigh GR15 0x0005||

#pc = 0x00031428  
movigl GR1 0xDE78||store32 GR26 GR15 0x0DD
movigh GR1 0x0004|loadu32 GR17 GR15 0x0DD|
bfextu GR12 GR4 0x0c 0x1f||fcvtus GR9 GR26
sub GR8 GR12 GR26||storeu8 GR12 GR1 0x1f9

#pc = 0x00031448  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00031474  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR16 0x4000||
movigh GR16 0x0000||

#pc = 0x00031484  
movg2c GR16||
test GR8 GR9||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR12||

#pc = 0x000314B8  
movigl GR12 0x0001||
movigh GR12 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x000314C8  
movg2c GR9||
movigl GR3 0xFD24||
movigh GR3 0x0003||
movigl BAR2 0xFD1A||

#pc = 0x000314D8  
movigh BAR2 0x0003||
movigl MR2 0x0008||
movigh MR2 0x0000||
movigl OFF2 0x0002||

#pc = 0x000314E8  
movigh OFF2 0x0000||
movigl GR22 0x4000||storeo16 GR12 GR3 BAR2
movigh GR22 0x0000||storeo16 GR9 GR3 BAR2
movg2c GR22||

#pc = 0x00031500  
subc GR13 GR5 GR24||
movigl GR25 0x0000||storeo16 GR13 GR3 BAR2
movigh GR25 0x0000||storeo16 GR22 GR3 BAR2
movg2c GR25||

#pc = 0x00031518  
movigl GR9 0xAC4C||
movigh GR9 0xC6BD||
movigl GR21 0xAF28||
movigh GR21 0xC6B9||

#pc = 0x00031528  
subc GR6 GR9 GR21||
movigl GR8 0x0000|loado16 GR19 GR6 BAR2|
movigh GR8 0x0000|loado16 GR19 GR6 BAR2|
movg2c GR8|loado16 GR19 GR6 BAR2|

#pc = 0x00031544  
movigl GR28 0xF728|loado16 GR19 GR6 BAR2|
movigh GR28 0xF84F||
movigl GR9 0xFB9A||
movigh GR9 0xF848||

#pc = 0x00031558  
subc GR4 GR28 GR9||
movigl GR22 0x15F9||store8 GR21 GR4 0x009
movigh GR22 0x48D0||
movigl GR17 0x15F9||

#pc = 0x0003156C  
movigh GR17 0x48D0||
fsle GR22 GR17||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR11||

#pc = 0x000315A0  
movigl GR11 0x0001||
movigh GR11 0x0000||
movigl GR1 0x4000||
movigh GR1 0x0000||

#pc = 0x000315B0  
movg2c GR1||
movigl GR27 0x00EC||
movigh GR27 0x0000||
gei GR27 0x189||

#pc = 0x000315C0  
movigl GR20 0x000F||
movigh GR20 0x0000||
srl GR2 GR17 GR20||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR5||

#pc = 0x000315F8  
movigl GR5 0x0001||
movigh GR5 0x0000||
movigl GR2 0x4000||
movigh GR2 0x0000||

#pc = 0x00031608  
movg2c GR2||
movigl GR16 0x0155||
movigh GR16 0x0000||
neqi GR16 0x181||

#pc = 0x00031618  
addic GR16 GR25 0x0e5||
movigl GR20 0xD6E4||
movigh GR20 0x0006||
bfext GR10 GR16 0x03 0x01||

#pc = 0x00031628  
movigl GR13 0xDE01||store32 GR10 GR20 0x1C4
movigh GR13 0x0004|loadu32 GR14 GR20 0x1C4|
movigl GR21 0x4000||
movigh GR21 0x0000||

#pc = 0x00031640  
movg2c GR21||
sub GR28 GR16 GR10||
fseq GR5 GR16||store8 GR28 GR13 0x149
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR5||

#pc = 0x0003167C  
movigl GR5 0x0001||
movigh GR5 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x0003168C  
movg2c GR19||
movg2g GR25 GR13||
movigl GR10 0x16CE||
movigh GR10 0x0007||

#pc = 0x0003169C  
movigl GR12 0x475A||store8 GR5 GR10 0x052
movigh GR12 0x0007|load8 GR7 GR10 0x052|
max GR25 GR25 GR9||
fsmin GR1 GR25 GR19||store16 GR25 GR12 0x1EA

#pc = 0x000316B8  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR6||

#pc = 0x000316E4  
movigl GR6 0x0001||
movigh GR6 0x0000||
movigl GR21 0x4000||
movigh GR21 0x0000||

#pc = 0x000316F4  
movg2c GR21||
add GR16 GR21 GR1||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00031728  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x00031738  
movg2c GR19||
movigl GR3 0x00C2||
movigh GR3 0x0000||
gti GR3 0x170||

#pc = 0x00031748  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR24||

#pc = 0x00031774  
movigl GR24 0x0001||
movigh GR24 0x0000||
movigl GR11 0x4000||
movigh GR11 0x0000||

#pc = 0x00031784  
movg2c GR11||
subc GR8 GR11 GR24||
add GR24 GR21 GR8||
movigl GR3 0x1164||

#pc = 0x00031794  
movigh GR3 0x4D01||
movigl GR23 0x16FC||
movigh GR23 0x4D06||
xor GR17 GR3 GR23||

#pc = 0x000317A4  
not GR15 GR3||
movigl GR26 0x0BD3||store32 GR15 GR17 0x097
movigh GR26 0xC217|load32 GR22 GR17 0x097|
movigl GR5 0x8124||

#pc = 0x000317BC  
movigh GR5 0xC210||
xor GR1 GR26 GR5||
movigl GR2 0x0018||
movigh GR2 0x0000||

#pc = 0x000317CC  
sra GR6 GR15 GR2||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR21||

#pc = 0x000317FC  
movigl GR21 0x0001||
movigh GR21 0x0000||
movigl GR3 0x4000||
movigh GR3 0x0000||

#pc = 0x0003180C  
movg2c GR3||storeu8 GR3 GR1 0x05f
fslt GR14 GR12||
movigl GR21 0x6182||
movigh GR21 0x7F47||

#pc = 0x00031820  
movigl GR14 0xFF82||
movigh GR14 0xFFFF||
gt GR21 GR14||
movigl GR29 0xFCAC||

#pc = 0x00031830  
movigh GR29 0x0003||
movigl GR16 0xB8A8||
movigh GR16 0x0002||
or GR4 GR29 GR16||

#pc = 0x00031840  
bclr GR29 0x1d||store16 GR4 GR4 0x048
movigl GR9 0x827A|load16 GR24 GR4 0x048|
movigh GR9 0x0003||
test GR16 GR14||storeu16 GR9 GR9 0x086

#pc = 0x0003185C  
movigl GR5 0xAA0E||
movigh GR5 0xB71F||
movigl GR18 0x832D||
movigh GR18 0x217B||

#pc = 0x0003186C  
fsdiv GR14 GR5 GR18||
movigl GR25 0x0006||
movigh GR25 0x0000||
gti GR25 0x014||

#pc = 0x0003187C  
leu GR25 GR8||
movigl GR13 0x001B||
movigh GR13 0x0000||
srl GR23 GR25 GR13||

#pc = 0x0003188C  
and GR16 GR18 GR29||
movigl GR14 0x929C||
movigh GR14 0x0005||
movigl GR7 0x909C||

#pc = 0x0003189C  
movigh GR7 0x0001||
or GR25 GR14 GR7||
movigl GR29 0x7A43||store8 GR8 GR25 0x0D7
movigh GR29 0x0006|load8 GR10 GR25 0x0D7|

#pc = 0x000318B4  
sub GR12 GR7 GR14||
movigl GR7 0x8656||storeu8 GR12 GR29 0x020
movigh GR7 0x9F9A||
movigl GR5 0x4F18||

#pc = 0x000318C8  
movigh GR5 0x9A5E||
fsmul GR26 GR7 GR5||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x000318FC  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR15 0x4000||
movigh GR15 0x0000||

#pc = 0x0003190C  
movg2c GR15||
add GR12 GR5 GR7||
sub GR2 GR5 GR26||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR15||

#pc = 0x00031944  
movigl GR15 0x0001||
movigh GR15 0x0000||
movigl GR22 0x4000||
movigh GR22 0x0000||

#pc = 0x00031954  
movg2c GR22||
movigl GR27 0x9CAC||
movigh GR27 0xD11B||
movigl GR20 0x5384||

#pc = 0x00031964  
movigh GR20 0xD115||
sub GR17 GR27 GR20||
movigl BAR0 0x4938||
movigh BAR0 0x0006||

#pc = 0x00031974  
movigl MR0 0x0030||
movigh MR0 0x0000||
movigl OFF0 0x0008||
movigh OFF0 0x0000||

#pc = 0x00031984  
movigl GR22 0x0007||
movigh GR22 0x0000||
srl GR24 GR20 GR22||
test GR22 GR14||storeo16 GR24 GR17 BAR0

#pc = 0x00031998  
movigl GR12 0x000C||storeo16 GR24 GR17 BAR0
movigh GR12 0x0000||
sl GR2 GR22 GR12||
movigl GR8 0x4928||storeo16 GR2 GR17 BAR0

#pc = 0x000319B0  
movigh GR8 0x0006||storeo16 GR16 GR17 BAR0
movigl GR16 0xB3DE||storeo16 GR12 GR17 BAR0
movigh GR16 0x0005||storeo16 GR12 GR17 BAR0
abs GR10 GR1|loado16 GR22 GR8 BAR0|

#pc = 0x000319D0  
fsle GR26 GR18|loado16 GR22 GR8 BAR0|storeu8 GR10 GR16 0x160
addic GR10 GR28 0x65b|loado16 GR22 GR8 BAR0|
gtu GR15 GR10|loado16 GR22 GR8 BAR0|
nop|loado16 GR22 GR8 BAR0|
nop|loado16 GR22 GR8 BAR0|
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR24||

#pc = 0x00031A20  
movigl GR24 0x0001||
movigh GR24 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x00031A30  
movg2c GR19||
movigl GR3 0x0032||
movigh GR3 0x0000||
eqi GR3 0x032||

#pc = 0x00031A40  
movigl GR25 0x7736||
movigh GR25 0x94C2||
movigl GR20 0x418C||
movigh GR20 0x94BB||

#pc = 0x00031A50  
sub GR27 GR25 GR20||
movigl BAR3 0x35B6||
movigh BAR3 0x0007||
movigl MR3 0x0018||

#pc = 0x00031A60  
movigh MR3 0x0000||
movigl OFF3 0x0006||
movigh OFF3 0x0000||
bfextu GR20 GR20 0x1c 0x14||storeo16 GR25 GR27 BAR3

#pc = 0x00031A74  
movigl GR23 0x4000||storeo16 GR20 GR27 BAR3
movigh GR23 0x0000||storeo16 GR20 GR27 BAR3
movg2c GR23||
addc GR11 GR20 GR17||

#pc = 0x00031A8C  
movigl GR24 0x5BEC||storeo16 GR11 GR27 BAR3
movigh GR24 0xBCB9||
movigl GR17 0x2642||
movigh GR17 0xBCB2||

#pc = 0x00031AA0  
sub GR7 GR24 GR17||
movigl GR28 0xF9E4|loado16 GR10 GR7 BAR3|
movigh GR28 0x9D45|loado16 GR10 GR7 BAR3|
movigl GR1 0xBFDF|loado16 GR10 GR7 BAR3|

#pc = 0x00031ABC  
movigh GR1 0x62BE|loado16 GR10 GR7 BAR3|
and GR18 GR28 GR1||
addi GR1 GR24 0x571||fsdiv GR5 GR25 GR16
min GR27 GR1 GR28||storeu8 GR1 GR18 0x098

#pc = 0x00031AD8  
max GR22 GR1 GR8||
movigl GR24 0x77E1||
movigh GR24 0x6F90||
movigl GR14 0xE243||

#pc = 0x00031AE8  
movigh GR14 0x6F89||
sub GR25 GR24 GR14||
movigl GR10 0xA7EC||store8 GR1 GR25 0x054
movigh GR10 0x0005|loadu8 GR12 GR25 0x054|

#pc = 0x00031B00  
movigl GR5 0x139D||storeu8 GR14 GR10 0x144
movigh GR5 0xC038||
movigl GR26 0x1A3B||
movigh GR26 0x4502||

#pc = 0x00031B14  
fssub GR22 GR5 GR26||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00031B44  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x00031B54  
movg2c GR9||
leu GR5 GR9||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR28||

#pc = 0x00031B88  
movigl GR28 0x0001||
movigh GR28 0x0000||
movigl GR16 0x4000||
movigh GR16 0x0000||

#pc = 0x00031B98  
movg2c GR16||
movigl GR24 0x0014||
movigh GR24 0x0000||
sl GR16 GR8 GR24||

#pc = 0x00031BA8  
movigl GR6 0x00E4||
movigh GR6 0x0000||
neqi GR6 0x06e||
neq GR21 GR24||

#pc = 0x00031BB8  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR28||

#pc = 0x00031BE4  
movigl GR28 0x0001||
movigh GR28 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x00031BF4  
movg2c GR9||
movigl GR22 0xED74||
movigh GR22 0x0007||
movigl GR3 0xA209||store8 GR5 GR22 0x127

#pc = 0x00031C08  
movigh GR3 0x0007|loadu8 GR20 GR22 0x127|
||store8 GR29 GR3 0x126
movigl GR19 0x24A3||
movigh GR19 0x2D45||

#pc = 0x00031C1C  
movigl GR19 0xD7A3||
movigh GR19 0xC3CB||
fcvtus GR17 GR19||
movigl GR19 0xB23F||

#pc = 0x00031C2C  
movigh GR19 0x0A8E||
movigl GR1 0xB23F||
movigh GR1 0x0A8E||
lt GR19 GR1||

#pc = 0x00031C3C  
eq GR19 GR1||
movigl GR29 0x606D||
movigh GR29 0x0007||
xor GR11 GR5 GR19||

#pc = 0x00031C4C  
movigl GR2 0x78C2||store8 GR11 GR29 0x14D
movigh GR2 0x0004|loadu8 GR9 GR29 0x14D|
xor GR7 GR19 GR1||
movigl GR28 0x3B22||storeu8 GR7 GR2 0x105

#pc = 0x00031C68  
movigh GR28 0x6340||
movigl GR1 0x3B22||
movigh GR1 0x6340||
fsge GR28 GR1||

#pc = 0x00031C78  
movigl GR1 0x24E5||
movigh GR1 0x66E0||
movigl GR28 0x24E5||
movigh GR28 0x66E0||

#pc = 0x00031C88  
ge GR1 GR28||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR7||

#pc = 0x00031CB8  
movigl GR7 0x0001||
movigh GR7 0x0000||
movigl GR19 0x4000||
movigh GR19 0x0000||

#pc = 0x00031CC8  
movg2c GR19||
subc GR16 GR28 GR4||
movigl GR8 0x0001||
movigh GR8 0x0000||

#pc = 0x00031CD8  
neqi GR8 0x1ca||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR14||

#pc = 0x00031D08  
movigl GR14 0x0001||
movigh GR14 0x0000||
movigl GR24 0x4000||
movigh GR24 0x0000||

#pc = 0x00031D18  
movg2c GR24||
movigl GR1 0x0011||
movigh GR1 0x0000||
sra GR27 GR24 GR1||

#pc = 0x00031D28  
movigl GR26 0x550A||
movigh GR26 0x0005||
add GR25 GR1 GR14||
movigl GR10 0xFF93||store8 GR25 GR26 0x023

#pc = 0x00031D3C  
movigh GR10 0x0006|load8 GR17 GR26 0x023|
addi GR5 GR10 0x7FD||
test GR23 GR10||store16 GR5 GR5 0x079
fseisqrt GR11 GR10||

#pc = 0x00031D54  
ge GR27 GR18||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR12||

#pc = 0x00031D84  
movigl GR12 0x0001||
movigh GR12 0x0000||
movigl GR1 0x4000||
movigh GR1 0x0000||

#pc = 0x00031D94  
movg2c GR1||
movigl GR22 0xBA77||
movigh GR22 0x0005||
addi GR28 GR22 0x525||

#pc = 0x00031DA4  
movigl BAR3 0xB76C||
movigh BAR3 0x0005||
movigl MR3 0x003C||
movigh MR3 0x0000||

#pc = 0x00031DB4  
movigl OFF3 0x000C||
movigh OFF3 0x0000||
max GR24 GR22 GR20||storeo16 GR1 GR28 BAR3
movigl GR20 0x0000||storeo16 GR24 GR28 BAR3

#pc = 0x00031DCC  
movigh GR20 0x0000||storeo16 GR9 GR28 BAR3
movg2c GR20||storeo16 GR16 GR28 BAR3
movigl GR23 0xC896||storeo16 GR6 GR28 BAR3
movigh GR23 0x3F69||

#pc = 0x00031DE8  
movigl GR25 0xEF06||
movigh GR25 0xC09B||
addc GR22 GR23 GR25||
movigl GR3 0x4C31|loado16 GR7 GR22 BAR3|

#pc = 0x00031DFC  
movigh GR3 0x0006|loado16 GR7 GR22 BAR3|
|loado16 GR7 GR22 BAR3|store8 GR29 GR3 0x15E
|loado16 GR7 GR22 BAR3|
|loado16 GR7 GR22 BAR3|

#pc = 0x00031E14  
movigl GR24 0xC1BA||
movigh GR24 0xA720||
movigl GR11 0x81B8||
movigh GR11 0xB47F||

#pc = 0x00031E24  
movigl GR24 0xFE23||
movigh GR24 0xD539||
fsdiv GR15 GR11 GR24||
gt GR11 GR24||

#pc = 0x00031E34  
movigl GR11 0x2085||
movigh GR11 0x27AD||
movigl GR24 0x2085||
movigh GR24 0x27AD||

#pc = 0x00031E44  
gtu GR11 GR24||
movigl GR28 0xC03D||
movigh GR28 0x0004||
testi GR11 0x06||store8 GR28 GR28 0x0E1

#pc = 0x00031E58  
movigl GR2 0x8400|loadu8 GR21 GR28 0x0E1|
movigh GR2 0x0007||
movigl GR29 0x0001||
movigh GR29 0x0000||

#pc = 0x00031E6C  
sl GR8 GR27 GR29||
movigl GR29 0x4CCD||storeu8 GR8 GR2 0x0b2
movigh GR29 0x3847||
movigl GR9 0x4CCD||

#pc = 0x00031E80  
movigh GR9 0x3847||
fsle GR29 GR9||
movigl GR10 0x4000||
movigh GR10 0x0000||

#pc = 0x00031E90  
movg2c GR10||
addi GR9 GR5 0x79f||
movigl GR1 0x396C||
movigh GR1 0x0005||

#pc = 0x00031EA0  
addc GR12 GR24 GR23||
movigl GR6 0x042E||store8 GR12 GR1 0x13E
movigh GR6 0x0006|loadu8 GR19 GR1 0x13E|
movigl BAR1 0x0460||

#pc = 0x00031EB8  
movigh BAR1 0x0006||
movigl MR1 0x0064||
movigh MR1 0x0000||
movigl OFF1 0x000A||

#pc = 0x00031EC8  
movigh OFF1 0x0000||
movigl GR26 0x001F||
movigh GR26 0x0000||
srl GR14 GR22 GR26||

#pc = 0x00031ED8  
movigl GR20 0x4001||storeo16 GR14 GR6 BAR1
movigh GR20 0x0000||storeo16 GR25 GR6 BAR1
movg2c GR20||storeo16 GR26 GR6 BAR1
addi GR26 GR4 0x42c||

#pc = 0x00031EF4  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR14||

#pc = 0x00031F20  
movigl GR14 0x0001||
movigh GR14 0x0000||
movigl GR24 0x4000||
movigh GR24 0x0000||

#pc = 0x00031F30  
movg2c GR24||
addc GR20 GR26 GR20||storeo16 GR24 GR6 BAR1
max GR21 GR14 GR24||storeo16 GR20 GR6 BAR1
movigl GR15 0x0002||storeo16 GR29 GR6 BAR1

#pc = 0x00031F4C  
movigh GR15 0x0000||storeo16 GR21 GR6 BAR1
srl GR11 GR7 GR15||
bclr GR13 0x0d||storeo16 GR11 GR6 BAR1
and GR3 GR15 GR11||storeo16 GR11 GR6 BAR1

#pc = 0x00031F68  
||storeo16 GR3 GR6 BAR1
movigl GR24 0x54AC||
movigh GR24 0xB28C||
movigl GR24 0x939A||

#pc = 0x00031F78  
movigh GR24 0x49A3||
fseisqrt GR16 GR24||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR11||

#pc = 0x00031FAC  
movigl GR11 0x0001||
movigh GR11 0x0000||
movigl GR4 0x4000||
movigh GR4 0x0000||

#pc = 0x00031FBC  
movg2c GR4||
chw GR23 GR13||
add GR28 GR24 GR11||
ltu GR28 GR26||

#pc = 0x00031FCC  
movigl GR24 0x4000||
movigh GR24 0x0000||
movg2c GR24||
addi GR3 GR9 0x232||

#pc = 0x00031FDC  
movigl GR24 0x0000||
movigh GR24 0x0000||
movg2c GR24||
movigl GR10 0x8119||

#pc = 0x00031FEC  
movigh GR10 0xBD4C||
movigl GR28 0x34F0||
movigh GR28 0xBD45||
subc GR13 GR10 GR28||

#pc = 0x00031FFC  
addi GR24 GR21 0x495||
movigl GR2 0x3C41||store8 GR24 GR13 0x1A8
movigh GR2 0x0005|loadu8 GR19 GR13 0x1A8|
fsle GR7 GR8||store8 GR24 GR2 0x0F7

#pc = 0x00032018  
gtu GR10 GR28||
movigl GR22 0x0019||
movigh GR22 0x0000||
sra GR8 GR24 GR22||

#pc = 0x00032028  
movigl GR1 0x966E||
movigh GR1 0x7D35||
movigl GR22 0x966E||
movigh GR22 0x7D35||

#pc = 0x00032038  
gtu GR1 GR22||
movigl GR14 0x00E1||
movigh GR14 0x0000||
lei GR14 0x0f9||

#pc = 0x00032048  
movigl GR20 0xC8D4||
movigh GR20 0x0004||
movigl GR17 0x925A||store32 GR1 GR20 0x05C
movigh GR17 0x0006|loadu32 GR22 GR20 0x05C|

#pc = 0x00032060  
movigl GR9 0x4000||
movigh GR9 0x0000||
movg2c GR9||
subc GR11 GR14 GR1||

#pc = 0x00032070  
fseq GR28 GR26||store8 GR11 GR17 0x0DE
testi GR9 0x1c||
movigl GR15 0x8AF0||
movigh GR15 0x0004||

#pc = 0x00032084  
abs GR27 GR9||
movigl GR24 0xAD28||store16 GR27 GR15 0x119
movigh GR24 0x0003|loadu16 GR6 GR15 0x119|
addi GR23 GR24 0x0BF||

#pc = 0x0003209C  
movigl GR5 0x4001||
movigh GR5 0x0000||
movg2c GR5||
addic GR27 GR18 0x1ee||

#pc = 0x000320AC  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR24||

#pc = 0x000320D8  
movigl GR24 0x0001||
movigh GR24 0x0000||
movigl GR18 0x4000||
movigh GR18 0x0000||

#pc = 0x000320E8  
movg2c GR18||store8 GR18 GR23 0x1B5
movigl GR27 0x4288||
movigh GR27 0x0F93||
movigl GR5 0xF832||

#pc = 0x000320FC  
movigh GR5 0x1860||
fsmin GR26 GR27 GR5||
movigl GR27 0x0054||
movigh GR27 0x0000||

#pc = 0x0003210C  
lti GR27 0x0d3||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR5||

#pc = 0x0003213C  
movigl GR5 0x0001||
movigh GR5 0x0000||
movigl GR4 0x4000||
movigh GR4 0x0000||

#pc = 0x0003214C  
movg2c GR4||
movigl GR1 0x01C9||
movigh GR1 0x0000||
gti GR1 0x16b||

#pc = 0x0003215C  
movigl GR5 0xE919||
movigh GR5 0x280F||
movigl GR26 0xE919||
movigh GR26 0x280F||

#pc = 0x0003216C  
ltu GR5 GR26||
movigl GR29 0x1D17||
movigh GR29 0x0006||
movigl GR4 0xDDCE||store8 GR26 GR29 0x116

#pc = 0x00032180  
movigh GR4 0x0007|load8 GR13 GR29 0x116|
xor GR24 GR8 GR26||
movigl GR26 0xE6A4||store8 GR24 GR4 0x1FA
movigh GR26 0x307E||

#pc = 0x00032198  
fcvtsu GR5 GR26||
movigl GR26 0xA22C||
movigh GR26 0x5C48||
movigl GR11 0xA22C||

#pc = 0x000321A8  
movigh GR11 0x5C48||
ge GR26 GR11||
movigl GR8 0x4001||
movigh GR8 0x0000||

#pc = 0x000321B8  
movg2c GR8||
addi GR11 GR14 0x714||
movigl GR14 0xB2E4||
movigh GR14 0x0007||

#pc = 0x000321C8  
movigl GR8 0x001E||
movigh GR8 0x0000||
sra GR26 GR5 GR8||
movigl GR2 0xFF6B||store8 GR26 GR14 0x138

#pc = 0x000321DC  
movigh GR2 0xCC07|load8 GR20 GR14 0x138|
movigl GR3 0x7CDC||
movigh GR3 0x33FD||
and GR1 GR2 GR3||

#pc = 0x000321F0  
test GR8 GR5||storeu16 GR1 GR1 0x081
fslt GR16 GR23||
le GR18 GR2||
addi GR3 GR24 0x176||

#pc = 0x00032204  
movigl GR11 0x0EA5||
movigh GR11 0x0007||
min GR7 GR3 GR2||
movigl GR17 0x2FE6||store8 GR7 GR11 0x0CB

#pc = 0x00032218  
movigh GR17 0x0006|loadu8 GR19 GR11 0x0CB|
sub GR12 GR3 GR22||
movigl GR16 0xF35D||storeu16 GR12 GR17 0x175
movigh GR16 0xBEEC||

#pc = 0x00032230  
fseinv GR6 GR16||
addi GR16 GR22 0x098||
lt GR16 GR24||
movigl GR28 0x4000||

#pc = 0x00032240  
movigh GR28 0x0000||
movg2c GR28||
addic GR16 GR12 0x5cd||
movigl GR12 0x8624||

#pc = 0x00032250  
movigh GR12 0x0007||
movigl BAR3 0x8630||
movigh BAR3 0x0007||
movigl MR3 0x0028||

#pc = 0x00032260  
movigh MR3 0x0000||
movigl OFF3 0x0004||
movigh OFF3 0x0000||
movigl GR3 0x4001||storeo32 GR16 GR12 BAR3

#pc = 0x00032274  
movigh GR3 0x0000||storeo32 GR16 GR12 BAR3
movg2c GR3||
addi GR2 GR13 0x55f||
test GR2 GR3||storeo32 GR2 GR12 BAR3

#pc = 0x0003228C  
chw GR6 GR2||storeo32 GR2 GR12 BAR3
movigl GR24 0x4000||storeo32 GR2 GR12 BAR3
movigh GR24 0x0000||storeo32 GR3 GR12 BAR3
movg2c GR24||storeo32 GR6 GR12 BAR3

#pc = 0x000322AC  
subc GR15 GR6 GR7||storeo32 GR6 GR12 BAR3
movigl GR4 0x8624||storeo32 GR6 GR12 BAR3
movigh GR4 0x0007||storeo32 GR15 GR12 BAR3
movigl GR16 0xF3B8|loado32 GR10 GR4 BAR3|

#pc = 0x000322CC  
movigh GR16 0x0003|loado32 GR10 GR4 BAR3|
and GR15 GR3 GR9|loado32 GR10 GR4 BAR3|
fslt GR5 GR6|loado32 GR10 GR4 BAR3|store16 GR15 GR16 0x1D5
nop|loado32 GR10 GR4 BAR3|
nop|loado32 GR10 GR4 BAR3|
nop|loado32 GR10 GR4 BAR3|
nop|loado32 GR10 GR4 BAR3|
nop|loado32 GR10 GR4 BAR3|
nop||
nop||
nop||
nop||
nop||
movc2g GR9|loado32 GR10 GR4 BAR3|

#pc = 0x0003232C  
movigl GR9 0x0001||
movigh GR9 0x0000||
movigl GR6 0x4000||
movigh GR6 0x0000||

#pc = 0x0003233C  
movg2c GR6||
movigl GR26 0x00B2||
movigh GR26 0x0000||
lei GR26 0x111||

#pc = 0x0003234C  
movigl GR25 0x4001||
movigh GR25 0x0000||
movg2c GR25||
subc GR21 GR9 GR26||

#pc = 0x0003235C  
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR8||

#pc = 0x00032388  
movigl GR8 0x0001||
movigh GR8 0x0000||
movigl GR9 0x4000||
movigh GR9 0x0000||

#pc = 0x00032398  
movg2c GR9||
leu GR8 GR26||
movigl GR28 0xE71D||
movigh GR28 0xE408||

#pc = 0x000323A8  
movigl GR13 0x05B9||
movigh GR13 0xE40C||
xor GR18 GR28 GR13||
movigl GR17 0x0008||

#pc = 0x000323B8  
movigh GR17 0x0000||
srl GR28 GR19 GR17||
movigl GR2 0x261A||store8 GR28 GR18 0x0AC
movigh GR2 0x0006|load8 GR27 GR18 0x0AC|

#pc = 0x000323D0  
||storeu8 GR28 GR2 0x146
movigl GR1 0x54BE||
movigh GR1 0x3FE5||
fseinv GR5 GR1||

#pc = 0x000323E0  
subc GR29 GR29 GR28||
bfextu GR28 GR7 0x1e 0x07||
movigl GR8 0x2294||
movigh GR8 0x0007||

#pc = 0x000323F0  
addi GR5 GR8 0x05C||
movigl GR24 0x0000||store32 GR23 GR5 0x137
movigh GR24 0x0000|load32 GR12 GR5 0x137|
movg2c GR24||

#pc = 0x00032408  
movigl GR22 0x819E||
movigh GR22 0x1B43||
movigl GR20 0x7CB2||
movigh GR20 0x1B3F||

#pc = 0x00032418  
subc GR23 GR22 GR20||
||store16 GR8 GR23 0x0F2
movigl GR17 0x51CA||
movigh GR17 0x4D51||

#pc = 0x00032428  
fsmul GR26 GR1 GR17||
ge GR22 GR20||
movigl GR20 0xFF8C||
movigh GR20 0xFFFF||

#pc = 0x00032438  
movigl GR19 0xFF8C||
movigh GR19 0xFFFF||
gt GR20 GR19||
movigl GR20 0x741F||

#pc = 0x00032448  
movigh GR20 0x5AD2||
movigl GR26 0x741F||
movigh GR26 0x5AD2||
le GR20 GR26||

#pc = 0x00032458  
abs GR17 GR20||
movigl GR1 0x12B0||
movigh GR1 0x0007||
movigl GR26 0x4000||

#pc = 0x00032468  
movigh GR26 0x0000||
movg2c GR26||
addi GR19 GR9 0x096||
movigl GR29 0xB570||store16 GR19 GR1 0x1B8

#pc = 0x0003247C  
movigh GR29 0x0005|loadu16 GR21 GR1 0x1B8|
addic GR19 GR15 0x69a||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR15||

#pc = 0x000324B4  
movigl GR15 0x0001||
movigh GR15 0x0000||
movigl GR13 0x4000||
movigh GR13 0x0000||

#pc = 0x000324C4  
movg2c GR13||store16 GR13 GR29 0x049
movigl GR16 0x3ABF||
movigh GR16 0x2A37||
movigl GR19 0x9493||

#pc = 0x000324D8  
movigh GR19 0xCB27||
movigl GR16 0x4A7F||
movigh GR16 0x37E9||
movigl GR19 0x0913||

#pc = 0x000324E8  
movigh GR19 0xB583||
fsadd GR22 GR16 GR19||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR15||

#pc = 0x0003251C  
movigl GR15 0x0001||
movigh GR15 0x0000||
movigl GR16 0x4000||
movigh GR16 0x0000||

#pc = 0x0003252C  
movg2c GR16||
xor GR9 GR16 GR19||
leu GR22 GR16||
movigl GR16 0xB1E0||

#pc = 0x0003253C  
movigh GR16 0x0005||
movigl GR18 0x4000||
movigh GR18 0x0000||
movg2c GR18||

#pc = 0x0003254C  
add GR20 GR15 GR11||
movigl GR27 0x7A2D||store32 GR20 GR16 0x0B7
movigh GR27 0x62A2|loadu32 GR15 GR16 0x0B7|
movigl GR6 0xDD52||

#pc = 0x00032564  
movigh GR6 0x62A7||
xor GR14 GR27 GR6||
bclr GR6 0x10||store8 GR14 GR14 0x14E
fsge GR8 GR19||

#pc = 0x00032578  
sub GR12 GR27 GR6||
min GR13 GR27 GR3||
movigl GR20 0x00C3||
movigh GR20 0x0000||

#pc = 0x00032588  
gei GR20 0x0c3||
movigl GR27 0xDEEE||
movigh GR27 0x413F||
movigl GR5 0xEFF9||

#pc = 0x00032598  
movigh GR5 0xBEC5||
and GR12 GR27 GR5||
movigl GR13 0x0000||store8 GR27 GR12 0x103
movigh GR13 0x0000|loadu8 GR27 GR12 0x103|

#pc = 0x000325B0  
movg2c GR13||
movigl GR24 0x85A5||
movigh GR24 0xA5E9||
movigl GR21 0x4FD3||

#pc = 0x000325C0  
movigh GR21 0xA5E2||
subc GR26 GR24 GR21||
addi GR13 GR2 0x3c3||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR28||

#pc = 0x000325F8  
movigl GR28 0x0001||
movigh GR28 0x0000||
movigl GR3 0x4000||
movigh GR3 0x0000||

#pc = 0x00032608  
movg2c GR3||store16 GR3 GR26 0x09A
movigl GR3 0x049F||
movigh GR3 0xCCF8||
fsabs GR28 GR3||

#pc = 0x0003261C  
movigl GR7 0x018E||
movigh GR7 0x0000||
gei GR7 0x034||
ltu GR3 GR21||

#pc = 0x0003262C  
movigl GR25 0x01D4||
movigh GR25 0x0000||
eqi GR25 0x1d4||
movigl GR9 0x6938||

#pc = 0x0003263C  
movigh GR9 0x0007||
movigl GR3 0x0000||store32 GR28 GR9 0x195
movigh GR3 0x0000|loadu32 GR10 GR9 0x195|
movg2c GR3||

#pc = 0x00032654  
movigl GR28 0x15BE||
movigh GR28 0x3B3A||
movigl GR1 0x538E||
movigh GR1 0x3B35||

#pc = 0x00032664  
subc GR11 GR28 GR1||
movigl GR28 0x9128||storeu8 GR25 GR11 0x0ca
movigh GR28 0xAF9D||
fsabs GR3 GR28||

#pc = 0x00032678  
movigl GR19 0x0141||
movigh GR19 0x0000||
gei GR19 0x03b||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR2||

#pc = 0x000326B0  
movigl GR2 0x0001||
movigh GR2 0x0000||
movigl GR14 0x4000||
movigh GR14 0x0000||

#pc = 0x000326C0  
movg2c GR14||
addc GR24 GR19 GR14||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
nop||
movc2g GR16||

#pc = 0x000326F4  
movigl GR16 0x0001||
movigh GR16 0x0000||
movigl GR8 0x4000||
movigh GR8 0x0000||

#pc = 0x00032704  
movg2c GR8||
xor GR27 GR16 GR14||
movigl GR15 0x57BE||
movigh GR15 0x0005||

#pc = 0x00032714  
testi GR2 0x00||store8 GR15 GR15 0x1A1
movigl GR1 0xE390|loadu8 GR2 GR15 0x1A1|
movigh GR1 0x0005||
movigl BAR0 0xE380||

#pc = 0x0003272C  
movigh BAR0 0x0005||
movigl MR0 0x0048||
movigh MR0 0x0000||
movigl OFF0 0x0008||

#pc = 0x0003273C  
movigh OFF0 0x0000||
testi GR22 0x10||
movigl GR7 0x4001||storeo32 GR1 GR1 BAR0
movigh GR7 0x0000||

#pc = 0x00032750  
movg2c GR7||
subc GR29 GR14 GR23||
max GR4 GR7 GR4||storeo32 GR29 GR1 BAR0
movigl GR8 0x001F||storeo32 GR12 GR1 BAR0

#pc = 0x00032768  
movigh GR8 0x0000||storeo32 GR4 GR1 BAR0
sra GR4 GR26 GR8||storeo32 GR7 GR1 BAR0
movigl GR25 0x4000||storeo32 GR4 GR1 BAR0
movigh GR25 0x0000||storeo32 GR8 GR1 BAR0

#pc = 0x00032788  
movg2c GR25||storeo32 GR8 GR1 BAR0
subc GR12 GR8 GR5||fcvtsu GR8 GR20
movigl GR10 0x4001||storeo32 GR12 GR1 BAR0
movigh GR10 0x0000||

#pc = 0x000327A4  
movg2c GR10||
addi GR4 GR24 0x799||
movigl GR11 0xFE41||
movigh GR11 0x0003||

#pc = 0x000327B4  
addi GR23 GR4 0x39d||
movigl GR29 0x70EE||store8 GR23 GR11 0x0ED
movigh GR29 0x0006|loadu8 GR28 GR11 0x0ED|
addi GR14 GR29 0x63E||

#pc = 0x000327CC  
bclr GR6 0x10||store32 GR14 GR14 0x077
fsmac GR23 GR3 GR22||

import os
import re
import sys
import copy
import argparse
import shutil
import binascii
import subprocess as sp

class GenRamImage:
    def __init__(self, coretype, inputexec, toolbinpath, linuxenv):
        self.coretype    = coretype
        self.inputexec   = inputexec
        self.toolbinpath = toolbinpath

        if not os.path.isfile(self.inputexec):
            print(self.inputexec + " doesn't exist!", file=sys.stderr)
            sys.exit(-1)

        if not linuxenv:
            objcopy = self.toolbinpath + '\\objcopy.exe'
            objdump = self.toolbinpath + '\\objdump.exe'
        else:
            objcopy = self.toolbinpath + '/objcopy.bin'
            objdump = self.toolbinpath + '/objdump.bin'

        if not os.path.isfile(objcopy):
            print(objcopy + "doesn't exist!", file=sys.stderr)
            sys.exit(-1)

        if not os.path.isfile(objdump):
            print(objdump + " doesn't exist!",file=sys.stderr)
            sys.exit(-1)

        self.objcopy = objcopy
        self.objdump = objdump

        self.INVALID_SYMBOL_VALUE = 0xFFFFFFFF
        # sections' LMA
        self.secLmaDict = {
            'dataStart'    : self.INVALID_SYMBOL_VALUE,
            'bssStart'     : self.INVALID_SYMBOL_VALUE,
            'dataEnd'      : self.INVALID_SYMBOL_VALUE,
            'textStart'    : self.INVALID_SYMBOL_VALUE,
            'textEnd'      : self.INVALID_SYMBOL_VALUE,
            'claDataStart' : self.INVALID_SYMBOL_VALUE,
            'claBssStart'  : self.INVALID_SYMBOL_VALUE,
            'claDataEnd'   : self.INVALID_SYMBOL_VALUE,
            'claTextStart' : self.INVALID_SYMBOL_VALUE,
            'claTextEnd'   : self.INVALID_SYMBOL_VALUE,

            'xintfDataStart': self.INVALID_SYMBOL_VALUE,
            'xintfBssStart' : self.INVALID_SYMBOL_VALUE,
            'xintfDataEnd'  : self.INVALID_SYMBOL_VALUE,
            'xintfTextStart': self.INVALID_SYMBOL_VALUE,
            'xintfTextEnd'  : self.INVALID_SYMBOL_VALUE
        }
        # sections' position in .bin file
        self.secBinPosDict = {};

    def genPlainBinary(self):
        outBin = self.inputexec[:-4] + '.bin'
        cmd = ["-O", "binary", self.inputexec ,outBin]
        sp.check_call([self.objcopy, *cmd])
        if not os.path.isfile(outBin):
            print("Failed to create " + outBin, file=sys.stderr)
            sys.exit(-1)
        self.outBin = outBin

    def genDisassembly(self):
        outdis = self.inputexec[:-4] + '.dis'
        cmd = ["-d", self.inputexec]
        sp.check_call([self.objdump, *cmd], stdout = open(outdis,'w'))
        if not os.path.isfile(outdis):
            print("Failed to create " + outdis, file=sys.stderr)
            sys.exit(-1)

        outdis = self.inputexec[:-4] + '.S.dis'
        cmd = ["-S", self.inputexec]
        sp.check_call([self.objdump, *cmd], stdout = open(outdis,'w'), stderr = sp.STDOUT)
        if not os.path.isfile(outdis):
            print("Failed to create " + outdis, file=sys.stderr)
            sys.exit(-1)

    def genRamImage(self, ramtype, ds, de, outputimage, offset):
        expectedRamtype = ['.data', '.bss', '.text', '.cla.data', '.cla.bss', '.cla.text', '.xintf.data', '.xintf.bss', '.xintf.text']
        if not ramtype in expectedRamtype:
            print("ERROR: unrecognized ramtype:", ramtype)
            sys.exit(-1)
        
        if (ds == de) and (ds == self.INVALID_SYMBOL_VALUE):
            return

        # skip for xintf contents if size is 0
        if ('.xintf' in ramtype) and (ds == de):
            return

        print(f"  section {ramtype:>12s}: range = [0x{ds:0>8x}, 0x{de:0>8x}], size = {(de-ds):>6d} Bytes (0x{(de-ds):0>6x})")

        # only print info for .bss sections
        if '.bss' in ramtype:
            return

        fd = open(outputimage, 'w')
        outBin = open(self.outBin,'rb')
        outBin.seek(offset)
        for i in range(ds, de, 16):
            insnPack = outBin.read(16)
            if(len(insnPack) != 16):
                break
            insnPack = binascii.b2a_hex(insnPack)
            insn0 = insnPack[0:8]
            insn1 = insnPack[8:16]
            insn2 = insnPack[16:24]
            insn3 = insnPack[24:32]
            insn0 = insn0[6:8] + insn0[4:6] + insn0[2:4] + insn0[0:2]
            insn1 = insn1[6:8] + insn1[4:6] + insn1[2:4] + insn1[0:2]
            insn2 = insn2[6:8] + insn2[4:6] + insn2[2:4] + insn2[0:2]
            insn3 = insn3[6:8] + insn3[4:6] + insn3[2:4] + insn3[0:2]
            if ramtype == '.text' or ramtype == '.cla.text' or ramtype == '.xintf.text':
                s = insn2.decode() + insn3.decode() + '\n' + insn0.decode() + insn1.decode() + '\n'
            elif ramtype == '.data' or ramtype == '.cla.data' or ramtype == '.xintf.data':
                s = insn1.decode() + insn0.decode() + '\n' + insn3.decode() + insn2.decode() + '\n'
            else:
                assert(False)
            fd.write(s)
        fd.close()
        outBin.close()

    def copy4RtlSimulation(self, textfile, datafile, claTextfile, claDatafile):
        # copy for software_lib_driver project only
        if re.match("software_lib_driver_", self.inputexec) == None:
            return

        # do not need to copy bootloader ram image
        if self.coretype == 'bootloader':
            return

        textfile4rtlsim = 'outer_insn_mem_' + self.coretype + '.dat'
        datafile4rtlsim = 'outer_data_mem_' + self.coretype + '.dat'
        shutil.copyfile(textfile, textfile4rtlsim)
        shutil.copyfile(datafile, datafile4rtlsim)

        claTextfile4rtlsim = 'outer_insn_mem_cla' + self.coretype[-1] + '.dat'
        claDatafile4rtlsim = 'outer_data_mem_cla' + self.coretype[-1] + '.dat'
        if os.path.exists(claTextfile) and os.path.exists(claDatafile):
            shutil.copyfile(claTextfile, claTextfile4rtlsim)
            shutil.copyfile(claDatafile, claDatafile4rtlsim)

    def generate(self):
        self.getSectionRange()
        self.genPlainBinary()
        self.genDisassembly()

        textfile = 'iram_image.' + self.coretype + '.dat'
        datafile = 'dram_image.' + self.coretype + '.dat'
        self.genRamImage('.text', self.secLmaDict['textStart'], self.secLmaDict['textEnd'], textfile, self.secBinPosDict['textStart'])
        self.genRamImage('.data', self.secLmaDict['dataStart'], self.secLmaDict['dataEnd'], datafile, self.secBinPosDict['dataStart'])
        self.genRamImage('.bss' , self.secLmaDict['bssStart'] , self.secLmaDict['dataEnd'], datafile, self.secBinPosDict['bssStart'] )

        claTextfile = 'iram_image.cla' + self.coretype[-1] + '.dat'
        claDatafile = 'dram_image.cla' + self.coretype[-1] + '.dat'
        self.genRamImage('.cla.text', self.secLmaDict['claTextStart'], self.secLmaDict['claTextEnd'], claTextfile, self.secBinPosDict['claTextStart'])
        self.genRamImage('.cla.data', self.secLmaDict['claDataStart'], self.secLmaDict['claDataEnd'], claDatafile, self.secBinPosDict['claDataStart'])
        self.genRamImage('.cla.bss' , self.secLmaDict['claBssStart'] , self.secLmaDict['claDataEnd'], claDatafile, self.secBinPosDict['claBssStart'] )

        xintfTextfile = 'xintf_iram_image.' + self.coretype + '.dat'
        xintfDatafile = 'xintf_dram_image.' + self.coretype + '.dat'
        self.genRamImage('.xintf.text', self.secLmaDict['xintfTextStart'], self.secLmaDict['xintfTextEnd'], xintfTextfile, self.secBinPosDict['xintfTextStart'])
        self.genRamImage('.xintf.data', self.secLmaDict['xintfDataStart'], self.secLmaDict['xintfDataEnd'], xintfDatafile, self.secBinPosDict['xintfDataStart'])
        self.genRamImage('.xintf.bss' , self.secLmaDict['xintfBssStart'] , self.secLmaDict['xintfDataEnd'], xintfDatafile, self.secBinPosDict['xintfBssStart'] )

        #self.copy4RtlSimulation(textfile, datafile, claTextfile, claDatafile)

        # clean up
        os.remove(self.outBin)

    def determineAdjustValue(self, symbolVals):
        symbols        = ['__data_start__', '__bss_start', '__cla_data_start__', '__cla_bss_start']
        dataSymbols    = ['__data_start__', '__bss_start']
        claDataSymbols = ['__cla_data_start__', '__cla_bss_start']

        adjustPos         = 0
        skipAdjustData    = False
        skipAdjustClaData = False

        del symbolVals['__data_end__']
        del symbolVals['__text_end__']
        del symbolVals['__cla_data_end__']
        del symbolVals['__cla_text_end__']

        if min(symbolVals, key=symbolVals.get) in symbols:
            if (min(symbolVals, key=symbolVals.get) in dataSymbols) and (symbolVals['__data_start__'] == symbolVals['__bss_start']):
                del symbolVals['__data_start__']
                del symbolVals['__bss_start']
                skipAdjustData = True

                if (min(symbolVals, key=symbolVals.get) in claDataSymbols) and (symbolVals['__cla_data_start__'] == symbolVals['__cla_bss_start']):
                    del symbolVals['__cla_data_start__']
                    del symbolVals['__cla_bss_start']
                    skipAdjustClaData = True
            
            if (min(symbolVals, key=symbolVals.get) in claDataSymbols) and (symbolVals['__cla_data_start__'] == symbolVals['__cla_bss_start']):
                del symbolVals['__cla_data_start__']
                del symbolVals['__cla_bss_start']
                skipAdjustClaData = True

                if (min(symbolVals, key=symbolVals.get) in dataSymbols) and (symbolVals['__data_start__'] == symbolVals['__bss_start']):
                    del symbolVals['__data_start__']
                    del symbolVals['__bss_start']
                    skipAdjustData = True

        adjustPos = symbolVals[min(symbolVals, key=symbolVals.get)]
        return adjustPos, skipAdjustData, skipAdjustClaData

    def getSectionRange(self):
        cmd = ["-t", self.inputexec]
        p = sp.Popen([self.objdump,*cmd], stdout=sp.PIPE)
        infos = p.stdout.readlines()

        symbolVals = {
            '__data_start__'    : self.INVALID_SYMBOL_VALUE,
            '__bss_start'       : self.INVALID_SYMBOL_VALUE,
            '__data_end__'      : self.INVALID_SYMBOL_VALUE,
            '__text_start__'    : self.INVALID_SYMBOL_VALUE,
            '__text_end__'      : self.INVALID_SYMBOL_VALUE,
            '__cla_data_start__': self.INVALID_SYMBOL_VALUE,
            '__cla_bss_start'   : self.INVALID_SYMBOL_VALUE,
            '__cla_data_end__'  : self.INVALID_SYMBOL_VALUE,
            '__cla_text_start__': self.INVALID_SYMBOL_VALUE,
            '__cla_text_end__'  : self.INVALID_SYMBOL_VALUE,

            '__xintf_data_start__' : self.INVALID_SYMBOL_VALUE,
            '__xintf_bss_start'    : self.INVALID_SYMBOL_VALUE,
            '__xintf_data_end__'   : self.INVALID_SYMBOL_VALUE,
            '__xintf_text_start__' : self.INVALID_SYMBOL_VALUE,
            '__xintf_text_end__'   : self.INVALID_SYMBOL_VALUE
        }

        ## get symbols' LMA
        for symbol in symbolVals.keys():
            valbytes = self.getSymbolValue(infos, str.encode(symbol), 0)
            symbolVals[symbol] = int((valbytes).decode(), 16)

        self.secLmaDict['dataStart'] = symbolVals['__data_start__']
        self.secLmaDict['bssStart']  = symbolVals['__bss_start']
        dataEnd = symbolVals['__data_end__']
        if dataEnd != self.INVALID_SYMBOL_VALUE:
            # align data section to 16-byte
            self.secLmaDict['dataEnd'] = dataEnd // 16 * 16
            if self.secLmaDict['dataEnd'] < dataEnd:
                self.secLmaDict['dataEnd'] = self.secLmaDict['dataEnd'] + 16
        else:
            self.secLmaDict['dataEnd'] = dataEnd

        self.secLmaDict['textStart'] = symbolVals['__text_start__']
        self.secLmaDict['textEnd']   = symbolVals['__text_end__']

        self.secLmaDict['claDataStart'] = symbolVals['__cla_data_start__']
        self.secLmaDict['claBssStart']  = symbolVals['__cla_bss_start']
        claDataEnd   = symbolVals['__cla_data_end__']
        if claDataEnd != self.INVALID_SYMBOL_VALUE:
            # align data section to 16-byte
            self.secLmaDict['claDataEnd'] = claDataEnd // 16 * 16
            if self.secLmaDict['claDataEnd'] < claDataEnd:
                self.secLmaDict['claDataEnd'] = self.secLmaDict['claDataEnd'] + 16
        else:
            self.secLmaDict['claDataEnd'] = claDataEnd

        self.secLmaDict['claTextStart'] = symbolVals['__cla_text_start__']
        self.secLmaDict['claTextEnd']   = symbolVals['__cla_text_end__']

        self.secLmaDict['xintfDataStart'] = symbolVals['__xintf_data_start__']
        self.secLmaDict['xintfBssStart']  = symbolVals['__xintf_bss_start']
        self.secLmaDict['xintfDataEnd']   = symbolVals['__xintf_data_end__']
        self.secLmaDict['xintfTextStart'] = symbolVals['__xintf_text_start__']
        self.secLmaDict['xintfTextEnd']   = symbolVals['__xintf_text_end__']

        ## adjust for .bss not occupy space
        adjustPos, skipAdjustData, skipAdjustClaData = self.determineAdjustValue(symbolVals)

        self.secBinPosDict = copy.deepcopy(self.secLmaDict)
        for k, v in self.secBinPosDict.items():
            if skipAdjustData and (k == 'dataStart' or k == 'bssStart' or k == 'dataEnd'):
                continue
            if skipAdjustClaData and (k == 'claDataStart' or k == 'claBssStart' or k == 'claDataEnd'):
                continue
            if v == self.INVALID_SYMBOL_VALUE:
                continue
            self.secBinPosDict[k] = v - adjustPos

        #print("\ngetSectionRange():")
        #for k, v in self.secLmaDict.items():
        #    print(k, hex(v))
        #print("\nadjustPos", hex(adjustPos))
        #print("skipAdjustData", skipAdjustData)
        #print("skipAdjustClaData", skipAdjustClaData, "\n")
        #for k, v in self.secBinPosDict.items():
        #    print(k, hex(v))

    def getSymbolValue(self, lines, token, pos):
        for line in lines:
            if line.find(token) > 0:
                infos = line.split()
                return infos[pos]
        #print("Warning:", token, "not found, return self.INVALID_SYMBOL_VALUE")
        return str.encode('0xFFFFFFFF')

if __name__=="__main__":
    versionStr = '1.0.9.20260108'

    parser = argparse.ArgumentParser(
        prog = 'gen_ram_image',
        description = 'generate IRAM and DRAM image for DSP application, v' + versionStr)
    parser.add_argument('--coretype',
                        help='which part of software to generate image, bootloader | core0 | core1')
    parser.add_argument('--inputexec', help='input DSP exectuable file, normally, with .out postfix')
    parser.add_argument('--toolbinpath', help='toolchain binary path')
    parser.add_argument('--linux', action='store_true', default=False, help='running environment is OS Linux')
    args = parser.parse_args()

    # use optional arguments so that user side knows arguments meaning better
    if args.coretype == None:
        print('ERROR: args.coretype not specified')
        sys.exit(-1)

    if args.inputexec == None:
        print('ERROR: args.inputexec not specified')
        sys.exit(-1)

    if args.toolbinpath == None:
        print('ERROR: args.toolbinpath not specified')
        sys.exit(-1)

    validCoreType = ['bootloader', 'core0', 'core1']
    if not args.coretype in validCoreType:
        print('ERROR: invalid args.coretype, `' + args.coretype +'`, expecting {bootloader | core0 | core1}')
        sys.exit(-1)

    ramImageGenerator = GenRamImage(args.coretype, args.inputexec, args.toolbinpath, args.linux)

    print("\nExtracting",  args.coretype, "image ... (v" + versionStr + ")")
    ramImageGenerator.generate()
    print("done.\n")

    sys.exit(0)

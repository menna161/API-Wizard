import getopt
import os
import re
import sys
import types
import random
import shutil
import struct
import string
import types
import urllib
import inspect
import datetime
import binascii
import itertools
import traceback
import pickle
import json
from operator import itemgetter
from collections import defaultdict, namedtuple
import cProfile
import pstats
import copy
import immlib as dbglib
from immlib import LogBpHook
from immutils import *
import time
import pykd
import windbglib as dbglib
from windbglib import LogBpHook
import copy, random, time
import sys
import sys
import traceback
import traceback


def findJOPGADGETS(modulecriteria={}, criteria={}, depth=6):
    '\n\tSearches for jop gadgets\n\n\tArguments:\n\tmodulecriteria - dictionary with criteria modules need to comply with.\n\t                 Default settings are : ignore aslr and rebased modules\n\tcriteria - dictionary with criteria the pointers need to comply with.\n\tdepth - maximum number of instructions to go back\n\t\n\tReturn:\n\tOutput is written to files, containing jop gadgets and suggestions\n\t'
    found_opcodes = {}
    all_opcodes = {}
    ptr_counter = 0
    modulestosearch = getModulesToQuery(modulecriteria)
    progressid = toHex(dbg.getDebuggedPid())
    progressfilename = (((('_jop_progress_' + dbg.getDebuggedName()) + '_') + progressid) + '.log')
    objprogressfile = MnLog(progressfilename)
    progressfile = objprogressfile.reset()
    dbg.log(('[+] Progress will be written to %s' % progressfilename))
    dbg.log(('[+] Max nr of instructions : %d' % depth))
    filesok = 0
    usefiles = False
    filestouse = []
    vplogtxt = ''
    suggestions = {}
    fast = False
    search = []
    jopregs = ['EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP']
    offsetval = 0
    for jreg in jopregs:
        search.append(('JMP ' + jreg))
        search.append((('JMP [' + jreg) + ']'))
        for offsetval in range(0, (40 + 1), 2):
            search.append((((('JMP [' + jreg) + '+0x') + toHexByte(offsetval)) + ']'))
    search.append('JMP [ESP]')
    for offsetval in range(0, (40 + 1), 2):
        search.append((('JMP [ESP+0x' + toHexByte(offsetval)) + ']'))
    dbg.log(('[+] Enumerating %d endings in %d module(s)...' % (len(search), len(modulestosearch))))
    for thismodule in modulestosearch:
        dbg.log(('    - Querying module %s' % thismodule))
        dbg.updateLog()
        found_opcodes = searchInModule(search, thismodule, criteria)
        all_opcodes = mergeOpcodes(all_opcodes, found_opcodes)
    dbg.log('    - Search complete :')
    dbg.updateLog()
    tp = 0
    for endingtype in all_opcodes:
        if (len(all_opcodes[endingtype]) > 0):
            if usefiles:
                dbg.log(('       Ending : %s, Nr found : %d' % (endingtype, (len(all_opcodes[endingtype]) / 2))))
                tp = (tp + (len(all_opcodes[endingtype]) / 2))
            else:
                dbg.log(('       Ending : %s, Nr found : %d' % (endingtype, len(all_opcodes[endingtype]))))
                tp = (tp + len(all_opcodes[endingtype]))
    global silent
    dbg.log(('    - Filtering and mutating %d gadgets' % tp))
    dbg.updateLog()
    jopgadgets = {}
    interestinggadgets = {}
    adcnt = 0
    tc = 1
    issafeseh = False
    step = 0
    for endingtype in all_opcodes:
        if (len(all_opcodes[endingtype]) > 0):
            for endingtypeptr in all_opcodes[endingtype]:
                adcnt += 1
                if usefiles:
                    adcnt = (adcnt - 0.5)
                if (adcnt > (tc * 1000)):
                    thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
                    updatetext = (((((((('      - Progress update : ' + str((tc * 1000))) + ' / ') + str(tp)) + ' items processed (') + thistimestamp) + ') - (') + str((((tc * 1000) * 100) / tp))) + '%)')
                    objprogressfile.write(updatetext.strip(), progressfile)
                    dbg.log(updatetext)
                    dbg.updateLog()
                    tc += 1
                thisopcode = dbg.disasmBackward(endingtypeptr, (depth + 1))
                thisptr = thisopcode.getAddress()
                startptr = thisptr
                while ((startptr <= endingtypeptr) and (startptr != 0)):
                    thischain = ''
                    msfchain = []
                    thisopcodebytes = ''
                    chainptr = startptr
                    if (isGoodGadgetPtr(startptr, criteria) and (not (startptr in jopgadgets)) and (not (startptr in interestinggadgets))):
                        invalidinstr = False
                        while ((chainptr < endingtypeptr) and (not invalidinstr)):
                            thisopcode = dbg.disasm(chainptr)
                            thisinstruction = getDisasmInstruction(thisopcode)
                            if (isGoodJopGadgetInstr(thisinstruction) and (not isGadgetEnding(thisinstruction, search))):
                                thischain = ((thischain + ' # ') + thisinstruction)
                                msfchain.append([chainptr, thisinstruction])
                                thisopcodebytes = (thisopcodebytes + opcodesToHex(thisopcode.getDump().lower()))
                                chainptr = dbg.disasmForwardAddressOnly(chainptr, 1)
                            else:
                                invalidinstr = True
                        if ((endingtypeptr == chainptr) and (startptr != chainptr) and (not invalidinstr)):
                            fullchain = ((thischain + ' # ') + endingtype)
                            msfchain.append([endingtypeptr, endingtype])
                            thisopcode = dbg.disasm(endingtypeptr)
                            thisopcodebytes = (thisopcodebytes + opcodesToHex(thisopcode.getDump().lower()))
                            msfchain.append(['raw', thisopcodebytes])
                            if isInterestingJopGadget(fullchain):
                                interestinggadgets[startptr] = fullchain
                            elif (not fast):
                                jopgadgets[startptr] = fullchain
                    startptr = (startptr + 1)
    thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
    updatetext = (((((('      - Progress update : ' + str(tp)) + ' / ') + str(tp)) + ' items processed (') + thistimestamp) + ') - (100%)')
    objprogressfile.write(updatetext.strip(), progressfile)
    dbg.log(updatetext)
    dbg.updateLog()
    logfile = MnLog('jop.txt')
    thislog = logfile.reset()
    objprogressfile.write('Enumerating gadgets', progressfile)
    dbg.log((((('[+] Writing results to file ' + thislog) + ' (') + str(len(interestinggadgets))) + ' interesting gadgets)'))
    logfile.write('Interesting gadgets', thislog)
    logfile.write('-------------------', thislog)
    dbg.updateLog()
    arrtowrite = ''
    try:
        with open(thislog, 'a') as fh:
            arrtowrite = ''
            for gadget in interestinggadgets:
                ptrx = MnPointer(gadget)
                modname = ptrx.belongsTo()
                modinfo = MnModule(modname)
                ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + interestinggadgets[gadget]) + '    ** ') + modinfo.__str__()) + ' **   |  ') + ptrx.__str__()) + '\n')
                arrtowrite += ptrinfo
            objprogressfile.write((((('Writing results to file ' + thislog) + ' (') + str(len(interestinggadgets))) + ' interesting gadgets)'), progressfile)
            fh.writelines(arrtowrite)
    except:
        pass
    return (interestinggadgets, jopgadgets, suggestions, vplogtxt)

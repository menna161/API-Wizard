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


def findROPGADGETS(modulecriteria={}, criteria={}, endings=[], maxoffset=40, depth=5, split=False, pivotdistance=0, fast=False, mode='all', sortedprint=False, technique=''):
    '\n\tSearches for rop gadgets\n\n\tArguments:\n\tmodulecriteria - dictionary with criteria modules need to comply with.\n\t                 Default settings are : ignore aslr and rebased modules\n\tcriteria - dictionary with criteria the pointers need to comply with.\n\tendings - array with all rop gadget endings to look for. Default : RETN and RETN+offsets\n\tmaxoffset - maximum offset value for RETN if endings are set to RETN\n\tdepth - maximum number of instructions to go back\n\tsplit - Boolean that indicates whether routine should write all gadgets to one file, or split per module\n\tpivotdistance - minimum distance a stackpivot needs to be\n\tfast - Boolean indicating if you want to process less obvious gadgets as well\n\tmode - internal use only\n\tsortedprint - sort pointers before printing output to rop.txt\n\ttechnique - create all chains if empty. otherwise, create virtualalloc or virtualprotect chain (based on what is specified)\n\t\n\tReturn:\n\tOutput is written to files, containing rop gadgets, suggestions, stack pivots and virtualprotect/virtualalloc routine (if possible)\n\t'
    found_opcodes = {}
    all_opcodes = {}
    ptr_counter = 0
    valid_techniques = ['virtualalloc', 'virtualprotect']
    modulestosearch = getModulesToQuery(modulecriteria)
    progressid = str(dbg.getDebuggedPid())
    progressfilename = (((('_rop_progress_' + dbg.getDebuggedName()) + '_') + progressid) + '.log')
    objprogressfile = MnLog(progressfilename)
    progressfile = objprogressfile.reset()
    dbg.log(('[+] Progress will be written to %s' % progressfilename))
    dbg.log(('[+] Maximum offset : %d' % maxoffset))
    dbg.log(('[+] (Minimum/optional maximum) stackpivot distance : %s' % str(pivotdistance)))
    dbg.log(('[+] Max nr of instructions : %d' % depth))
    dbg.log(('[+] Split output into module rop files ? %s' % split))
    if ((technique != '') and (technique in valid_techniques)):
        dbg.log(("[+] Only creating rop chain for '%s'" % technique))
    else:
        dbg.log(('[+] Going to create rop chains for all relevant/supported techniques: %s' % technique))
    usefiles = False
    filestouse = []
    vplogtxt = ''
    suggestions = {}
    if ('f' in criteria):
        if (criteria['f'] != ''):
            if (type(criteria['f']).__name__.lower() != 'bool'):
                usefiles = True
                rawfilenames = criteria['f'].replace('"', '')
                allfiles = [getAbsolutePath(f) for f in rawfilenames.split(',')]
                dbg.log(('[+] Attempting to use %d rop file(s) as input' % len(allfiles)))
                for fname in allfiles:
                    fname = fname.strip()
                    if (not os.path.exists(fname)):
                        dbg.log(('     ** %s : Does not exist !' % fname), highlight=1)
                    else:
                        filestouse.append(fname)
                if (len(filestouse) == 0):
                    dbg.log(' ** Unable to find any of the source files, aborting... **', highlight=1)
                    return
    search = []
    if (not usefiles):
        if (len(endings) == 0):
            search.append('RETN')
            for i in range(0, (maxoffset + 1), 2):
                search.append(('RETN 0x' + toHexByte(i)))
        else:
            for ending in endings:
                dbg.log(('[+] Custom ending : %s' % ending))
                if (ending != ''):
                    search.append(ending)
        if (len(modulestosearch) == 0):
            dbg.log('[-] No modules selected, aborting search', highlight=1)
            return
        dbg.log(('[+] Enumerating %d endings in %d module(s)...' % (len(search), len(modulestosearch))))
        for thismodule in modulestosearch:
            dbg.log(('    - Querying module %s' % thismodule))
            dbg.updateLog()
            found_opcodes = searchInModule(search, thismodule, criteria)
            all_opcodes = mergeOpcodes(all_opcodes, found_opcodes)
        dbg.log('    - Search complete :')
    else:
        dbg.log('[+] Reading input files')
        for filename in filestouse:
            dbg.log(('     - Reading %s' % filename))
            all_opcodes = mergeOpcodes(all_opcodes, readGadgetsFromFile(filename))
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
    if (not usefiles):
        dbg.log(('    - Filtering and mutating %d gadgets' % tp))
    else:
        dbg.log(('    - Categorizing %d gadgets' % tp))
        silent = True
    dbg.updateLog()
    ropgadgets = {}
    interestinggadgets = {}
    stackpivots = {}
    stackpivots_safeseh = {}
    adcnt = 0
    tc = 1
    issafeseh = False
    step = 0
    updateth = 1000
    if ((tp >= 2000) and (tp < 5000)):
        updateth = 500
    if (tp < 2000):
        updateth = 100
    for endingtype in all_opcodes:
        if (len(all_opcodes[endingtype]) > 0):
            for endingtypeptr in all_opcodes[endingtype]:
                adcnt = (adcnt + 1)
                if usefiles:
                    adcnt = (adcnt - 0.5)
                if (adcnt > (tc * updateth)):
                    thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
                    updatetext = (((((((('      - Progress update : ' + str((tc * updateth))) + ' / ') + str(tp)) + ' items processed (') + thistimestamp) + ') - (') + str((((tc * updateth) * 100) / tp))) + '%)')
                    objprogressfile.write(updatetext.strip(), progressfile)
                    dbg.log(updatetext)
                    dbg.updateLog()
                    tc += 1
                if (not usefiles):
                    try:
                        thisopcode = dbg.disasmBackward(endingtypeptr, (depth + 1))
                        thisptr = thisopcode.getAddress()
                    except:
                        dbg.log(('        ** Unable to backward disassemble at 0x%0x, depth %d, skipping location\n' % (endingtypeptr, (depth + 1))))
                        thisopcode = ''
                        thisptr = 0
                    startptr = thisptr
                    currentmodulename = MnPointer(thisptr).belongsTo()
                    modinfo = MnModule(currentmodulename)
                    issafeseh = modinfo.isSafeSEH
                    while ((startptr <= endingtypeptr) and (startptr != 0)):
                        thischain = ''
                        msfchain = []
                        thisopcodebytes = ''
                        chainptr = startptr
                        if (isGoodGadgetPtr(startptr, criteria) and (not (startptr in ropgadgets)) and (not (startptr in interestinggadgets))):
                            invalidinstr = False
                            while ((chainptr < endingtypeptr) and (not invalidinstr)):
                                thisopcode = dbg.disasm(chainptr)
                                thisinstruction = getDisasmInstruction(thisopcode)
                                if (isGoodGadgetInstr(thisinstruction) and (not isGadgetEnding(thisinstruction, search))):
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
                                if isInterestingGadget(fullchain):
                                    interestinggadgets[startptr] = fullchain
                                    stackpivotdistance = getStackPivotDistance(fullchain, pivotdistance)
                                    if (stackpivotdistance > 0):
                                        if issafeseh:
                                            if (not (stackpivotdistance in stackpivots_safeseh)):
                                                stackpivots_safeseh.setdefault(stackpivotdistance, [[startptr, fullchain]])
                                            else:
                                                stackpivots_safeseh[stackpivotdistance] += [[startptr, fullchain]]
                                        elif (not (stackpivotdistance in stackpivots)):
                                            stackpivots.setdefault(stackpivotdistance, [[startptr, fullchain]])
                                        else:
                                            stackpivots[stackpivotdistance] += [[startptr, fullchain]]
                                elif (not fast):
                                    ropgadgets[startptr] = fullchain
                        startptr = (startptr + 1)
                else:
                    if (step == 0):
                        startptr = endingtypeptr
                    if (step == 1):
                        thischain = endingtypeptr
                        chainptr = startptr
                        ptrx = MnPointer(chainptr)
                        modname = ptrx.belongsTo()
                        issafeseh = False
                        if (modname != ''):
                            thism = MnModule(modname)
                            issafeseh = thism.isSafeSEH
                        if (isGoodGadgetPtr(startptr, criteria) and (not (startptr in ropgadgets)) and (not (startptr in interestinggadgets))):
                            fullchain = thischain
                            if isInterestingGadget(fullchain):
                                interestinggadgets[startptr] = fullchain
                                stackpivotdistance = getStackPivotDistance(fullchain, pivotdistance)
                                if (stackpivotdistance > 0):
                                    if issafeseh:
                                        if (not (stackpivotdistance in stackpivots_safeseh)):
                                            stackpivots_safeseh.setdefault(stackpivotdistance, [[startptr, fullchain]])
                                        else:
                                            stackpivots_safeseh[stackpivotdistance] += [[startptr, fullchain]]
                                    elif (not (stackpivotdistance in stackpivots)):
                                        stackpivots.setdefault(stackpivotdistance, [[startptr, fullchain]])
                                    else:
                                        stackpivots[stackpivotdistance] += [[startptr, fullchain]]
                            elif (not fast):
                                ropgadgets[startptr] = fullchain
                        step = (- 1)
                    step += 1
    thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
    updatetext = (((((('      - Progress update : ' + str(tp)) + ' / ') + str(tp)) + ' items processed (') + thistimestamp) + ') - (100%)')
    objprogressfile.write(updatetext.strip(), progressfile)
    dbg.log(updatetext)
    dbg.updateLog()
    if (mode == 'all'):
        if ((len(ropgadgets) > 0) and (len(interestinggadgets) > 0)):
            updatetext = '[+] Creating suggestions list'
            dbg.log(updatetext)
            objprogressfile.write(updatetext.strip(), progressfile)
            suggestions = getRopSuggestion(interestinggadgets, ropgadgets)
            updatetext = '[+] Processing suggestions'
            dbg.log(updatetext)
            objprogressfile.write(updatetext.strip(), progressfile)
            suggtowrite = ''
            for suggestedtype in suggestions:
                limitnr = 2147483647
                if suggestedtype.startswith('pop '):
                    limitnr = 10
                gcnt = 0
                suggtowrite += ('[%s]\n' % suggestedtype)
                for suggestedpointer in suggestions[suggestedtype]:
                    if (gcnt < limitnr):
                        sptr = MnPointer(suggestedpointer)
                        modname = sptr.belongsTo()
                        modinfo = MnModule(modname)
                        if (not (modinfo.moduleBase.__class__.__name__ == 'instancemethod')):
                            rva = (suggestedpointer - modinfo.moduleBase)
                        suggesteddata = suggestions[suggestedtype][suggestedpointer]
                        if (not (modinfo.moduleBase.__class__.__name__ == 'instancemethod')):
                            ptrinfo = (((((((((('0x' + toHex(suggestedpointer)) + ' (RVA : 0x') + toHex(rva)) + ') : ') + suggesteddata) + '    ** [') + modname) + '] **   |  ') + sptr.__str__()) + '\n')
                        else:
                            ptrinfo = (((((((('0x' + toHex(suggestedpointer)) + ' : ') + suggesteddata) + '    ** [') + modname) + '] **   |  ') + sptr.__str__()) + '\n')
                        suggtowrite += ptrinfo
                    else:
                        break
                    gcnt += 1
            if (arch == 32):
                dbg.log('[+] Launching ROP generator')
                updatetext = 'Attempting to create rop chain proposals'
                objprogressfile.write(updatetext.strip(), progressfile)
                vplogtxt = createRopChains(suggestions, interestinggadgets, ropgadgets, modulecriteria, criteria, objprogressfile, progressfile, technique)
                dbg.logLines(vplogtxt.replace('\t', '    '))
                dbg.log('    ROP generator finished')
        else:
            updatetext = '[+] Oops, no gadgets found, aborting..'
            dbg.log(updatetext)
            objprogressfile.write(updatetext.strip(), progressfile)
    dbg.setStatusBar('Writing to logfiles...')
    dbg.log('')
    logfile = MnLog('stackpivot.txt')
    thislog = logfile.reset()
    objprogressfile.write(((((('Writing ' + str((len(stackpivots) + len(stackpivots_safeseh)))) + ' stackpivots with minimum offset ') + str(pivotdistance)) + ' to file ') + thislog), progressfile)
    dbg.log(('[+] Writing stackpivots to file ' + thislog))
    logfile.write((('Stack pivots, minimum distance ' + str(pivotdistance)) + ', in descending order'), thislog)
    logfile.write('------------------------------------------------------------------------------', thislog)
    logfile.write('', thislog)
    logfile.write('', thislog)
    logfile.write('Non-SafeSEH protected pivots :', thislog)
    logfile.write('------------------------------', thislog)
    logfile.write('', thislog)
    arrtowrite = ''
    pivotcount = 0
    try:
        with open(thislog, 'a') as fh:
            arrtowrite = ''
            stackpivots_index = sorted(stackpivots, reverse=True)
            for sdist in stackpivots_index:
                for (spivot, schain) in stackpivots[sdist]:
                    ptrx = MnPointer(spivot)
                    modname = ptrx.belongsTo()
                    sdisthex = ('%02x' % sdist)
                    ptrinfo = (((((((((((('0x' + toHex(spivot)) + ' : {pivot ') + str(sdist)) + ' / 0x') + sdisthex) + '} : ') + schain) + '    ** [') + modname) + '] **   |  ') + ptrx.__str__()) + '\n')
                    pivotcount += 1
                    arrtowrite += ptrinfo
            fh.writelines(arrtowrite)
    except:
        pass
    logfile.write('', thislog)
    logfile.write('', thislog)
    logfile.write('', thislog)
    logfile.write('**********************************************************************************************************', thislog)
    logfile.write('', thislog)
    logfile.write('', thislog)
    logfile.write('', thislog)
    logfile.write('SafeSEH protected pivots :', thislog)
    logfile.write('--------------------------', thislog)
    logfile.write('', thislog)
    arrtowrite = ''
    try:
        with open(thislog, 'a') as fh:
            arrtowrite = ''
            stackpivots_safeseh_index = sorted(stackpivots_safeseh, reverse=True)
            for sdist in stackpivots_safeseh_index:
                for (spivot, schain) in stackpivots_safeseh[sdist]:
                    ptrx = MnPointer(spivot)
                    modname = ptrx.belongsTo()
                    sdisthex = ('%02x' % sdist)
                    ptrinfo = (((((((((((('0x' + toHex(spivot)) + ' : {pivot ') + str(sdist)) + ' / 0x') + sdisthex) + '} : ') + schain) + '    ** [') + modname) + '] SafeSEH **   |  ') + ptrx.__str__()) + '\n')
                    pivotcount += 1
                    arrtowrite += ptrinfo
            fh.writelines(arrtowrite)
    except:
        pass
    dbg.log(('    Wrote %d pivots to file ' % pivotcount))
    arrtowrite = ''
    if (mode == 'all'):
        if (len(suggestions) > 0):
            logfile = MnLog('rop_suggestions.txt')
            thislog = logfile.reset()
            objprogressfile.write(('Writing all suggestions to file ' + thislog), progressfile)
            dbg.log(('[+] Writing suggestions to file ' + thislog))
            logfile.write('Suggestions', thislog)
            logfile.write('-----------', thislog)
            with open(thislog, 'a') as fh:
                fh.writelines(suggtowrite)
                fh.write('\n')
            nrsugg = len(suggtowrite.split('\n'))
            dbg.log(('    Wrote %d suggestions to file' % nrsugg))
        if (not split):
            logfile = MnLog('rop.txt')
            thislog = logfile.reset()
            objprogressfile.write('Gathering interesting gadgets', progressfile)
            dbg.log((((('[+] Writing results to file ' + thislog) + ' (') + str(len(interestinggadgets))) + ' interesting gadgets)'))
            logfile.write('Interesting gadgets', thislog)
            logfile.write('-------------------', thislog)
            dbg.updateLog()
            try:
                with open(thislog, 'a') as fh:
                    arrtowrite = ''
                    if sortedprint:
                        arrptrs = []
                        dbg.log('    Sorting interesting gadgets first')
                        for gadget in interestinggadgets:
                            arrptrs.append(gadget)
                        arrptrs.sort()
                        dbg.log("    Done sorting, let's go")
                        for gadget in arrptrs:
                            ptrx = MnPointer(gadget)
                            modname = ptrx.belongsTo()
                            ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + interestinggadgets[gadget]) + '    ** [') + modname) + '] **   |  ') + ptrx.__str__()) + '\n')
                            arrtowrite += ptrinfo
                    else:
                        for gadget in interestinggadgets:
                            ptrx = MnPointer(gadget)
                            modname = ptrx.belongsTo()
                            ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + interestinggadgets[gadget]) + '    ** [') + modname) + '] **   |  ') + ptrx.__str__()) + '\n')
                            arrtowrite += ptrinfo
                    objprogressfile.write((((('Writing results to file ' + thislog) + ' (') + str(len(interestinggadgets))) + ' interesting gadgets)'), progressfile)
                    fh.writelines(arrtowrite)
                dbg.log(('    Wrote %d interesting gadgets to file' % len(interestinggadgets)))
            except:
                pass
            arrtowrite = ''
            if (not fast):
                objprogressfile.write((('Enumerating other gadgets (' + str(len(ropgadgets))) + ')'), progressfile)
                dbg.log((((('[+] Writing other gadgets to file ' + thislog) + ' (') + str(len(ropgadgets))) + ' gadgets)'))
                try:
                    logfile.write('', thislog)
                    logfile.write('Other gadgets', thislog)
                    logfile.write('-------------', thislog)
                    with open(thislog, 'a') as fh:
                        arrtowrite = ''
                        if sortedprint:
                            arrptrs = []
                            dbg.log('    Sorting other gadgets too')
                            for gadget in ropgadgets:
                                arrptrs.append(gadget)
                            arrptrs.sort()
                            dbg.log("    Done sorting, let's go")
                            for gadget in arrptrs:
                                ptrx = MnPointer(gadget)
                                modname = ptrx.belongsTo()
                                ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + ropgadgets[gadget]) + '    ** [') + modname) + '] **   |  ') + ptrx.__str__()) + '\n')
                                arrtowrite += ptrinfo
                        else:
                            for gadget in ropgadgets:
                                ptrx = MnPointer(gadget)
                                modname = ptrx.belongsTo()
                                ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + ropgadgets[gadget]) + '    ** [') + modname) + '] **   |  ') + ptrx.__str__()) + '\n')
                                arrtowrite += ptrinfo
                        dbg.log(('    Wrote %d other gadgets to file' % len(ropgadgets)))
                        objprogressfile.write((((('Writing results to file ' + thislog) + ' (') + str(len(ropgadgets))) + ' other gadgets)'), progressfile)
                        fh.writelines(arrtowrite)
                except:
                    pass
        else:
            dbg.log('[+] Writing results to individual files (grouped by module)')
            dbg.updateLog()
            for thismodule in modulestosearch:
                thismodname = thismodule.replace(' ', '_')
                thismodversion = getModuleProperty(thismodule, 'version')
                logfile = MnLog((((('rop_' + thismodname) + '_') + thismodversion) + '.txt'))
                thislog = logfile.reset()
                logfile.write('Interesting gadgets', thislog)
                logfile.write('-------------------', thislog)
            for gadget in interestinggadgets:
                ptrx = MnPointer(gadget)
                modname = ptrx.belongsTo()
                modinfo = MnModule(modname)
                thismodversion = getModuleProperty(modname, 'version')
                thismodname = modname.replace(' ', '_')
                logfile = MnLog((((('rop_' + thismodname) + '_') + thismodversion) + '.txt'))
                thislog = logfile.reset(False)
                ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + interestinggadgets[gadget]) + '    ** ') + modinfo.__str__()) + ' **   |  ') + ptrx.__str__()) + '\n')
                with open(thislog, 'a') as fh:
                    fh.write(ptrinfo)
            if (not fast):
                for thismodule in modulestosearch:
                    thismodname = thismodule.replace(' ', '_')
                    thismodversion = getModuleProperty(thismodule, 'version')
                    logfile = MnLog((((('rop_' + thismodname) + '_') + thismodversion) + '.txt'))
                    logfile.write('Other gadgets', thislog)
                    logfile.write('-------------', thislog)
                for gadget in ropgadgets:
                    ptrx = MnPointer(gadget)
                    modname = ptrx.belongsTo()
                    modinfo = MnModule(modname)
                    thismodversion = getModuleProperty(modname, 'version')
                    thismodname = modname.replace(' ', '_')
                    logfile = MnLog((((('rop_' + thismodname) + '_') + thismodversion) + '.txt'))
                    thislog = logfile.reset(False)
                    ptrinfo = (((((((('0x' + toHex(gadget)) + ' : ') + ropgadgets[gadget]) + '    ** ') + modinfo.__str__()) + ' **   |  ') + ptrx.__str__()) + '\n')
                    with open(thislog, 'a') as fh:
                        fh.write(ptrinfo)
    thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
    objprogressfile.write((('Done (' + thistimestamp) + ')'), progressfile)
    dbg.log('Done')
    return (interestinggadgets, ropgadgets, suggestions, vplogtxt)

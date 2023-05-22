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


def createRopChains(suggestions, interestinggadgets, allgadgets, modulecriteria, criteria, objprogressfile, progressfile, technique):
    '\n\tWill attempt to produce ROP chains\n\t'
    global ptr_to_get
    global ptr_counter
    global silent
    global noheader
    global ignoremodules
    vplogtxt = ''
    showrva = False
    if ('rva' in criteria):
        showrva = True
    routinedefs = {}
    routinesetup = {}
    virtualprotect = [['esi', 'api'], ['ebp', 'jmp esp'], ['ebx', 513], ['edx', 64], ['ecx', '&?W'], ['edi', 'ropnop'], ['eax', 'nop']]
    virtualalloc = [['esi', 'api'], ['ebp', 'jmp esp'], ['ebx', 1], ['edx', 4096], ['ecx', 64], ['edi', 'ropnop'], ['eax', 'nop']]
    setinformationprocess = [['ebp', 'api'], ['edx', 34], ['ecx', '&', '0x00000002'], ['ebx', 4294967295], ['eax', 4], ['edi', 'pop']]
    setprocessdeppolicy = [['ebp', 'api'], ['ebx', '&', '0x00000000'], ['edi', 'pop']]
    routinedefs['VirtualProtect'] = virtualprotect
    routinedefs['VirtualAlloc'] = virtualalloc
    osver = dbg.getOsVersion()
    if (not ((osver == '6') or (osver == '7') or (osver == '8') or (osver == '10') or (osver == '11') or (osver == 'vista') or (osver == 'win7') or (osver == '2008server') or (osver == 'win8') or (osver == 'win8.1') or (osver == 'win10'))):
        routinedefs['SetInformationProcess'] = setinformationprocess
        routinedefs['SetProcessDEPPolicy'] = setprocessdeppolicy
    modulestosearch = getModulesToQuery(modulecriteria)
    routinesetup['VirtualProtect'] = '--------------------------------------------\n EAX = NOP (0x90909090)\n ECX = lpOldProtect (ptr to W address)\n EDX = NewProtect (0x40)\n EBX = dwSize\n ESP = lPAddress (automatic)\n EBP = ReturnTo (ptr to jmp esp)\n ESI = ptr to VirtualProtect()\n EDI = ROP NOP (RETN)\n --- alternative chain ---\n EAX = ptr to &VirtualProtect()\n ECX = lpOldProtect (ptr to W address)\n EDX = NewProtect (0x40)\n EBX = dwSize\n ESP = lPAddress (automatic)\n EBP = POP (skip 4 bytes)\n ESI = ptr to JMP [EAX]\n EDI = ROP NOP (RETN)\n + place ptr to "jmp esp" on stack, below PUSHAD\n--------------------------------------------'
    routinesetup['VirtualAlloc'] = '--------------------------------------------\n EAX = NOP (0x90909090)\n ECX = flProtect (0x40)\n EDX = flAllocationType (0x1000)\n EBX = dwSize\n ESP = lpAddress (automatic)\n EBP = ReturnTo (ptr to jmp esp)\n ESI = ptr to VirtualAlloc()\n EDI = ROP NOP (RETN)\n --- alternative chain ---\n EAX = ptr to &VirtualAlloc()\n ECX = flProtect (0x40)\n EDX = flAllocationType (0x1000)\n EBX = dwSize\n ESP = lpAddress (automatic)\n EBP = POP (skip 4 bytes)\n ESI = ptr to JMP [EAX]\n EDI = ROP NOP (RETN)\n + place ptr to "jmp esp" on stack, below PUSHAD\n--------------------------------------------'
    routinesetup['SetInformationProcess'] = '--------------------------------------------\n EAX = SizeOf(ExecuteFlags) (0x4)\n ECX = &ExecuteFlags (ptr to 0x00000002)\n EDX = ProcessExecuteFlags (0x22)\n EBX = NtCurrentProcess (0xffffffff)\n ESP = ReturnTo (automatic)\n EBP = ptr to NtSetInformationProcess()\n ESI = <not used>\n EDI = ROP NOP (4 byte stackpivot)\n--------------------------------------------'
    routinesetup['SetProcessDEPPolicy'] = '--------------------------------------------\n EAX = <not used>\n ECX = <not used>\n EDX = <not used>\n EBX = dwFlags (ptr to 0x00000000)\n ESP = ReturnTo (automatic)\n EBP = ptr to SetProcessDEPPolicy()\n ESI = <not used>\n EDI = ROP NOP (4 byte stackpivot)\n--------------------------------------------'
    updatetxt = ''
    validatedroutinedefs = {}
    if (technique != ''):
        for routine in routinedefs:
            if (technique.lower() == routine.lower()):
                validatedroutinedefs[routine] = routinedefs[routine]
        routinedefs = validatedroutinedefs
    for routine in routinedefs:
        thischain = {}
        updatetxt = ('Attempting to produce rop chain for %s' % routine)
        dbg.log(('[+] %s' % updatetxt))
        objprogressfile.write(('- ' + updatetxt), progressfile)
        vplogtxt += '\n'
        vplogtxt += ('#' * 80)
        vplogtxt += (((('\n\nRegister setup for ' + routine) + '() :\n') + routinesetup[routine]) + '\n\n')
        targetOS = '(XP/2003 Server and up)'
        if (routine == 'SetInformationProcess'):
            targetOS = '(XP/2003 Server only)'
        if (routine == 'SetProcessDEPPolicy'):
            targetOS = '(XP SP3/Vista SP1/2008 Server SP1, can be called only once per process)'
        title = ('ROP Chain for %s() [%s] :' % (routine, targetOS))
        vplogtxt += ('\n%s\n' % title)
        vplogtxt += (('-' * len(title)) + '\n\n')
        vplogtxt += '*** [ Ruby ] ***\n\n'
        vplogtxt += '  def create_rop_chain()\n'
        vplogtxt += '\n    # rop chain generated with mona.py - www.corelan.be'
        vplogtxt += '\n    rop_gadgets = \n'
        vplogtxt += '    [\n'
        thischaintxt = ''
        dbg.updateLog()
        modused = {}
        skiplist = []
        replacelist = {}
        toadd = {}
        movetolast = []
        regsequences = []
        stepcnt = 1
        for step in routinedefs[routine]:
            thisreg = step[0]
            thistarget = step[1]
            if (thisreg in replacelist):
                thistarget = replacelist[thisreg]
            thistimestamp = datetime.datetime.now().strftime('%a %Y/%m/%d %I:%M:%S %p')
            dbg.log(('    %s: Step %d/%d: %s' % (thistimestamp, stepcnt, len(routinedefs[routine]), thisreg)))
            stepcnt += 1
            if (not (thisreg in skiplist)):
                regsequences.append(thisreg)
                if (str(thistarget) == 'api'):
                    objprogressfile.write('  * Enumerating ROPFunc info (IAT Query)', progressfile)
                    (funcptr, functext) = getRopFuncPtr(routine, modulecriteria, criteria, 'iat', objprogressfile, progressfile)
                    if ((routine == 'SetProcessDEPPolicy') and (funcptr == 0)):
                        (funcptr, functext) = getRopFuncPtr(routine, modulecriteria, criteria, 'eat', objprogressfile, progressfile)
                        extra = ''
                        if (funcptr == 0):
                            extra = '[-] Unable to find ptr to '
                            thischain[thisreg] = [[0, ((((extra + routine) + '() (-> to be put in ') + thisreg) + ')'), 0]]
                        else:
                            thischain[thisreg] = putValueInReg(thisreg, funcptr, (((routine + '() [') + MnPointer(funcptr).belongsTo()) + ']'), suggestions, interestinggadgets, criteria)
                    else:
                        objprogressfile.write(('    Function pointer : 0x%0x' % funcptr), progressfile)
                        objprogressfile.write('  * Getting pickup gadget', progressfile)
                        (thischain[thisreg], skiplist) = getPickupGadget(thisreg, funcptr, functext, suggestions, interestinggadgets, criteria, modulecriteria, routine)
                        if (len(skiplist) > 0):
                            if ((routine.lower() == 'virtualprotect') or (routine.lower() == 'virtualalloc')):
                                replacelist['ebp'] = 'pop'
                                oldsilent = silent
                                silent = True
                                ptr_counter = 0
                                ptr_to_get = 3
                                jmpreg = findJMP(modulecriteria, criteria, 'esp')
                                ptr_counter = 0
                                ptr_to_get = (- 1)
                                jmpptr = 0
                                jmptype = ''
                                silent = oldsilent
                                total = getNrOfDictElements(jmpreg)
                                if (total > 0):
                                    ptrindex = random.randint(1, total)
                                    indexcnt = 1
                                    for regtype in jmpreg:
                                        for ptr in jmpreg[regtype]:
                                            if (indexcnt == ptrindex):
                                                jmpptr = ptr
                                                jmptype = regtype
                                                break
                                            indexcnt += 1
                                if (jmpptr > 0):
                                    toadd[thistarget] = [jmpptr, (("ptr to '" + jmptype) + "'")]
                                else:
                                    toadd[thistarget] = [jmpptr, "ptr to 'jmp esp'"]
                                movetolast.append(thisreg)
                if str(thistarget).startswith('jmp'):
                    targetreg = str(thistarget).split(' ')[1]
                    oldsilent = silent
                    silent = True
                    ptr_counter = 0
                    ptr_to_get = 3
                    jmpreg = findJMP(modulecriteria, criteria, targetreg)
                    ptr_counter = 0
                    ptr_to_get = (- 1)
                    jmpptr = 0
                    jmptype = ''
                    silent = oldsilent
                    total = getNrOfDictElements(jmpreg)
                    if (total > 0):
                        ptrindex = random.randint(1, total)
                        indexcnt = 1
                        for regtype in jmpreg:
                            for ptr in jmpreg[regtype]:
                                if (indexcnt == ptrindex):
                                    jmpptr = ptr
                                    jmptype = regtype
                                    break
                                indexcnt += 1
                    jmpinfo = ''
                    jmpmodinfo = ''
                    if (jmpptr == 0):
                        jmptype = ''
                        jmpinfo = "Unable to find ptr to 'JMP ESP'"
                    else:
                        jmpinfo = MnPointer(jmpptr).belongsTo()
                        tmod = MnModule(jmpinfo)
                        jmpmodinfo = getGadgetAddressInfo(jmpptr)
                    thischain[thisreg] = putValueInReg(thisreg, jmpptr, ((((('& ' + jmptype) + ' [') + jmpinfo) + ']') + jmpmodinfo), suggestions, interestinggadgets, criteria)
                if (str(thistarget) == 'ropnop'):
                    ropptr = 0
                    for poptype in suggestions:
                        if poptype.startswith('pop '):
                            for retptr in suggestions[poptype]:
                                if ((getOffset(interestinggadgets[retptr]) == 0) and (interestinggadgets[retptr].count('#') == 2)):
                                    ropptr = (retptr + 1)
                                    break
                        if poptype.startswith('inc '):
                            for retptr in suggestions[poptype]:
                                if ((getOffset(interestinggadgets[retptr]) == 0) and (interestinggadgets[retptr].count('#') == 2)):
                                    ropptr = (retptr + 1)
                                    break
                        if poptype.startswith('dec '):
                            for retptr in suggestions[poptype]:
                                if ((getOffset(interestinggadgets[retptr]) == 0) and (interestinggadgets[retptr].count('#') == 2)):
                                    ropptr = (retptr + 1)
                                    break
                        if poptype.startswith('neg '):
                            for retptr in suggestions[poptype]:
                                if ((getOffset(interestinggadgets[retptr]) == 0) and (interestinggadgets[retptr].count('#') == 2)):
                                    ropptr = (retptr + 2)
                                    break
                    if (ropptr == 0):
                        for emptytype in suggestions:
                            if emptytype.startswith('empty '):
                                for retptr in suggestions[emptytype]:
                                    if interestinggadgets[retptr].startswith('# XOR'):
                                        if (getOffset(interestinggadgets[retptr]) == 0):
                                            ropptr = (retptr + 2)
                                        break
                    if (ropptr > 0):
                        thismodname = MnPointer(ropptr).belongsTo()
                        tmod = MnModule(thismodname)
                        ropnopinfo = getGadgetAddressInfo(ropptr)
                        thischain[thisreg] = putValueInReg(thisreg, ropptr, ((('RETN (ROP NOP) [' + thismodname) + ']') + ropnopinfo), suggestions, interestinggadgets, criteria)
                    else:
                        thischain[thisreg] = putValueInReg(thisreg, ropptr, '[-] Unable to find ptr to RETN (ROP NOP)', suggestions, interestinggadgets, criteria)
                if ((thistarget.__class__.__name__ == 'int') or (thistarget.__class__.__name__ == 'long')):
                    thischain[thisreg] = putValueInReg(thisreg, thistarget, ((('0x' + toHex(thistarget)) + '-> ') + thisreg), suggestions, interestinggadgets, criteria)
                if (str(thistarget) == 'nop'):
                    thischain[thisreg] = putValueInReg(thisreg, 2425393296, 'nop', suggestions, interestinggadgets, criteria)
                if str(thistarget).startswith('&?'):
                    rwptr = getAPointer(modulestosearch, criteria, 'RW')
                    if (rwptr == 0):
                        rwptr = getAPointer(modulestosearch, criteria, 'W')
                    if (rwptr != 0):
                        rwmodname = MnPointer(rwptr).belongsTo()
                        rwmodinfo = getGadgetAddressInfo(rwptr)
                        thischain[thisreg] = putValueInReg(thisreg, rwptr, ((('&Writable location [' + rwmodname) + ']') + rwmodinfo), suggestions, interestinggadgets, criteria)
                    else:
                        thischain[thisreg] = putValueInReg(thisreg, rwptr, '[-] Unable to find writable location', suggestions, interestinggadgets, criteria)
                if str(thistarget).startswith('pop'):
                    if (('pop ' + thisreg) in suggestions):
                        popptr = getShortestGadget(suggestions[('pop ' + thisreg)])
                        junksize = (getJunk(interestinggadgets[popptr]) - 4)
                        thismodname = MnPointer(popptr).belongsTo()
                        tmodinfo = getGadgetAddressInfo(popptr)
                        thischain[thisreg] = [[popptr, '', junksize], [popptr, ((('skip 4 bytes [' + thismodname) + ']') + tmodinfo)]]
                    else:
                        thischain[thisreg] = [[0, ("[-] Couldn't find a gadget to put a pointer to a stackpivot (4 bytes) into " + thisreg), 0]]
                if (str(thistarget) == '&'):
                    pattern = step[2]
                    base = 0
                    top = TOP_USERLAND
                    type = 'ptr'
                    al = criteria['accesslevel']
                    criteria['accesslevel'] = 'R'
                    ptr_counter = 0
                    ptr_to_get = 2
                    oldsilent = silent
                    silent = True
                    allpointers = findPattern(modulecriteria, criteria, pattern, type, base, top)
                    silent = oldsilent
                    criteria['accesslevel'] = al
                    if (len(allpointers) > 0):
                        theptr = 0
                        for ptrtype in allpointers:
                            for ptrs in allpointers[ptrtype]:
                                theptr = ptrs
                                break
                        thischain[thisreg] = putValueInReg(thisreg, theptr, (((('&' + str(pattern)) + ' [') + MnPointer(theptr).belongsTo()) + ']'), suggestions, interestinggadgets, criteria)
                    else:
                        thischain[thisreg] = putValueInReg(thisreg, 0, ('[-] Unable to find ptr to ' + str(pattern)), suggestions, interestinggadgets, criteria)
        returnoffset = 0
        delayedfill = 0
        junksize = 0
        longestmod = 0
        fillersize = 0
        for step in routinedefs[routine]:
            thisreg = step[0]
            if (thisreg in thischain):
                for gadget in thischain[thisreg]:
                    thismodname = sanitize_module_name(MnPointer(gadget[0]).belongsTo())
                    if (len(thismodname) > longestmod):
                        longestmod = len(thismodname)
        if showrva:
            fillersize = (longestmod + 8)
        else:
            fillersize = 0
        for reg in movetolast:
            if (reg in regsequences):
                regsequences.remove(reg)
                regsequences.append(reg)
        regimpact = {}
        ropdbchain = ''
        tohex_array = []
        for step in regsequences:
            thisreg = step
            vplogtxt += ('      #[---INFO:gadgets_to_set_%s:---]\n' % thisreg)
            thischaintxt += ('      #[---INFO:gadgets_to_set_%s:---]\n' % thisreg)
            if (thisreg in thischain):
                for gadget in thischain[thisreg]:
                    gadgetstep = gadget[0]
                    steptxt = gadget[1]
                    junksize = 0
                    showfills = False
                    if (len(gadget) > 2):
                        junksize = gadget[2]
                    if ((gadgetstep in interestinggadgets) and (steptxt == '')):
                        thisinstr = interestinggadgets[gadgetstep].lstrip()
                        if thisinstr.startswith('#'):
                            thisinstr = thisinstr[2:len(thisinstr)]
                            showfills = True
                        thismodname = MnPointer(gadgetstep).belongsTo()
                        thisinstr += ((' [' + thismodname) + ']')
                        tmod = MnModule(thismodname)
                        thisinstr += getGadgetAddressInfo(gadgetstep)
                        if (not (thismodname in modused)):
                            modused[thismodname] = [tmod.moduleBase, tmod.__str__()]
                        modprefix = ('base_' + sanitize_module_name(thismodname))
                        if showrva:
                            alignsize = (longestmod - len(sanitize_module_name(thismodname)))
                            vplogtxt += ('      %s + 0x%s,%s  # %s %s\n' % (modprefix, toHex((gadgetstep - tmod.moduleBase)), toSize('', alignsize), thisinstr, steptxt))
                            thischaintxt += ('      %s + 0x%s,%s  # %s %s\n' % (modprefix, toHex((gadgetstep - tmod.moduleBase)), toSize('', alignsize), thisinstr, steptxt))
                        else:
                            vplogtxt += ('      0x%s,  # %s %s\n' % (toHex(gadgetstep), thisinstr, steptxt))
                            thischaintxt += ('      0x%s,  # %s %s\n' % (toHex(gadgetstep), thisinstr, steptxt))
                        ropdbchain += ('    <gadget offset="0x%s">%s</gadget>\n' % (toHex((gadgetstep - tmod.moduleBase)), thisinstr.strip(' ')))
                        tohex_array.append(gadgetstep)
                        if showfills:
                            vplogtxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
                            thischaintxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
                            if (returnoffset > 0):
                                ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
                            returnoffset = getOffset(interestinggadgets[gadgetstep])
                            if (delayedfill > 0):
                                vplogtxt += createJunk(delayedfill, 'Filler (compensate)', fillersize)
                                thischaintxt += createJunk(delayedfill, 'Filler (compensate)', fillersize)
                                ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
                                delayedfill = 0
                            if thisinstr.startswith('POP '):
                                delayedfill = junksize
                            else:
                                vplogtxt += createJunk(junksize, 'Filler (compensate)', fillersize)
                                thischaintxt += createJunk(junksize, 'Filler (compensate)', fillersize)
                                if (junksize > 0):
                                    ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
                    else:
                        thismodname = MnPointer(gadgetstep).belongsTo()
                        if (thismodname != ''):
                            tmod = MnModule(thismodname)
                            if (not (thismodname in modused)):
                                modused[thismodname] = [tmod.moduleBase, tmod.__str__()]
                            modprefix = ('base_' + sanitize_module_name(thismodname))
                            if showrva:
                                alignsize = (longestmod - len(sanitize_module_name(thismodname)))
                                vplogtxt += ('      %s + 0x%s,%s  # %s\n' % (modprefix, toHex((gadgetstep - tmod.moduleBase)), toSize('', alignsize), steptxt))
                                thischaintxt += ('      %s + 0x%s,%s  # %s\n' % (modprefix, toHex((gadgetstep - tmod.moduleBase)), toSize('', alignsize), steptxt))
                            else:
                                vplogtxt += ('      0x%s,  # %s\n' % (toHex(gadgetstep), steptxt))
                                thischaintxt += ('      0x%s,  # %s\n' % (toHex(gadgetstep), steptxt))
                            ropdbchain += ('    <gadget offset="0x%s">%s</gadget>\n' % (toHex((gadgetstep - tmod.moduleBase)), steptxt.strip(' ')))
                        else:
                            vplogtxt += ('      0x%s,%s  # %s\n' % (toHex(gadgetstep), toSize('', fillersize), steptxt))
                            thischaintxt += ('      0x%s,%s  # %s\n' % (toHex(gadgetstep), toSize('', fillersize), steptxt))
                            ropdbchain += ('    <gadget value="0x%s">%s</gadget>\n' % (toHex(gadgetstep), steptxt.strip(' ')))
                        if steptxt.startswith('[-]'):
                            vplogtxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
                            thischaintxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
                            ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
                            returnoffset = 0
                        if (delayedfill > 0):
                            vplogtxt += createJunk(delayedfill, 'Filler (compensate)', fillersize)
                            thischaintxt += createJunk(delayedfill, 'Filler (compensate)', fillersize)
                            ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
                            delayedfill = 0
                        vplogtxt += createJunk(junksize, '', fillersize)
                        thischaintxt += createJunk(junksize, '', fillersize)
                        if (fillersize > 0):
                            ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
        steptxt = ''
        vplogtxt += '      #[---INFO:pushad:---]\n'
        thischaintxt += '      #[---INFO:pushad:---]\n'
        if ('pushad' in suggestions):
            shortest_pushad = getShortestGadget(suggestions['pushad'])
            junksize = getJunk(interestinggadgets[shortest_pushad])
            thisinstr = interestinggadgets[shortest_pushad].lstrip()
            if thisinstr.startswith('#'):
                thisinstr = thisinstr[2:len(thisinstr)]
            regimpact = getRegImpact(thisinstr)
            thismodname = MnPointer(shortest_pushad).belongsTo()
            thisinstr += ((' [' + thismodname) + ']')
            tmod = MnModule(thismodname)
            thisinstr += getGadgetAddressInfo(shortest_pushad)
            if (not (thismodname in modused)):
                modused[thismodname] = [tmod.moduleBase, tmod.__str__()]
            modprefix = ('base_' + sanitize_module_name(thismodname))
            if showrva:
                alignsize = (longestmod - len(thismodname))
                vplogtxt += ('      %s + 0x%s,%s  # %s %s\n' % (modprefix, toHex((shortest_pushad - tmod.moduleBase)), toSize('', alignsize), thisinstr, steptxt))
                thischaintxt += ('      %s + 0x%s,%s  # %s %s\n' % (modprefix, toHex((shortest_pushad - tmod.moduleBase)), toSize('', alignsize), thisinstr, steptxt))
            else:
                vplogtxt += ('      0x%s,  # %s %s\n' % (toHex(shortest_pushad), thisinstr, steptxt))
                thischaintxt += ('      0x%s,  # %s %s\n' % (toHex(shortest_pushad), thisinstr, steptxt))
            ropdbchain += ('    <gadget offset="0x%s">%s</gadget>\n' % (toHex((shortest_pushad - tmod.moduleBase)), thisinstr.strip(' ')))
            vplogtxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
            thischaintxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
            if (fillersize > 0):
                ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
            vplogtxt += createJunk(junksize, '', fillersize)
            thischaintxt += createJunk(junksize, '', fillersize)
            if (fillersize > 0):
                ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
        else:
            vplogtxt += ('      0x00000000,%s  # %s\n' % (toSize('', fillersize), '[-] Unable to find pushad gadget'))
            thischaintxt += ('      0x00000000,%s  # %s\n' % (toSize('', fillersize), '[-] Unable to find pushad gadget'))
            ropdbchain += '    <gadget offset="0x00000000">Unable to find PUSHAD gadget</gadget>\n'
            vplogtxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
            thischaintxt += createJunk(returnoffset, 'Filler (RETN offset compensation)', fillersize)
            if (returnoffset > 0):
                ropdbchain += '    <gadget value="junk">Filler</gadget>\n'
        if (len(toadd) > 0):
            vplogtxt += '      #[---INFO:extras:---]\n'
            thischaintxt += '      #[---INFO:extras:---]\n'
            for adds in toadd:
                theptr = toadd[adds][0]
                freetext = toadd[adds][1]
                if (theptr > 0):
                    thismodname = MnPointer(theptr).belongsTo()
                    freetext += ((' [' + thismodname) + ']')
                    tmod = MnModule(thismodname)
                    freetext += getGadgetAddressInfo(theptr)
                    if (not (thismodname in modused)):
                        modused[thismodname] = [tmod.moduleBase, tmod.__str__()]
                    modprefix = ('base_' + sanitize_module_name(thismodname))
                    if showrva:
                        alignsize = (longestmod - len(thismodname))
                        vplogtxt += ('      %s + 0x%s,%s  # %s\n' % (modprefix, toHex((theptr - tmod.moduleBase)), toSize('', alignsize), freetext))
                        thischaintxt += ('      %s + 0x%s,%s  # %s\n' % (modprefix, toHex((theptr - tmod.moduleBase)), toSize('', alignsize), freetext))
                    else:
                        vplogtxt += ('      0x%s,  # %s\n' % (toHex(theptr), freetext))
                        thischaintxt += ('      0x%s,  # %s\n' % (toHex(theptr), freetext))
                    ropdbchain += ('    <gadget offset="0x%s">%s</gadget>\n' % (toHex((theptr - tmod.moduleBase)), freetext.strip(' ')))
                else:
                    vplogtxt += ('      0x%s,  # <- Unable to find %s\n' % (toHex(theptr), freetext))
                    thischaintxt += ('      0x%s,  # <- Unable to find %s\n' % (toHex(theptr), freetext))
                    ropdbchain += ('    <gadget offset="0x%s">Unable to find %s</gadget>\n' % (toHex(theptr), freetext.strip(' ')))
        vplogtxt += '    ].flatten.pack("V*")\n'
        vplogtxt += '\n    return rop_gadgets\n\n'
        vplogtxt += '  end\n'
        vplogtxt += "\n\n  # Call the ROP chain generator inside the 'exploit' function :\n\n"
        calltxt = 'rop_chain = create_rop_chain('
        argtxt = ''
        vplogtxtpy = ''
        vplogtxtc = ''
        vplogtxtjs = ''
        argtxtpy = ''
        if showrva:
            for themod in modused:
                repr_mod = sanitize_module_name(themod)
                vplogtxt += (('  # ' + modused[themod][1]) + '\n')
                vplogtxtpy += (('  # ' + modused[themod][1]) + '\n')
                vplogtxtc += (('  // ' + modused[themod][1]) + '\n')
                vplogtxtjs += (('  // ' + modused[themod][1]) + '\n')
                vplogtxt += (('  base_' + repr_mod) + (' = 0x%s\n' % toHex(modused[themod][0])))
                vplogtxtjs += (('  var base_' + repr_mod) + (' = 0x%s;\n' % toHex(modused[themod][0])))
                vplogtxtpy += (('  base_' + repr_mod) + (' = 0x%s\n' % toHex(modused[themod][0])))
                vplogtxtc += (('  unsigned int base_' + repr_mod) + (' = 0x%s;\n' % toHex(modused[themod][0])))
                calltxt += (('base_' + repr_mod) + ',')
                argtxt += (('base_' + repr_mod) + ',')
                argtxtpy += (('base_' + repr_mod) + ',')
        calltxt = (calltxt.rstrip(',') + ')\n')
        argtxt = argtxt.strip(',')
        argtxtpy = argtxtpy.strip(',')
        argtxtjs = argtxtpy.replace('.', '')
        vplogtxt = vplogtxt.replace('create_rop_chain()', (('create_rop_chain(' + argtxt) + ')'))
        vplogtxt += ('\n  ' + calltxt)
        vplogtxt += '\n\n\n'
        vplogtxt += '*** [ C ] ***\n\n'
        vplogtxt += '  #define CREATE_ROP_CHAIN(name, ...) \\\n'
        vplogtxt += '    int name##_length = create_rop_chain(NULL, ##__VA_ARGS__); \\\n'
        vplogtxt += '    unsigned int name[name##_length / sizeof(unsigned int)]; \\\n'
        vplogtxt += '    create_rop_chain(name, ##__VA_ARGS__);\n\n'
        vplogtxt += ('  int create_rop_chain(unsigned int *buf, %s)\n' % ', '.join((('unsigned int %s' % _) for _ in argtxt.split(','))))
        vplogtxt += '  {\n'
        vplogtxt += '    // rop chain generated with mona.py - www.corelan.be\n'
        vplogtxt += '    unsigned int rop_gadgets[] = {\n'
        vplogtxt += thischaintxt.replace('#', '//')
        vplogtxt += '    };\n'
        vplogtxt += '    if(buf != NULL) {\n'
        vplogtxt += '      memcpy(buf, rop_gadgets, sizeof(rop_gadgets));\n'
        vplogtxt += '    };\n'
        vplogtxt += '    return sizeof(rop_gadgets);\n'
        vplogtxt += '  }\n\n'
        vplogtxt += vplogtxtc
        vplogtxt += "  // use the 'rop_chain' variable after this call, it's just an unsigned int[]\n"
        vplogtxt += ('  CREATE_ROP_CHAIN(rop_chain, %s);\n' % argtxtpy)
        vplogtxt += '  // alternatively just allocate a large enough buffer and get the rop chain, i.e.:\n'
        vplogtxt += '  // unsigned int rop_chain[256];\n'
        vplogtxt += ('  // int rop_chain_length = create_rop_chain(rop_chain, %s);\n\n' % argtxtpy)
        vplogtxt += '*** [ Python ] ***\n\n'
        vplogtxt += ('  def create_rop_chain(%s):\n' % argtxt)
        vplogtxt += '\n    # rop chain generated with mona.py - www.corelan.be\n'
        vplogtxt += '    rop_gadgets = [\n'
        vplogtxt += thischaintxt
        vplogtxt += '    ]\n'
        vplogtxt += "    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)\n\n"
        vplogtxt += vplogtxtpy
        vplogtxt += ('  rop_chain = create_rop_chain(%s)\n\n' % argtxtpy)
        vplogtxt += '\n\n*** [ JavaScript ] ***\n\n'
        vplogtxt += '  //rop chain generated with mona.py - www.corelan.be\n'
        if (not showrva):
            vplogtxt += '  rop_gadgets = unescape(\n'
            allptr = thischaintxt.split('\n')
            tptrcnt = 0
            for tptr in allptr:
                comments = tptr.split(',')
                comment = ''
                if (len(comments) > 1):
                    ic = 1
                    while (ic < len(comments)):
                        comment += (',' + comments[ic])
                        ic += 1
                tptrcnt += 1
                comment = comment.replace('  ', '')
                if (tptrcnt < len(allptr)):
                    vplogtxt += (((((('    "' + toJavaScript(tptr)) + '" + // ') + comments[0].replace('  ', '').replace(' ', '')) + ' : ') + comment) + '\n')
                else:
                    vplogtxt += (((((('    "' + toJavaScript(tptr)) + '"); // ') + comments[0].replace('  ', '').replace(' ', '')) + ' : ') + comment) + '\n\n')
        else:
            vplogtxt += ('  function get_rop_chain(%s) {\n' % argtxtjs)
            vplogtxt += '    var rop_gadgets = [\n'
            vplogtxt += thischaintxt.replace('  #', '  //').replace('.', '')
            vplogtxt += '      ];\n'
            vplogtxt += '    return rop_gadgets;\n'
            vplogtxt += '  }\n\n'
            vplogtxt += '  function gadgets2uni(gadgets) {\n'
            vplogtxt += '    var uni = "";\n'
            vplogtxt += '    for(var i=0;i<gadgets.length;i++){\n'
            vplogtxt += '      uni += d2u(gadgets[i]);\n'
            vplogtxt += '    }\n'
            vplogtxt += '    return uni;\n'
            vplogtxt += '  }\n\n'
            vplogtxt += '  function d2u(dword) {\n'
            vplogtxt += '    var uni = String.fromCharCode(dword & 0xFFFF);\n'
            vplogtxt += '    uni += String.fromCharCode(dword>>16);\n'
            vplogtxt += '    return uni;\n'
            vplogtxt += '  }\n\n'
            vplogtxt += ('%s' % vplogtxtjs)
            vplogtxt += ('\n  var rop_chain = gadgets2uni(get_rop_chain(%s));\n\n' % argtxtjs)
        vplogtxt += '\n--------------------------------------------------------------------------------------------------\n\n'
        if (len(modused) == 1):
            modulename = ''
            for modname in modused:
                modulename = modname
            objMod = MnModule(modulename)
            modversion = objMod.moduleVersion
            modbase = objMod.moduleBase
            ropdb = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            ropdb += '<db>\n<rop>\n'
            ropdb += '  <compatibility>\n'
            ropdb += ('    <target>%s</target>\n' % modversion)
            ropdb += '  </compatibility>\n\n'
            ropdb += ('  <gadgets base="0x%s">\n' % toHex(modbase))
            ropdb += ropdbchain.replace((('[' + modulename) + ']'), '').replace('&', '').replace((('[IAT ' + modulename) + ']'), '')
            ropdb += '  </gadgets>\n'
            ropdb += '</rop>\n</db>'
            shortmodname = modulename.replace('.dll', '')
            ignoremodules = True
            if (ropdbchain.lower().find('virtualprotect') > (- 1)):
                ofile = MnLog((shortmodname + '_virtualprotect.xml'))
                thisofile = ofile.reset(showheader=False)
                ofile.write(ropdb, thisofile)
            if (ropdbchain.lower().find('virtualalloc') > (- 1)):
                ofile = MnLog((shortmodname + '_virtualalloc.xml'))
                thisofile = ofile.reset(showheader=False)
                ofile.write(ropdb, thisofile)
            ignoremodules = False
    vpfile = MnLog('rop_chains.txt')
    thisvplog = vpfile.reset()
    vpfile.write(vplogtxt, thisvplog)
    dbg.log(('[+] ROP chains written to file %s' % thisvplog))
    objprogressfile.write('Done creating rop chains', progressfile)
    return vplogtxt

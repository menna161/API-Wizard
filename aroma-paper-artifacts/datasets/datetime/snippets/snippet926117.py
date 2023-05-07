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


def args2criteria(args, modulecriteria, criteria):
    (thisversion, thisrevision) = getVersionInfo(inspect.stack()[0][1])
    thisversion = thisversion.replace("'", '')
    dbg.logLines(('\n---------- Mona command started on %s (v%s, rev %s) ----------' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), thisversion, thisrevision)))
    dbg.log('[+] Processing arguments and criteria')
    global ptr_to_get
    criteria['accesslevel'] = 'X'
    if ('x' in args):
        if (not (args['x'].upper() in ['*', 'R', 'RW', 'RX', 'RWX', 'W', 'WX', 'X'])):
            dbg.log(('invalid access level : %s' % args['x']), highlight=1)
            criteria['accesslevel'] = ''
        else:
            criteria['accesslevel'] = args['x'].upper()
    dbg.log(('    - Pointer access level : %s' % criteria['accesslevel']))
    if (('o' in args) and args['o']):
        modulecriteria['os'] = False
        dbg.log('    - Ignoring OS modules')
    if (('n' in args) and args['n']):
        criteria['nonull'] = True
        dbg.log('    - Ignoring pointers that have null bytes')
    if ('m' in args):
        if (type(args['m']).__name__.lower() != 'bool'):
            modulecriteria['modules'] = args['m']
            dbg.log(('    - Only querying modules %s' % args['m']))
    if ('p' in args):
        if (str(args['p']).lower() != 'true'):
            ptr_to_get = int(args['p'].strip())
        if (ptr_to_get > 0):
            dbg.log(('    - Maximum nr of pointers to return : %d' % ptr_to_get))
    if ('cp' in args):
        ptrcriteria = args['cp'].split(',')
        for ptrcrit in ptrcriteria:
            ptrcrit = ptrcrit.strip("'")
            ptrcrit = ptrcrit.strip('"').lower().strip()
            criteria[ptrcrit] = True
        dbg.log(('    - Pointer criteria : %s' % ptrcriteria))
    if ('cbp' in args):
        dbg.log("    * Trying to use '-cbp' instead of '-cpb'?", highlight=True)
        if (not ('cpb' in args)):
            dbg.log("    * I'll try to fix your typo myself, but please pay attention to the syntax next time", highlight=True)
            args['cpb'] = args['cbp']
    if ('cpb' in args):
        badchars = args['cpb']
        badchars = badchars.replace("'", '')
        badchars = badchars.replace('"', '')
        badchars = badchars.replace('\\x', '')
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
        criteria['badchars'] = strb
        dbg.log(('    - Bad char filter will be applied to pointers : %s ' % args['cpb']))
    if ('cm' in args):
        modcriteria = args['cm'].split(',')
        for modcrit in modcriteria:
            modcrit = modcrit.strip("'")
            modcrit = modcrit.strip('"').lower().strip()
            modcritparts = modcrit.split('=')
            try:
                if (len(modcritparts) < 2):
                    modulecriteria[modcritparts[0].strip()] = True
                else:
                    modulecriteria[modcritparts[0].strip()] = (modcritparts[1].strip() == 'true')
            except:
                continue
        if (inspect.stack()[1][3] == 'procShowMODULES'):
            modcriteria = args['cm'].split(',')
            for modcrit in modcriteria:
                modcrit = modcrit.strip("'")
                modcrit = modcrit.strip('"').lower().strip()
                if modcrit.startswith('+'):
                    modulecriteria[modcrit] = True
                else:
                    modulecriteria[modcrit] = False
        dbg.log(('    - Module criteria : %s' % modcriteria))
    return (modulecriteria, criteria)

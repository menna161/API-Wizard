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


def findSEH(modulecriteria={}, criteria={}):
    '\n\tPerforms a search for pointers to gain code execution in a SEH overwrite exploit\n\n\tArguments:\n\tmodulecriteria - dictionary with criteria modules need to comply with.\n\t                 Default settings are : ignore aslr, rebase and safeseh protected modules\n\tcriteria - dictionary with criteria the pointers need to comply with.\n\n\tReturn:\n\tDictionary (pointers)\n\t'
    type = ''
    if ('rop' in criteria):
        type = 'rop'
    search = getSearchSequences('seh', 0, type)
    found_opcodes = {}
    all_opcodes = {}
    modulestosearch = getModulesToQuery(modulecriteria)
    if (not silent):
        dbg.log(('[+] Querying %d modules' % len(modulestosearch)))
    starttime = datetime.datetime.now()
    for thismodule in modulestosearch:
        if (not silent):
            dbg.log(('    - Querying module %s' % thismodule))
        dbg.updateLog()
        found_opcodes = searchInModule(search, thismodule, criteria)
        all_opcodes = mergeOpcodes(all_opcodes, found_opcodes)
    if ('all' in criteria):
        if ('accesslevel' in criteria):
            if (criteria['accesslevel'].find('R') == (- 1)):
                if (not silent):
                    dbg.log("[+] Setting pointer access level criteria to 'R', to increase search results")
                criteria['accesslevel'] = 'R'
                if (not silent):
                    dbg.log(('    New pointer access level : %s' % criteria['accesslevel']))
        if criteria['all']:
            rangestosearch = getRangesOutsideModules()
            if (not silent):
                dbg.log('[+] Querying memory outside modules')
            for thisrange in rangestosearch:
                if (not silent):
                    dbg.log(('    - Querying 0x%08x - 0x%08x' % (thisrange[0], thisrange[1])))
                found_opcodes = searchInRange(search, thisrange[0], thisrange[1], criteria)
                all_opcodes = mergeOpcodes(all_opcodes, found_opcodes)
            if (not silent):
                dbg.log('    - Search complete, processing results')
            dbg.updateLog()
    return all_opcodes

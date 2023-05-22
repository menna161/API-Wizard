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


def findJMP(modulecriteria={}, criteria={}, register='esp'):
    '\n\tPerforms a search for pointers to jump to a given register\n\n\tArguments:\n\tmodulecriteria - dictionary with criteria modules need to comply with.\n\t                 Default settings are : ignore aslr and rebased modules\n\tcriteria - dictionary with criteria the pointers need to comply with.\n\tregister - the register to jump to\n\n\tReturn:\n\tDictionary (pointers)\n\t'
    search = getSearchSequences('jmp', register, '', criteria)
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
    if (not silent):
        dbg.log('    - Search complete, processing results')
    dbg.updateLog()
    return all_opcodes

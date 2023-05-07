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


def getAPointer(modules, criteria, accesslevel):
    '\n\tGets the first pointer from one of the supplied module that meets a set of criteria\n\t\n\tArguments:\n\tmodules - array with module names\n\tcriteria - dictionary describing the criteria the pointer needs to comply with\n\taccesslevel - the required access level\n\t\n\tReturn:\n\ta pointer (integer value) or 0 if nothing was found\n\t'
    pointer = 0
    dbg.getMemoryPages()
    for a in dbg.MemoryPages.keys():
        page_start = a
        page_size = dbg.MemoryPages[a].getSize()
        page_end = (a + page_size)
        if meetsAccessLevel(dbg.MemoryPages[a], accesslevel):
            pageptr = MnPointer(a)
            thismodulename = pageptr.belongsTo()
            if ((thismodulename != '') and (thismodulename in modules)):
                thismod = MnModule(thismodulename)
                start = thismod.moduleBase
                end = thismod.moduleTop
                random.seed()
                for cnt in xrange((page_size + 1)):
                    theoffset = random.randint(0, page_size)
                    thispointer = MnPointer((page_start + theoffset))
                    if meetsCriteria(thispointer, criteria):
                        return (page_start + theoffset)
    return pointer

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


def Poly_ReturnDW(value):
    I = random.randint(1, 3)
    if (I == 1):
        if (random.randint(1, 2) == 1):
            return dbg.assemble(('SUB EAX, EAX\n ADD EAX, 0x%08x' % value))
        else:
            return dbg.assemble(('SUB EAX, EAX\n ADD EAX, -0x%08x' % value))
    if (I == 2):
        return dbg.assemble(('PUSH 0x%08x\n POP EAX\n' % value))
    if (I == 3):
        if (random.randint(1, 2) == 1):
            return dbg.assemble(('XCHG EAX, EDI\n DB 0xBF\n DD 0x%08x\n XCHG EAX, EDI' % value))
        else:
            return dbg.assemble(('XCHG EAX, EDI\n MOV EDI, 0x%08x\n XCHG EAX, EDI' % value))
    return

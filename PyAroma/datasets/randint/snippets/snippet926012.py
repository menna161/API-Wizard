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


def Poly_Return0():
    I = random.randint(1, 4)
    if (I == 1):
        return dbg.assemble('SUB EAX, EAX')
    if (I == 2):
        if (random.randint(1, 2) == 1):
            return dbg.assemble('PUSH 0\n POP EAX')
        else:
            return dbg.assemble('DB 0x6A, 0x00\n POP EAX')
    if (I == 3):
        return dbg.assemble('XCHG EAX, EDI\n SUB EDI, EDI\n XCHG EAX, EDI')
    if (I == 4):
        return Poly_ReturnDW(0)
    return

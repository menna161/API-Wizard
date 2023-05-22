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


@memoized
def get_blocks(self):
    '\n\t\tCompares two binary strings under the assumption that y is the result of\n\t\tapplying the following transformations onto x:\n\n\t\t * change single bytes in x (likely)\n\t\t * expand single bytes in x to two bytes (less likely)\n\t\t * drop single bytes in x (even less likely)\n\n\t\tReturns a generator that yields elements of the form (unmodified, xdiff, ydiff),\n\t\twhere each item represents a binary chunk with "unmodified" denoting whether the\n\t\tchunk is the same in both strings, "xdiff" denoting the size of the chunk in x\n\t\tand "ydiff" denoting the size of the chunk in y.\n\n\t\tExample:\n\t\t>>> x = "abcdefghijklm"\n\t\t>>> y = "mmmcdefgHIJZklm"\n\t\t>>> list(MemoryComparator(x, y).get_blocks())\n\t\t[(False, 2, 3), (True, 5, 5),\n\t\t (False, 3, 4), (True, 3, 3)]\n\t\t'
    (x, y) = (self.x, self.y)
    (_, moves) = self.get_grid()
    path = []
    (i, j) = (0, 0)
    while True:
        (dy, dx) = self.move_to_gradient[moves[j][i]]
        if (dy == dx == 0):
            break
        path.append((((dy == 1) and (x[i] == y[j])), dy, dx))
        (j, i) = ((j + dy), (i + dx))
    for (i, j) in zip(range(i, len(x)), itertools.count(j)):
        if (j < len(y)):
            path.append(((x[i] == y[j]), 1, 1))
        else:
            path.append((False, 0, 1))
    i = j = 0
    for (unmodified, subpath) in itertools.groupby(path, itemgetter(0)):
        ydiffs = map(itemgetter(1), subpath)
        (dx, dy) = (len(ydiffs), sum(ydiffs))
        (yield (unmodified, dx, dy))
        i += dx
        j += dy

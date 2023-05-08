import json
import datetime
import time
import os.path
import random
import re
import sys
import os
import urllib.request
import urllib.error
import traceback


def object_id(args=[]):
    if (not args):
        args.extend([random.randint(0, 16777215), random.randint(0, 32766), random.randint(0, 16777215)])
    args[1] += 1
    if (args[2] > 16777215):
        args[2] = 0
    return '{:08x}{:06x}{:04x}{:06x}'.format(int(time.time()), args[0], args[1], args[2])

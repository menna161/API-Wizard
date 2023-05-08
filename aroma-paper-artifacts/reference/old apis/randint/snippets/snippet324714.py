from __future__ import annotations
import itertools
import os
import pprint
import random
import struct
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory
import click
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from getdents import paths
from mptool import output
from with_chdir import chdir


def random_utf8() -> bytes:
    gotutf8 = False
    while (not gotutf8):
        codepoint = random.SystemRandom().randint(0, 4294967296)
        possible_utf8_bytes = struct.pack('>I', codepoint)
        try:
            possible_utf8_bytes.decode('UTF8')
            gotutf8 = True
        except UnicodeDecodeError:
            pass
    return possible_utf8_bytes

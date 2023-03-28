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


def random_filename_length() -> int:
    return random.SystemRandom().randint(0, 255)

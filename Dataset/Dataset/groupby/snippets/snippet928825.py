import sys
import argparse
import binascii
import calendar
import cmd
import inspect
import io
import fnmatch
import os
import re
import select
import serial
import shutil
import socket
import tempfile
import time
import threading
import token
import tokenize
import shlex
import itertools
from serial.tools import list_ports
import traceback
import readline
import rlcompleter
import platform
from rshell.getch import getch
from rshell.pyboard import Pyboard, PyboardError
from rshell.version import __version__
import subprocess
import os
import time
import os
import os
import os
import os
import os
import os
import os
import os
import os
import os
import sys
import os
import sys
import sys
import sys
import time
import pyudev
import board
import os
import pyb
import ubinascii
import ubinascii
import ubinascii
import termios
import sys
import binascii as ubinascii
import micropython
import binascii as ubinascii
import binascii as ubinascii
import pycom
import machine
import machine
import os


def onecmd(self, line):
    "Override onecmd.\n\n        1 - So we don't have to have a do_EOF method.\n        2 - So we can strip comments\n        3 - So we can track line numbers\n        "
    if DEBUG:
        print(('Executing "%s"' % line))
    self.line_num += 1
    if ((line == 'EOF') or (line == 'exit')):
        if cmd.Cmd.use_rawinput:
            self.print('')
        return True
    comment_idx = line.find('#')
    if (comment_idx >= 0):
        line = line[0:comment_idx]
        line = line.strip()
    lexer = shlex.shlex(line)
    lexer.whitespace = ''
    for (issemicolon, group) in itertools.groupby(lexer, (lambda x: (x == ';'))):
        if (not issemicolon):
            self.onecmd_exec(''.join(group))

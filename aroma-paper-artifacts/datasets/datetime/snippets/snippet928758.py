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


def set_time(rtc_time):
    rtc = None
    try:
        import pyb
        rtc = pyb.RTC()
        rtc.datetime(rtc_time)
    except:
        try:
            import pycom
            rtc_time2 = (rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[4], rtc_time[5], rtc_time[6])
            import machine
            rtc = machine.RTC()
            rtc.init(rtc_time2)
        except:
            try:
                import machine
                rtc = machine.RTC()
                try:
                    rtc.datetime(rtc_time)
                except:
                    rtc.init(rtc_time)
            except:
                try:
                    import os
                    if (os.uname().sysname == 'rp2'):
                        setup_0 = (((rtc_time[0] << 12) | (rtc_time[1] << 8)) | rtc_time[2])
                        setup_1 = (((((rtc_time[3] % 7) << 24) | (rtc_time[4] << 16)) | (rtc_time[5] << 8)) | rtc_time[6])
                        machine.mem32[1074118660] = setup_0
                        machine.mem32[1074118664] = setup_1
                        machine.mem32[1074118668] |= 16
                except:
                    pass

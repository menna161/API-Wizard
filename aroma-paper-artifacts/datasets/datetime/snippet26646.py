import codecs
import datetime
import fcntl
import os
import pty
import select
import struct
import termios
import tty
from collections import defaultdict, namedtuple
from typing import Iterator
import pyte
import pyte.screens
from termtosvg import anim
from termtosvg.asciicast import AsciiCastV2Event, AsciiCastV2Header


def _capture_output(input_fileno, output_fileno, master_fd, buffer_size=1024):
    'Send data from input_fileno to master_fd and send data from master_fd to\n    output_fileno and to the caller\n\n    The implementation of this method is mostly copied from the pty.spawn\n    function of the CPython standard library. It has been modified in order to\n    make the `record` function a generator.\n\n    See https://github.com/python/cpython/blob/master/Lib/pty.py\n    '
    rlist = [input_fileno, master_fd]
    xlist = [input_fileno, output_fileno, master_fd]
    xfds = []
    while (not xfds):
        (rfds, _, xfds) = select.select(rlist, [], xlist)
        for fd in rfds:
            try:
                data = os.read(fd, buffer_size)
            except OSError:
                xfds.append(fd)
                continue
            if (not data):
                xfds.append(fd)
                continue
            if (fd == input_fileno):
                write_fileno = master_fd
            else:
                write_fileno = output_fileno
                (yield (data, datetime.datetime.now()))
            while data:
                n = os.write(write_fileno, data)
                data = data[n:]

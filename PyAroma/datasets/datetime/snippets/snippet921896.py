from __future__ import division
import collections
import contextlib
import datetime
import functools
import os
import signal
import subprocess
import sys
import threading
import time
from . import _common
from ._common import AccessDenied
from ._common import deprecated_method
from ._common import Error
from ._common import memoize
from ._common import memoize_when_activated
from ._common import NoSuchProcess
from ._common import TimeoutExpired
from ._common import wrap_numbers as _wrap_numbers
from ._common import ZombieProcess
from ._compat import long
from ._compat import PermissionError
from ._compat import ProcessLookupError
from ._compat import PY3 as _PY3
from ._common import STATUS_DEAD
from ._common import STATUS_DISK_SLEEP
from ._common import STATUS_IDLE
from ._common import STATUS_LOCKED
from ._common import STATUS_PARKED
from ._common import STATUS_RUNNING
from ._common import STATUS_SLEEPING
from ._common import STATUS_STOPPED
from ._common import STATUS_TRACING_STOP
from ._common import STATUS_WAITING
from ._common import STATUS_WAKING
from ._common import STATUS_ZOMBIE
from ._common import CONN_CLOSE
from ._common import CONN_CLOSE_WAIT
from ._common import CONN_CLOSING
from ._common import CONN_ESTABLISHED
from ._common import CONN_FIN_WAIT1
from ._common import CONN_FIN_WAIT2
from ._common import CONN_LAST_ACK
from ._common import CONN_LISTEN
from ._common import CONN_NONE
from ._common import CONN_SYN_RECV
from ._common import CONN_SYN_SENT
from ._common import CONN_TIME_WAIT
from ._common import NIC_DUPLEX_FULL
from ._common import NIC_DUPLEX_HALF
from ._common import NIC_DUPLEX_UNKNOWN
from ._common import AIX
from ._common import BSD
from ._common import FREEBSD
from ._common import LINUX
from ._common import MACOS
from ._common import NETBSD
from ._common import OPENBSD
from ._common import OSX
from ._common import POSIX
from ._common import SUNOS
from ._common import WINDOWS
import pwd
from . import _pslinux as _psplatform
from ._pslinux import IOPRIO_CLASS_BE
from ._pslinux import IOPRIO_CLASS_IDLE
from ._pslinux import IOPRIO_CLASS_NONE
from ._pslinux import IOPRIO_CLASS_RT
from ._common import bytes2human
from ._compat import get_terminal_size
from ._psutil_linux import RLIM_INFINITY
from ._psutil_linux import RLIMIT_AS
from ._psutil_linux import RLIMIT_CORE
from ._psutil_linux import RLIMIT_CPU
from ._psutil_linux import RLIMIT_DATA
from ._psutil_linux import RLIMIT_FSIZE
from ._psutil_linux import RLIMIT_LOCKS
from ._psutil_linux import RLIMIT_MEMLOCK
from ._psutil_linux import RLIMIT_NOFILE
from ._psutil_linux import RLIMIT_NPROC
from ._psutil_linux import RLIMIT_RSS
from ._psutil_linux import RLIMIT_STACK
from . import _psutil_linux
from . import _pswindows as _psplatform
from ._psutil_windows import ABOVE_NORMAL_PRIORITY_CLASS
from ._psutil_windows import BELOW_NORMAL_PRIORITY_CLASS
from ._psutil_windows import HIGH_PRIORITY_CLASS
from ._psutil_windows import IDLE_PRIORITY_CLASS
from ._psutil_windows import NORMAL_PRIORITY_CLASS
from ._psutil_windows import REALTIME_PRIORITY_CLASS
from ._pswindows import CONN_DELETE_TCB
from ._pswindows import IOPRIO_VERYLOW
from ._pswindows import IOPRIO_LOW
from ._pswindows import IOPRIO_NORMAL
from ._pswindows import IOPRIO_HIGH
import socket
from . import _psosx as _psplatform
from . import _psbsd as _psplatform
from . import _pssunos as _psplatform
from ._pssunos import CONN_BOUND
from ._pssunos import CONN_IDLE
from . import _psaix as _psplatform


def test():
    from ._common import bytes2human
    from ._compat import get_terminal_size
    today_day = datetime.date.today()
    templ = '%-10s %5s %5s %7s %7s %5s %6s %6s %6s  %s'
    attrs = ['pid', 'memory_percent', 'name', 'cmdline', 'cpu_times', 'create_time', 'memory_info', 'status', 'nice', 'username']
    print((templ % ('USER', 'PID', '%MEM', 'VSZ', 'RSS', 'NICE', 'STATUS', 'START', 'TIME', 'CMDLINE')))
    for p in process_iter(attrs, ad_value=None):
        if p.info['create_time']:
            ctime = datetime.datetime.fromtimestamp(p.info['create_time'])
            if (ctime.date() == today_day):
                ctime = ctime.strftime('%H:%M')
            else:
                ctime = ctime.strftime('%b%d')
        else:
            ctime = ''
        if p.info['cpu_times']:
            cputime = time.strftime('%M:%S', time.localtime(sum(p.info['cpu_times'])))
        else:
            cputime = ''
        user = (p.info['username'] or '')
        if ((not user) and POSIX):
            try:
                user = p.uids()[0]
            except Error:
                pass
        if (user and WINDOWS and ('\\' in user)):
            user = user.split('\\')[1]
        user = user[:9]
        vms = (bytes2human(p.info['memory_info'].vms) if (p.info['memory_info'] is not None) else '')
        rss = (bytes2human(p.info['memory_info'].rss) if (p.info['memory_info'] is not None) else '')
        memp = (round(p.info['memory_percent'], 1) if (p.info['memory_percent'] is not None) else '')
        nice = (int(p.info['nice']) if p.info['nice'] else '')
        if p.info['cmdline']:
            cmdline = ' '.join(p.info['cmdline'])
        else:
            cmdline = p.info['name']
        status = (p.info['status'][:5] if p.info['status'] else '')
        line = (templ % (user[:10], p.info['pid'], memp, vms, rss, nice, status, ctime, cputime, cmdline))
        print(line[:get_terminal_size()[0]])

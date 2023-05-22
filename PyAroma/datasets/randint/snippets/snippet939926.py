import logging
import os
import random
import socket
import subprocess
import sys
import tempfile
import time
from rpyc import classic as rpyc_classic
from .memory import CachedIDAMemory, CachedIDAPermissions
from .errors import IDALinkError


def __init__(self, ida_binary=None, filename=None, host=None, port=None, retry=10, processor_type=None, logfile=None, pull_memory=True):
    if (port is None):
        if (host is not None):
            raise ValueError('Provided host but not port')
        port = random.randint(40000, 49999)
    if ((ida_binary is None) and (host is None)):
        raise ValueError('Must provide ida_binary or host')
    if ((ida_binary is not None) and (host is not None)):
        raise ValueError('Must provide exactly one of ida_binary and host')
    if (ida_binary is not None):
        if (filename is None):
            raise ValueError('Must provide filename if spawning a local process')
        self._proc = ida_spawn(ida_binary, filename, port, processor_type=processor_type, logfile=logfile)
        host = 'localhost'
    else:
        self._proc = None
    self._link = ida_connect(host, port, retry=retry)
    for m in IDA_MODULES:
        try:
            setattr(self, m, self._link.root.getmodule(m))
        except ImportError:
            pass
    self.remote_idalink_module = self._link.root.getmodule('idalink')
    self.remote_link = self.remote_idalink_module.RemoteIDALink(filename)
    self._memory = None
    self.pull_memory = pull_memory
    self._permissions = None
    self.filename = filename

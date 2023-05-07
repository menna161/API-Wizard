from __future__ import absolute_import
import contextlib
import ctypes
import errno
import os.path
import shutil
import socket
import ssl
import threading
import weakref
from .. import util
from ._securetransport.bindings import Security, SecurityConst, CoreFoundation
from ._securetransport.low_level import _assert_no_error, _cert_array_from_pem, _temporary_keychain, _load_client_cert_chain
from socket import _fileobject
from ..packages.backports.makefile import backport_makefile


def _drop(self):
    if (self._makefile_refs < 1):
        self.close()
    else:
        self._makefile_refs -= 1

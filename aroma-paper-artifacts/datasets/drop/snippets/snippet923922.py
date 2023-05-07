from __future__ import absolute_import
import OpenSSL.SSL
from cryptography import x509
from cryptography.hazmat.backends.openssl import backend as openssl_backend
from cryptography.hazmat.backends.openssl.x509 import _Certificate
from socket import timeout, error as SocketError
from io import BytesIO
import logging
import ssl
from ..packages import six
import sys
from .. import util
from cryptography.x509 import UnsupportedExtension
from socket import _fileobject
from cryptography.x509.extensions import Extensions
from OpenSSL.crypto import X509
from ..packages.backports.makefile import backport_makefile
import idna


def _drop(self):
    if (self._makefile_refs < 1):
        self.close()
    else:
        self._makefile_refs -= 1

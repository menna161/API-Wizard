from __future__ import absolute_import
import datetime
import logging
import os
import socket
from socket import error as SocketError, timeout as SocketTimeout
import warnings
from .packages import six
from .packages.six.moves.http_client import HTTPConnection as _HTTPConnection
from .packages.six.moves.http_client import HTTPException
from .exceptions import NewConnectionError, ConnectTimeoutError, SubjectAltNameWarning, SystemTimeWarning
from .packages.ssl_match_hostname import match_hostname, CertificateError
from .util.ssl_ import resolve_cert_reqs, resolve_ssl_version, assert_fingerprint, create_urllib3_context, ssl_wrap_socket
from .util import connection
from ._collections import HTTPHeaderDict
import ssl


def connect(self):
    conn = self._new_conn()
    hostname = self.host
    if getattr(self, '_tunnel_host', None):
        self.sock = conn
        self._tunnel()
        self.auto_open = 0
        hostname = self._tunnel_host
    server_hostname = hostname
    if (self.server_hostname is not None):
        server_hostname = self.server_hostname
    is_time_off = (datetime.date.today() < RECENT_DATE)
    if is_time_off:
        warnings.warn('System time is way off (before {0}). This will probably lead to SSL verification errors'.format(RECENT_DATE), SystemTimeWarning)
    default_ssl_context = False
    if (self.ssl_context is None):
        default_ssl_context = True
        self.ssl_context = create_urllib3_context(ssl_version=resolve_ssl_version(self.ssl_version), cert_reqs=resolve_cert_reqs(self.cert_reqs))
    context = self.ssl_context
    context.verify_mode = resolve_cert_reqs(self.cert_reqs)
    if ((not self.ca_certs) and (not self.ca_cert_dir) and default_ssl_context and hasattr(context, 'load_default_certs')):
        context.load_default_certs()
    self.sock = ssl_wrap_socket(sock=conn, keyfile=self.key_file, certfile=self.cert_file, key_password=self.key_password, ca_certs=self.ca_certs, ca_cert_dir=self.ca_cert_dir, server_hostname=server_hostname, ssl_context=context)
    if self.assert_fingerprint:
        assert_fingerprint(self.sock.getpeercert(binary_form=True), self.assert_fingerprint)
    elif ((context.verify_mode != ssl.CERT_NONE) and (not getattr(context, 'check_hostname', False)) and (self.assert_hostname is not False)):
        cert = self.sock.getpeercert()
        if (not cert.get('subjectAltName', ())):
            warnings.warn('Certificate for {0} has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/urllib3/urllib3/issues/497 for details.)'.format(hostname), SubjectAltNameWarning)
        _match_hostname(cert, (self.assert_hostname or server_hostname))
    self.is_verified = ((context.verify_mode == ssl.CERT_REQUIRED) or (self.assert_fingerprint is not None))

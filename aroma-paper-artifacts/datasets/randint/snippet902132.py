import sys
import logging
import os
import os.path
import random
import ssl
import tempfile
import argparse
from .. import DeenPlugin
from deen.exceptions import MissingDependencyException
import http.server
import socketserver
import OpenSSL.crypto
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import OpenSSL.crypto


def _generate_pki(self):
    'Generate a random CA certificate and use it to\n        sign a randomly generated server certificate. If\n        SSL/TLS mode is enabled and no server certificate/\n        private key has been supplied via CLI arguments,\n        this function will generate temporary certificates\n        randomly.'
    ca_key = OpenSSL.crypto.PKey()
    ca_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    ca_cert = OpenSSL.crypto.X509()
    ca_cert.set_version(2)
    ca_cert.set_serial_number(random.randint(50000000, 100000000))
    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = self.ca_common_name
    ca_cert.add_extensions([OpenSSL.crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=ca_cert)])
    ca_cert.add_extensions([OpenSSL.crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always', issuer=ca_cert)])
    ca_cert.add_extensions([OpenSSL.crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'), OpenSSL.crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')])
    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)
    ca_cert.sign(ca_key, 'sha256')
    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(((((10 * 365) * 24) * 60) * 60))
    self.ca_cert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert)
    self.ca_key_pem = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, ca_key)
    server_key = OpenSSL.crypto.PKey()
    server_key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    server_cert = OpenSSL.crypto.X509()
    server_cert.set_version(2)
    server_cert.set_serial_number(random.randint(50000000, 100000000))
    server_subj = server_cert.get_subject()
    server_subj.commonName = 'deen server'
    server_cert.add_extensions([OpenSSL.crypto.X509Extension(b'basicConstraints', False, b'CA:FALSE'), OpenSSL.crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=server_cert)])
    server_cert.add_extensions([OpenSSL.crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always', issuer=ca_cert), OpenSSL.crypto.X509Extension(b'extendedKeyUsage', False, b'serverAuth'), OpenSSL.crypto.X509Extension(b'keyUsage', False, b'digitalSignature')])
    server_cert.set_issuer(ca_subj)
    server_cert.set_pubkey(server_key)
    server_cert.sign(ca_key, 'sha256')
    server_cert.gmtime_adj_notBefore(0)
    server_cert.gmtime_adj_notAfter(((((10 * 365) * 24) * 60) * 60))
    self.server_cert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, server_cert)
    self.server_key_pem = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, server_key)

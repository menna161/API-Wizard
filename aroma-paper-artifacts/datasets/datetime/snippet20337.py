import codecs
from collections import deque
import contextlib
import csv
from glob import iglob as std_iglob
import io
import json
import logging
import os
import py_compile
import re
import socket
import subprocess
import sys
import tarfile
import tempfile
import textwrap
import time
from . import DistlibException
from .compat import string_types, text_type, shutil, raw_input, StringIO, cache_from_source, urlopen, urljoin, httplib, xmlrpclib, splittype, HTTPHandler, BaseConfigurator, valid_ident, Container, configparser, URLError, ZipFile, fsdecode, unquote, urlparse
import ssl
import threading
from .compat import HTTPSHandler as BaseHTTPSHandler, match_hostname, CertificateError
import dummy_threading as threading


def __init__(self, uri, **kwargs):
    self.timeout = timeout = kwargs.pop('timeout', None)
    if (timeout is not None):
        (scheme, _) = splittype(uri)
        use_datetime = kwargs.get('use_datetime', 0)
        if (scheme == 'https'):
            tcls = SafeTransport
        else:
            tcls = Transport
        kwargs['transport'] = t = tcls(timeout, use_datetime=use_datetime)
        self.transport = t
    xmlrpclib.ServerProxy.__init__(self, uri, **kwargs)

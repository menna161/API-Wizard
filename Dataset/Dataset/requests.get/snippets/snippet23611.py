import types
import sys, os, getopt, time, codecs, re
import requests
import socket
import tempfile
import hashlib
import platform
from subprocess import Popen
from subprocess import STDOUT
from os import walk
import signal
import logging
import io
import ctypes
from urllib import urlretrieve
from urlparse import urlparse
from rfc6266 import build_header
from urllib.request import urlretrieve
from urllib.parse import urlparse as urlparse
import ssl
import ssl


def callServer(verb, serverEndpoint, service, data, headers, verbose=Verbose, tikaServerJar=TikaServerJar, httpVerbs={'get': requests.get, 'put': requests.put, 'post': requests.post}, classpath=None, rawResponse=False, config_path=None, requestOptions={}):
    '\n    Call the Tika Server, do some error checking, and return the response.\n    :param verb:\n    :param serverEndpoint:\n    :param service:\n    :param data:\n    :param headers:\n    :param verbose:\n    :param tikaServerJar:\n    :param httpVerbs:\n    :param classpath:\n    :return:\n    '
    parsedUrl = urlparse(serverEndpoint)
    serverHost = parsedUrl.hostname
    scheme = parsedUrl.scheme
    port = parsedUrl.port
    if (classpath is None):
        classpath = TikaServerClasspath
    global TikaClientOnly
    if (not TikaClientOnly):
        serverEndpoint = checkTikaServer(scheme, serverHost, port, tikaServerJar, classpath, config_path)
    serviceUrl = (serverEndpoint + service)
    if (verb not in httpVerbs):
        log.exception(('Tika Server call must be one of %s' % binary_string(httpVerbs.keys())))
        raise TikaException(('Tika Server call must be one of %s' % binary_string(httpVerbs.keys())))
    verbFn = httpVerbs[verb]
    if (Windows and hasattr(data, 'read')):
        data = data.read()
    encodedData = data
    if (type(data) is unicode_string):
        encodedData = data.encode('utf-8')
    requestOptionsDefault = {'timeout': 60, 'headers': headers, 'verify': False}
    effectiveRequestOptions = requestOptionsDefault.copy()
    effectiveRequestOptions.update(requestOptions)
    resp = verbFn(serviceUrl, encodedData, **effectiveRequestOptions)
    if verbose:
        print(sys.stderr, 'Request headers: ', headers)
        print(sys.stderr, 'Response headers: ', resp.headers)
    if (resp.status_code != 200):
        log.warning('Tika server returned status: %d', resp.status_code)
    resp.encoding = 'utf-8'
    if rawResponse:
        return (resp.status_code, resp.content)
    else:
        return (resp.status_code, resp.text)

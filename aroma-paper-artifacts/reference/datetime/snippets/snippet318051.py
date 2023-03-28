import hashlib
import hmac
import base64
import time
import calendar
import logging
import sys
import platform
import datetime
from email.utils import parsedate
import google.protobuf.text_format as text_format
import tablestore
from tablestore.error import *
from tablestore.encoder import OTSProtoBufferEncoder
from tablestore.decoder import OTSProtoBufferDecoder
import tablestore.protobuf.table_store_pb2 as pb2
import tablestore.protobuf.table_store_filter_pb2 as filter_pb2
from urlparse import urlparse, parse_qsl
from urllib import urlencode
from urllib.parse import urlparse, parse_qsl, urlencode


def _check_headers(self, headers, body, status=None):
    header_names = ['x-ots-contentmd5', 'x-ots-requestid', 'x-ots-date', 'x-ots-contenttype']
    if (200 <= status < 300):
        for name in header_names:
            if (not (name in headers)):
                raise OTSClientError(('"%s" is missing in response header.' % name))
    if ('x-ots-contentmd5' in headers):
        md5 = base64.b64encode(hashlib.md5(body).digest()).decode(self.encoding)
        if (md5 != headers['x-ots-contentmd5']):
            raise OTSClientError('MD5 mismatch in response.')
    if ('x-ots-date' in headers):
        try:
            server_time = datetime.datetime.strptime(headers['x-ots-date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            raise OTSClientError('Invalid date format in response.')
        server_unix_time = time.mktime(server_time.timetuple())
        now_unix_time = time.mktime(datetime.datetime.utcnow().timetuple())
        if (abs((server_unix_time - now_unix_time)) > (15 * 60)):
            raise OTSClientError('The difference between date in response and system time is more than 15 minutes.')

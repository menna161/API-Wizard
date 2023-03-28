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


def _make_headers(self, body, query):
    md5 = base64.b64encode(hashlib.md5(body).digest()).decode(self.encoding)
    date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    headers = {'x-ots-date': date, 'x-ots-apiversion': self.api_version, 'x-ots-accesskeyid': self.user_id, 'x-ots-instancename': self.instance_name, 'x-ots-contentmd5': md5}
    if (self.sts_token != None):
        headers['x-ots-ststoken'] = self.sts_token
    signature = self._make_request_signature(query, headers)
    headers['x-ots-signature'] = signature
    headers['User-Agent'] = self.user_agent
    return headers

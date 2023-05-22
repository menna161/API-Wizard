import sys
import base64
import json
import re
import requests
import os
import uuid
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from Crypto.Hash import SHA1
from struct import Struct
from operator import xor
from itertools import starmap
import binascii
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def upload(data, url, proxy=False):
    global CERT_VERIFY
    sys.stderr.write((('Preparing to send request to ' + url) + '\n'))
    session = requests.Session()
    request = requests.Request('POST', url, data=data)
    request = request.prepare()
    request.headers['Content-Type'] = ('multipart/form-data; ' + 'boundary=---------------------------62616f37756f2f')
    response = session.send(request, verify=CERT_VERIFY, proxies=getProxy(proxy))
    sys.stderr.write('Request done\n')
    return response.text

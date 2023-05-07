import base64
import hashlib
import hmac
import logging
import socket
import sys
import json
from multiprocessing import Process, Manager, Queue, pool
from threading import RLock, Thread
from datetime import datetime
import time
from .commons import synchronized_with_attr, truncate, python_version_bellow
from .params import group_key, parse_key, is_valid
from .server import get_server_list
from .files import read_file, save_file, delete_file
import ssl
from http import HTTPStatus
from urllib.request import Request, urlopen
from urllib.parse import urlencode, unquote_plus
from urllib.error import HTTPError, URLError
from aliyunsdkcore.client import AcsClient
from aliyunsdkkms.request.v20160120.DecryptRequest import DecryptRequest
from aliyunsdkkms.request.v20160120.EncryptRequest import EncryptRequest
from aliyunsdkcore.auth.credentials import EcsRamRoleCredential
from aliyunsdkcore.auth.signers.ecs_ram_role_signer import EcsRamRoleSigner
import httplib as HTTPStatus
from urllib2 import Request, urlopen, HTTPError, URLError
from urllib import urlencode, unquote_plus


def _refresh_sts_token(self):
    if self.sts_token:
        if ((self.sts_token['client_expiration'] - time.mktime(time.gmtime())) > (3 * 60)):
            return
    try:
        resp = urlopen(('http://100.100.100.200/latest/meta-data/ram/security-credentials/' + self.ram_role_name))
        server_time = time.mktime(datetime.strptime(resp.headers['Date'], '%a, %d %b %Y %H:%M:%S GMT').timetuple())
        sts_token = json.loads(resp.read().decode('utf8'))
        expiration = time.mktime(datetime.strptime(sts_token['Expiration'], '%Y-%m-%dT%H:%M:%SZ').timetuple())
        sts_token['client_expiration'] = ((expiration - server_time) + time.mktime(time.gmtime()))
        self.sts_token = sts_token
    except Exception as e:
        logger.error(('[refresh-sts-token] get sts token failed, due to %s' % e.message))
        raise ACMRequestException('Refresh sts token failed.')

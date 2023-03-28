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


def _check_session_credential_patch(self):
    if (not hasattr(self, '_expiration')):
        self._refresh_session_ak_and_sk()
        return
    expiration = (self._expiration if isinstance(self._expiration, (float, int)) else time.mktime(datetime.strptime(self._expiration, '%Y-%m-%dT%H:%M:%SZ').timetuple()))
    now = time.mktime(time.gmtime())
    if ((expiration - now) < (3 * 60)):
        self._refresh_session_ak_and_sk()

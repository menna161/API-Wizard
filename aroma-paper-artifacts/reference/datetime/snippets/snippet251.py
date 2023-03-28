import datetime
import logging
import os
from typing import Dict, Tuple, Union, Any, TypeVar, Type
import hvac
from django.apps.config import AppConfig
from django.db.backends.base.base import BaseDatabaseWrapper
from requests.exceptions import RequestException
from django_dbconn_retry import pre_reconnect


def __init__(self, vaulturl: str, vaultauth: VaultAuthentication, secretpath: str, pin_cacert: str=None, ssl_verify: bool=False, debug_output: bool=False) -> None:
    self.vaulturl = vaulturl
    self._vaultauth = vaultauth
    self.secretpath = secretpath
    self.pin_cacert = pin_cacert
    self.ssl_verify = ssl_verify
    self.debug_output = debug_output
    self._cache = None
    self._leasetime = None
    self._updatetime = None
    self._lease_id = None

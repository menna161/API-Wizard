import datetime
import logging
import os
from typing import Dict, Tuple, Union, Any, TypeVar, Type
import hvac
from django.apps.config import AppConfig
from django.db.backends.base.base import BaseDatabaseWrapper
from requests.exceptions import RequestException
from django_dbconn_retry import pre_reconnect


def _refresh(self) -> None:
    vcl = self._vaultauth.authenticated_client(url=self.vaulturl, verify=(self.pin_cacert if self.pin_cacert else self.ssl_verify))
    try:
        result = vcl.read(self.secretpath)
    except RequestException as e:
        raise VaultCredentialProviderException(("Unable to read credentials from path '%s' with request error: %s" % (self.secretpath, str(e)))) from e
    if (('data' not in result) or ('username' not in result['data']) or ('password' not in result['data'])):
        raise VaultCredentialProviderException(('Read dict from Vault path %s did not match expected structure (data->{username, password}): %s' % (self.secretpath, str(result))))
    self._cache = result['data']
    self._lease_id = result['lease_id']
    self._leasetime = self._now()
    self._updatetime = (self._leasetime + datetime.timedelta(seconds=int(result['lease_duration'])))
    _log.debug('Loaded new Vault DB credentials from %s:\nlease_id=%s\nleasetime=%s\nduration=%s\nusername=%s\npassword=%s', self.secretpath, self._lease_id, str(self._leasetime), result['lease_duration'], self._cache['username'], (self._cache['password'] if self.debug_output else 'Password withheld, debug output is disabled'))

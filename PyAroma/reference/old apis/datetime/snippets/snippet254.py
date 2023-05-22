import datetime
import logging
import os
from typing import Dict, Tuple, Union, Any, TypeVar, Type
import hvac
from django.apps.config import AppConfig
from django.db.backends.base.base import BaseDatabaseWrapper
from requests.exceptions import RequestException
from django_dbconn_retry import pre_reconnect


def _get_or_update(self, key: str) -> str:
    if ((self._cache is None) or ((self._updatetime - self._now()).total_seconds() < 10)):
        _log.info(('Vault DB credential lease has expired, refreshing for %s' % key))
        self._refresh()
        _log.info(('refresh done (%s, %s)' % (self._lease_id, str(self._updatetime))))
    return self._cache[key]

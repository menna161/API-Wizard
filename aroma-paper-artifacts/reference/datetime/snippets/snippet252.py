import datetime
import logging
import os
from typing import Dict, Tuple, Union, Any, TypeVar, Type
import hvac
from django.apps.config import AppConfig
from django.db.backends.base.base import BaseDatabaseWrapper
from requests.exceptions import RequestException
from django_dbconn_retry import pre_reconnect


def _now(self) -> datetime.datetime:
    return datetime.datetime.now()

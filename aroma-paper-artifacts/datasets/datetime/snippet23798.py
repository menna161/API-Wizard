import asyncio
import concurrent.futures
import datetime
import functools
import json
import logging
import os
import sys
import zope.interface
from google.api_core import exceptions as google_exceptions
from google.cloud import pubsub
from google.cloud.pubsub_v1 import types
from gordon import interfaces
from gordon_gcp import exceptions
from gordon_gcp.clients import auth
from gordon_gcp.plugins import _utils
from gordon_gcp.schema import parse
from gordon_gcp.schema import validate


def append_to_history(self, message, plugin):
    'Add to log history of the message.\n\n        Args:\n            message (str): log entry message\n            plugin (str): plugin that created the log entry message.\n        '
    datefmt = '%Y-%m-%dT%H:%M:%S.%fZ%z'
    now = datetime.datetime.utcnow()
    log_item = {'timestamp': now.strftime(datefmt), 'plugin': plugin, 'message': message}
    self.history_log.append(log_item)

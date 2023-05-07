import asyncio
import datetime
import functools
import json
import logging
import os
import zope.interface
from asyncio_extras import threads
from google.api_core import exceptions as google_exceptions
from google.cloud import pubsub
from gordon_janitor import interfaces
from gordon_gcp import exceptions
from gordon_gcp.clients import auth


@threads.threadpool
def publish(self, message):
    'Publish received change message to Google Pub/Sub.\n\n        Args:\n            message (dict): change message received from the\n                :obj:`changes_channel` to emit.\n        '
    message['timestamp'] = datetime.datetime.utcnow().isoformat()
    bytes_message = bytes(json.dumps(message), encoding='utf-8')
    future = self.publisher.publish(self.topic, bytes_message)
    self._messages.add(future)
    future.add_done_callback(functools.partial(self._message_publish_callback, message))

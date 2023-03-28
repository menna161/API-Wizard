from __future__ import unicode_literals
import datetime
import calendar
import json
import six
from uamqp import Message, BatchMessage
from uamqp import types, constants, errors
from uamqp.message import MessageHeader, MessageProperties


@property
def enqueued_time(self):
    '\n        The enqueued timestamp of the event data object.\n\n        :rtype: datetime.datetime\n        '
    timestamp = self._annotations.get(EventData.PROP_TIMESTAMP, None)
    if timestamp:
        return datetime.datetime.utcfromtimestamp((float(timestamp) / 1000))
    return None

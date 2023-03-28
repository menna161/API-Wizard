from __future__ import unicode_literals
import datetime
import calendar
import json
import six
from uamqp import Message, BatchMessage
from uamqp import types, constants, errors
from uamqp.message import MessageHeader, MessageProperties


def __init__(self, value, inclusive=False):
    '\n        Initialize Offset.\n\n        :param value: The offset value.\n        :type value: ~datetime.datetime or int or str\n        :param inclusive: Whether to include the supplied value as the start point.\n        :type inclusive: bool\n        '
    self.value = value
    self.inclusive = inclusive

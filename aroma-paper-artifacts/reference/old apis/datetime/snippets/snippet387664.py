from __future__ import unicode_literals
import datetime
import calendar
import json
import six
from uamqp import Message, BatchMessage
from uamqp import types, constants, errors
from uamqp.message import MessageHeader, MessageProperties


def selector(self):
    '\n        Creates a selector expression of the offset.\n\n        :rtype: bytes\n        '
    operator = ('>=' if self.inclusive else '>')
    if isinstance(self.value, datetime.datetime):
        timestamp = ((calendar.timegm(self.value.utctimetuple()) * 1000) + (self.value.microsecond / 1000))
        return "amqp.annotation.x-opt-enqueued-time {} '{}'".format(operator, int(timestamp)).encode('utf-8')
    if isinstance(self.value, six.integer_types):
        return "amqp.annotation.x-opt-sequence-number {} '{}'".format(operator, self.value).encode('utf-8')
    return "amqp.annotation.x-opt-offset {} '{}'".format(operator, self.value).encode('utf-8')

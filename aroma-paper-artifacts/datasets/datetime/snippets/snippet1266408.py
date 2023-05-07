from __future__ import unicode_literals
from .utils import Event
from .eventloop import AsyncGeneratorItem, From, ensure_future, consume_async_generator, generator_to_async_generator
from abc import ABCMeta, abstractmethod
from six import with_metaclass, text_type
import datetime
import os


def store_string(self, string):
    with open(self.filename, 'ab') as f:

        def write(t):
            f.write(t.encode('utf-8'))
        write(('\n# %s\n' % datetime.datetime.now()))
        for line in string.split('\n'):
            write(('+%s\n' % line))

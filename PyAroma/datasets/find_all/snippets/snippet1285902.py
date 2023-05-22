from __future__ import unicode_literals
from .controls import UIControl, BufferControl
from .containers import Container, Window, to_container, ConditionalContainer
from prompt_toolkit.buffer import Buffer
import six


def find_all_windows(self):
    '\n        Find all the :class:`.UIControl` objects in this layout.\n        '
    for item in self.walk():
        if isinstance(item, Window):
            (yield item)

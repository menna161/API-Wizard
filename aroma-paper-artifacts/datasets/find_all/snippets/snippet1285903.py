from __future__ import unicode_literals
from .controls import UIControl, BufferControl
from .containers import Container, Window, to_container, ConditionalContainer
from prompt_toolkit.buffer import Buffer
import six


def find_all_controls(self):
    for container in self.find_all_windows():
        (yield container.content)

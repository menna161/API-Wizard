from __future__ import unicode_literals
from .controls import UIControl, BufferControl
from .containers import Container, Window, to_container, ConditionalContainer
from prompt_toolkit.buffer import Buffer
import six


def __init__(self, container, focused_element=None):
    self.container = to_container(container)
    self._stack = []
    self.search_links = {}
    self._child_to_parent = {}
    if (focused_element is None):
        try:
            self._stack.append(next(self.find_all_windows()))
        except StopIteration:
            raise InvalidLayoutError('Invalid layout. The layout does not contain any Window object.')
    else:
        self.focus(focused_element)
    self.visible_windows = []

from __future__ import unicode_literals
from .controls import UIControl, BufferControl
from .containers import Container, Window, to_container, ConditionalContainer
from prompt_toolkit.buffer import Buffer
import six


@current_control.setter
def current_control(self, control):
    '\n        Set the :class:`.UIControl` to receive the focus.\n        '
    assert isinstance(control, UIControl)
    for window in self.find_all_windows():
        if (window.content == control):
            self.current_window = window
            return
    raise ValueError('Control not found in the user interface.')

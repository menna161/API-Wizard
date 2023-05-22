from __future__ import unicode_literals
from .controls import UIControl, BufferControl
from .containers import Container, Window, to_container, ConditionalContainer
from prompt_toolkit.buffer import Buffer
import six


def focus(self, value):
    '\n        Focus the given UI element.\n\n        `value` can be either:\n\n        - a :class:`.UIControl`\n        - a :class:`.Buffer` instance or the name of a :class:`.Buffer`\n        - a :class:`.Window`\n        - Any container object. In this case we will focus the :class:`.Window`\n          from this container that was focused most recent, or the very first\n          focusable :class:`.Window` of the container.\n        '
    if isinstance(value, six.text_type):
        for control in self.find_all_controls():
            if (isinstance(control, BufferControl) and (control.buffer.name == value)):
                self.focus(control)
                return
        raise ValueError(("Couldn't find Buffer in the current layout: %r." % (value,)))
    elif isinstance(value, Buffer):
        for control in self.find_all_controls():
            if (isinstance(control, BufferControl) and (control.buffer == value)):
                self.focus(control)
                return
        raise ValueError(("Couldn't find Buffer in the current layout: %r." % (value,)))
    elif isinstance(value, UIControl):
        if (value not in self.find_all_controls()):
            raise ValueError('Invalid value. Container does not appear in the layout.')
        if (not value.is_focusable()):
            raise ValueError('Invalid value. UIControl is not focusable.')
        self.current_control = value
    else:
        value = to_container(value)
        if isinstance(value, Window):
            if (value not in self.find_all_windows()):
                raise ValueError(('Invalid value. Window does not appear in the layout: %r' % (value,)))
            self.current_window = value
        else:
            windows = []
            for c in walk(value, skip_hidden=True):
                if (isinstance(c, Window) and c.content.is_focusable()):
                    windows.append(c)
            for w in reversed(self._stack):
                if (w in windows):
                    self.current_window = w
                    return
            if windows:
                self.current_window = windows[0]
                return
            raise ValueError(('Invalid value. Container cannot be focused: %r' % (value,)))

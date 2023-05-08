from __future__ import unicode_literals
import bisect
import re
import six
import string
import weakref
from six.moves import range, map
from .clipboard import ClipboardData
from .filters import vi_mode
from .selection import SelectionType, SelectionState, PasteMode


def find_all(self, sub, ignore_case=False):
    '\n        Find all occurrences of the substring. Return a list of absolute\n        positions in the document.\n        '
    flags = (re.IGNORECASE if ignore_case else 0)
    return [a.start() for a in re.finditer(re.escape(sub), self.text, flags)]

import types
import operator
from collections import deque
from jinja2.utils import Markup
from jinja2._compat import izip, with_metaclass, text_type, PY2
from .compiler import has_safe_repr


def find(self, node_type):
    'Find the first node of a given type.  If no such node exists the\n        return value is `None`.\n        '
    for result in self.find_all(node_type):
        return result

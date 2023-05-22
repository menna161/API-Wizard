import types
import operator
from collections import deque
from jinja2.utils import Markup
from jinja2._compat import izip, with_metaclass, text_type, PY2
from .compiler import has_safe_repr


def find_all(self, node_type):
    'Find all the nodes of a given type.  If the type is a tuple,\n        the check is performed for any of the tuple items.\n        '
    for child in self.iter_child_nodes():
        if isinstance(child, node_type):
            (yield child)
        for result in child.find_all(node_type):
            (yield result)

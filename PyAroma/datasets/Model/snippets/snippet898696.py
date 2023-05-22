from typing import Union, Mapping, Callable, Any, List, Set, cast
import copy
import logging
from penman.exceptions import LayoutError
from penman.types import Variable, Role, BasicTriple, Branch, Node
from penman.epigraph import Epidatum
from penman.surface import Alignment, RoleAlignment
from penman.tree import Tree, is_atomic
from penman.graph import Graph, CONCEPT_ROLE
from penman.model import Model


def rearrange(t: Tree, key: Callable[([Role], Any)]=None, attributes_first: bool=False) -> None:
    "\n    Sort the branches at each node in tree *t* according to *key*.\n\n    Each node in a tree contains a list of branches. This function\n    sorts those lists in-place using the *key* function, which accepts\n    a role and returns some sortable criterion.\n\n    If the *attributes_first* argument is ``True``, attribute branches\n    are appear before any edges.\n\n    Instance branches (``/``) always appear before any other branches.\n\n    Example:\n        >>> from penman import layout\n        >>> from penman.model import Model\n        >>> from penman.codec import PENMANCodec\n        >>> c = PENMANCodec()\n        >>> t = c.parse(\n        ...   '(s / see-01'\n        ...   '   :ARG1 (c / cat)'\n        ...   '   :ARG0 (d / dog))')\n        >>> layout.rearrange(t, key=Model().canonical_order)\n        >>> print(c.format(t))\n        (s / see-01\n           :ARG0 (d / dog)\n           :ARG1 (c / cat))\n    "
    if attributes_first:
        variables = {node[0] for node in t.nodes()}
    else:
        variables = set()

    def sort_key(branch: Branch):
        (role, target) = branch
        if is_atomic(target):
            criterion1 = (target in variables)
        else:
            criterion1 = (target[0] in variables)
        criterion2 = (True if (key is None) else key(role))
        return (criterion1, criterion2)
    _rearrange(t.node, sort_key)

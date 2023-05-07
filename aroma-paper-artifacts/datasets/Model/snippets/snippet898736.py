from typing import Optional, Dict, Set, List, Tuple
import logging
from penman.types import Variable, Target, BasicTriple, Node
from penman.exceptions import ModelError
from penman.epigraph import Epidatum, Epidata
from penman.surface import Alignment, RoleAlignment, alignments
from penman.tree import Tree, is_atomic
from penman.graph import Graph, CONCEPT_ROLE
from penman.model import Model
from penman.layout import Push, Pop, POP, appears_inverted, get_pushed_variable


def canonicalize_roles(t: Tree, model: Model) -> Tree:
    "\n    Normalize roles in *t* so they are canonical according to *model*.\n\n    This is a tree transformation instead of a graph transformation\n    because the orientation of the pure graph's triples is not decided\n    until the graph is configured into a tree.\n\n    Args:\n        t: a :class:`~penman.tree.Tree` object\n        model: a model defining role normalizations\n    Returns:\n        A new :class:`~penman.tree.Tree` object with canonicalized\n        roles.\n    Example:\n        >>> from penman.codec import PENMANCodec\n        >>> from penman.models.amr import model\n        >>> from penman.transform import canonicalize_roles\n        >>> codec = PENMANCodec()\n        >>> t = codec.parse('(c / chapter :domain-of 7)')\n        >>> t = canonicalize_roles(t, model)\n        >>> print(codec.format(t))\n        (c / chapter\n           :mod 7)\n    "
    if (model is None):
        model = Model()
    tree = Tree(_canonicalize_node(t.node, model), metadata=t.metadata)
    logger.info('Canonicalized roles: %s', tree)
    return tree

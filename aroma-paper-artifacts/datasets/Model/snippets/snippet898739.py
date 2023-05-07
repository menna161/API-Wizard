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


def dereify_edges(g: Graph, model: Model) -> Graph:
    "\n    Dereify edges in *g* that have reifications in *model*.\n\n    Args:\n        g: a :class:`~penman.graph.Graph` object\n    Returns:\n        A new :class:`~penman.graph.Graph` object with dereified\n        edges.\n    Example:\n        >>> from penman.codec import PENMANCodec\n        >>> from penman.models.amr import model\n        >>> from penman.transform import dereify_edges\n        >>> codec = PENMANCodec(model=model)\n        >>> g = codec.decode(\n        ...   '(c / chapter'\n        ...   '   :ARG1-of (_ / have-mod-91'\n        ...   '               :ARG2 7))')\n        >>> g = dereify_edges(g, model)\n        >>> print(codec.encode(g))\n        (c / chapter\n           :mod 7)\n    "
    if (model is None):
        model = Model()
    agenda = _dereify_agenda(g, model)
    new_epidata = dict(g.epidata)
    new_triples: List[BasicTriple] = []
    for triple in g.triples:
        var = triple[0]
        if (var in agenda):
            (first, dereified, epidata) = agenda[var]
            if (triple == first):
                new_triples.append(dereified)
                new_epidata[dereified] = epidata
            if (triple in new_epidata):
                del new_epidata[triple]
        else:
            new_triples.append(triple)
    g = Graph(new_triples, epidata=new_epidata, metadata=g.metadata)
    logger.info('Dereified edges: %s', g)
    return g

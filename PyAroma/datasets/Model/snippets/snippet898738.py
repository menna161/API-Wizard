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


def reify_edges(g: Graph, model: Model) -> Graph:
    "\n    Reify all edges in *g* that have reifications in *model*.\n\n    Args:\n        g: a :class:`~penman.graph.Graph` object\n        model: a model defining reifications\n    Returns:\n        A new :class:`~penman.graph.Graph` object with reified edges.\n    Example:\n        >>> from penman.codec import PENMANCodec\n        >>> from penman.models.amr import model\n        >>> from penman.transform import reify_edges\n        >>> codec = PENMANCodec(model=model)\n        >>> g = codec.decode('(c / chapter :mod 7)')\n        >>> g = reify_edges(g, model)\n        >>> print(codec.encode(g))\n        (c / chapter\n           :ARG1-of (_ / have-mod-91\n                       :ARG2 7))\n    "
    vars = g.variables()
    if (model is None):
        model = Model()
    new_epidata = dict(g.epidata)
    new_triples: List[BasicTriple] = []
    for triple in g.triples:
        if model.is_role_reifiable(triple[1]):
            (in_triple, node_triple, out_triple) = model.reify(triple, vars)
            if appears_inverted(g, triple):
                (in_triple, out_triple) = (out_triple, in_triple)
            new_triples.extend((in_triple, node_triple, out_triple))
            var = node_triple[0]
            vars.add(var)
            new_epidata[in_triple] = [Push(var)]
            old_epis = (new_epidata.pop(triple) if (triple in new_epidata) else [])
            (node_epis, out_epis) = _edge_markers(old_epis)
            new_epidata[node_triple] = node_epis
            new_epidata[out_triple] = out_epis
        else:
            new_triples.append(triple)
    g = Graph(new_triples, epidata=new_epidata, metadata=g.metadata)
    logger.info('Reified edges: %s', g)
    return g

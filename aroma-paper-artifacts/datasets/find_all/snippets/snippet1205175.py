import copy
import os
import re
from blockdiag import noderenderer, plugins
from blockdiag.utils import XY, images, unquote, urlutil, uuid
from blockdiag.utils.logging import warning


@classmethod
def find(cls, node1, node2=None):
    if ((node1 is None) and (node2 is None)):
        return cls.find_all()
    elif isinstance(node1, NodeGroup):
        edges = cls.find(None, node2)
        edges = (e for e in edges if e.node1.group.is_parent(node1))
        return [e for e in edges if (not e.node2.group.is_parent(node1))]
    elif isinstance(node2, NodeGroup):
        edges = cls.find(node1, None)
        edges = (e for e in edges if e.node2.group.is_parent(node2))
        return [e for e in edges if (not e.node1.group.is_parent(node2))]
    elif (node1 is None):
        return [e for e in cls.find_all() if (e.node2 == node2)]
    else:
        if (node1 not in cls.namespace):
            return []
        if (node2 is None):
            return cls.namespace[node1].values()
        if (node2 not in cls.namespace[node1]):
            return []
    return cls.namespace[node1][node2]

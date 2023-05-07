import copy
import os
import re
from blockdiag import noderenderer, plugins
from blockdiag.utils import XY, images, unquote, urlutil, uuid
from blockdiag.utils.logging import warning


@classmethod
def find_by_level(cls, level):
    edges = []
    for e in cls.find_all():
        edge = e.duplicate()
        skips = 0
        if (edge.node1.group.level < level):
            skips += 1
        else:
            while (edge.node1.group.level != level):
                edge.node1 = edge.node1.group
        if (edge.node2.group.level < level):
            skips += 1
        else:
            while (edge.node2.group.level != level):
                edge.node2 = edge.node2.group
        if (skips == 2):
            continue
        edges.append(edge)
    return edges

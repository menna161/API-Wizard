from blockdiag import parser
from blockdiag.elements import Diagram, DiagramEdge, DiagramNode, NodeGroup
from blockdiag.plugins import fire_node_event
from blockdiag.utils import XY, unquote
from blockdiag.utils.compat import cmp_to_key


@property
def _groups(self):
    nodes = {self.diagram: self.diagram.nodes}
    edges = {self.diagram: self.diagram.edges}
    levels = {self.diagram: self.diagram.level}
    for group in self.diagram.traverse_groups():
        nodes[group] = group.nodes
        edges[group] = group.edges
        levels[group] = group.level
    groups = {}
    orders = {}
    for node in self.diagram.traverse_nodes():
        groups[node] = node.group
        orders[node] = node.order
    for group in self.diagram.traverse_groups():
        (yield group)
        for g in nodes:
            g.nodes = nodes[g]
            g.edges = edges[g]
            g.level = levels[g]
        for n in groups:
            n.group = groups[n]
            n.order = orders[n]
            n.xy = XY(0, 0)
            n.colwidth = 1
            n.colheight = 1
            n.separated = False
        for edge in DiagramEdge.find_all():
            edge.skipped = False
            edge.crosspoints = []
    (yield self.diagram)

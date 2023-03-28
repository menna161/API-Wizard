import networkx as nx
import subprocess
import datetime
import adage.nodestate as nodestate


def colorize_graph_at_time(dag, time):
    colorized = nx.DiGraph()
    colorkey = {None: None, nodestate.DEFINED: 'grey', nodestate.RUNNING: 'yellow', nodestate.FAILED: 'red', nodestate.SUCCESS: 'green'}
    for node in dag.nodes():
        nodeobj = dag.getNode(node)
        state = state_at_time(nodeobj, time)
        color = colorkey[state]
        visible = node_visible(nodeobj, time)
        style = ('filled' if visible else 'invis')
        dot_attr = {'label': '{} '.format(nodeobj.name), 'style': style, 'color': color}
        colorized.add_node(node, **dot_attr)
        for pre in dag.predecessors(node):
            colorized.add_edge(pre, node)
    dotformat = nx.drawing.nx_pydot.to_pydot(colorized)
    dotformat.set_label(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
    for e in dotformat.get_edges():
        edge_visible = node_visible(dag.getNode(e.get_destination().replace('"', '')), time)
        if (not edge_visible):
            e.set_style('invis')
    return dotformat

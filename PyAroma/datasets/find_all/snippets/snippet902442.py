from collections import defaultdict


def find_all_connections(self, relation):
    '\n        :param relation:\n        :return: list of all edges representing this relation\n        '
    relevant_edges = []
    for edge in self.edges:
        if (edge.relation == relation):
            relevant_edges.append(edge)
    return relevant_edges

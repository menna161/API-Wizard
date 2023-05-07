import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_tour_graph(self, points, permutation_matrix):
    '\n        A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.\n        The permutation_matrix is n x n matrix, where n is the number of points in the TSP. Each row represents a point,\n        and each column represents the position of that point in the tour.\n        :param points: the list of points (tuples) which represent the points in the TSP\n        :param permutation_matrix: an n x n matrix, where n is the number of points, which represents the final tour\n        :return: a NetworkX Graph representing the tour, a dictionary defining the NetworkX positions for the Graph, and\n                 the total tour length\n        '
    assert (len(points) == len(permutation_matrix)), 'the number of rows in permutation_matrix does not match the number of points'
    assert (len(points) == len(permutation_matrix[0])), 'the number of columns in permutation_matrix does not match the number of points'
    G = nx.Graph()
    for point_index in range(len(points)):
        G.add_node(point_index)
    tour_index_to_point_index = {}
    for (point_index, row) in enumerate(permutation_matrix):
        tour_index = np.argmax(row)
        if (tour_index in tour_index_to_point_index):
            raise Exception(('a point has already claimed position #%s in the tour' % str((tour_index + 1))))
        tour_index_to_point_index[tour_index] = point_index
    distances = []
    for (tour_index, point_index) in tour_index_to_point_index.items():
        from_point_index = point_index
        to_point_index = tour_index_to_point_index[((tour_index + 1) % len(points))]
        G.add_edge(from_point_index, to_point_index)
        from_point = points[from_point_index]
        to_point = points[to_point_index]
        distances.append(math.sqrt((((to_point[0] - from_point[0]) ** 2) + ((to_point[1] - from_point[1]) ** 2))))
    pos = {i: point for (i, point) in enumerate(points)}
    return (G, pos, sum(distances))

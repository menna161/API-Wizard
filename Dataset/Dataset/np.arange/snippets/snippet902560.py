import numpy as np
import torch
import dgl
import random
import itertools
from scipy.sparse import coo_matrix


def sample_edge_neighborhood(adj_list, degrees, n_triplets, sample_size, sample=True, sampling_edge_ids=None):
    ' Edge neighborhood sampling to reduce training graph size\n    '
    if sample:
        edges = np.zeros(sample_size, dtype=np.int32)
        sample_counts = np.array([d for d in degrees])
        picked = np.array([False for _ in range(n_triplets)])
        seen = np.array([False for _ in degrees])
        i = 0
        while (i != sample_size):
            weights = (sample_counts * seen)
            if (np.sum(weights) == 0):
                weights = np.ones_like(weights)
                weights[np.where((sample_counts == 0))] = 0
            probabilities = (weights / np.sum(weights))
            chosen_vertex = np.random.choice(np.arange(degrees.shape[0]), p=probabilities)
            chosen_adj_list = adj_list[chosen_vertex]
            seen[chosen_vertex] = True
            chosen_edge = np.random.choice(np.arange(chosen_adj_list.shape[0]))
            chosen_edge = chosen_adj_list[chosen_edge]
            edge_number = chosen_edge[0]
            while picked[edge_number]:
                chosen_edge = np.random.choice(np.arange(chosen_adj_list.shape[0]))
                chosen_edge = chosen_adj_list[chosen_edge]
                edge_number = chosen_edge[0]
            edges[i] = edge_number
            other_vertex = chosen_edge[1]
            picked[edge_number] = True
            sample_counts[chosen_vertex] -= 1
            sample_counts[other_vertex] -= 1
            seen[other_vertex] = True
            i += 1
    else:
        if (sampling_edge_ids is None):
            random_edges = random.sample(range(n_triplets), sample_size)
        else:
            random_edges = np.random.choice(sampling_edge_ids, sample_size, replace=False)
        edges = np.array(random_edges)
    return edges

import numpy as np
import torch
import math
import json
import logging


def plot_degree_mrr(node_ranks):
    degree_rank = {}
    for (node, rank) in node_ranks.items():
        node_degree = node.get_degree()
        if (node_degree not in degree_rank):
            degree_rank[node_degree] = []
        degree_rank[node_degree].append((sum(rank) / len(rank)))
    degrees = []
    ranks = []
    for k in sorted(degree_rank.keys()):
        if (k < 20):
            for rank in degree_rank[k]:
                if (rank < 100):
                    degrees.append(k)
                    ranks.append(rank)
    (fig, ax) = plt.subplots()
    ax.scatter(degrees, ranks, marker='.')
    ax.set(xlabel='degree', ylabel='mean ranks')
    ax.grid()
    fig.savefig('comet_cn_degree_ranks.png')

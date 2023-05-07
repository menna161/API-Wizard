import os
import random
import code
from typing import Dict
import tensorflow as tf
import numpy as np
from graphviz import Digraph
from tqdm import tqdm


def visualize(self, name='unnamed', view=True):
    dot = Digraph(name=name)
    node_names = []
    for n_i in range(self.num_nodes):
        ord_ = (np.argmax(self.node_features['order'][n_i]) - 1)
        node_name = f"{self.attrs['value_tokens_list'][n_i]} ord={ord_}, i={n_i}"
        dot.node(node_name)
        node_names.append(node_name)
    for n_i in range(self.num_nodes):
        src_name = node_names[n_i]
        for (a_i, adj_bool) in enumerate(self.adj[n_i]):
            if adj_bool:
                targ_name = node_names[a_i]
                dot.edge(src_name, targ_name)
    os.makedirs('gviz', exist_ok=True)
    dot.render(os.path.join('gviz', f'{name}'), format='pdf', view=view)

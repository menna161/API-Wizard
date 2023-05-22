import math
import numpy as np
import board
import config


def select(self, nodes):
    best_nodes_batch = ([None] * len(nodes))
    for (i, node) in enumerate(nodes):
        current = node
        while current.expanded:
            best_edge = np.argmax(current.edge_Q_plus_U)
            if (best_edge not in current.child_nodes):
                current.child_nodes[best_edge] = Node(current, best_edge, (- current.player))
            if current.is_terminal:
                break
            if ((best_edge == config.pass_move) and (current.child_nodes[best_edge].legal_moves[config.pass_move] == 1)):
                current.is_terminal = True
                break
            current = current.child_nodes[best_edge]
        best_nodes_batch[i] = current
    return best_nodes_batch

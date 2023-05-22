import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter


def __init__(self, num_nodes, in_matrix, out_matrix, in_dim, dropout=0.0, device=torch.device('cpu'), root=None, hierarchical_label_dict=None, label_trees=None):
    '\n        TreeLSTM variant for Hierarchy Structure\n        :param num_nodes: int, N\n        :param in_matrix: numpy.Array(N, N), input adjacent matrix for child2parent (bottom-up manner)\n        :param out_matrix: numpy.Array(N, N), output adjacent matrix for parent2child (top-down manner)\n        :param in_dim: int, the dimension of each node <- config.structure_encoder.node.dimension\n        :param layers: int, the number of layers <- config.structure_encoder.num_layer\n        :param time_step: int, the number of time steps <- config.structure_encoder.time_step\n        :param dropout: Float, P value for dropout module <- configure.structure_encoder.node.dropout\n        :param prob_train: Boolean, train the probability matrix if True <- config.structure_encoder.prob_train\n        :param device: torch.device <- config.train.device_setting.device\n        :param root: Tree object of the root node\n        :param hierarchical_label_dict: Dict{parent_id: child_id}\n        :param label_trees: List[Tree]\n        '
    super(WeightedHierarchicalTreeLSTMEndtoEnd, self).__init__()
    self.root = root
    mem_dim = (in_dim // 2)
    self.hierarchical_label_dict = hierarchical_label_dict
    self.label_trees = label_trees
    self.bottom_up_lstm = WeightedChildSumTreeLSTMEndtoEnd(in_dim, mem_dim, num_nodes, in_matrix, device)
    self.top_down_lstm = WeightedTopDownTreeLSTMEndtoEnd(in_dim, mem_dim, num_nodes, out_matrix, device)
    self.tree_projection_layer = torch.nn.Linear((2 * mem_dim), mem_dim)
    self.node_dropout = torch.nn.Dropout(dropout)
    self.num_nodes = num_nodes
    self.mem_dim = mem_dim

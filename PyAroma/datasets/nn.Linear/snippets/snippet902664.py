import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter


def __init__(self, in_dim, mem_dim, num_nodes=(- 1), prob=None, device=torch.device('cpu')):
    '\n        Child-Sum variant for hierarchy-structure\n        Child-Sum treelstm paper:Tai, K. S., Socher, R., & Manning, C. D. (2015).\n            Improved semantic representations from tree-structured long short-term memory networks.\n             arXiv preprint arXiv:1503.00075.\n        :param in_dim: int, config.structure_encoder.dimension\n        :param mem_dim: int, in_dim // 2\n        :param num_nodes: int, the number of nodes in the hierarchy taxonomy\n        :param prob: numpy.array, the prior probability of the hierarchical relation\n        :param if_prob_train: Boolean, True for updating the prob\n        :param device: torch.device  <- config.train.device_setting.device\n        '
    super(WeightedChildSumTreeLSTMEndtoEnd, self).__init__()
    self.in_dim = in_dim
    self.mem_dim = mem_dim
    self.ioux = nn.Linear(self.in_dim, (3 * self.mem_dim))
    self.iouh = nn.Linear(self.mem_dim, (3 * self.mem_dim))
    self.fx = nn.Linear(self.in_dim, self.mem_dim)
    self.fh = nn.Linear(self.mem_dim, self.mem_dim)
    self.node_transformation = torch.nn.ModuleList()
    self.node_transformation_decompostion = torch.nn.ModuleList()
    self.prob = torch.Tensor(prob).to(device)
    self.prob = Parameter(self.prob)

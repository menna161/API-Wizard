import torch
import math


def __init__(self, input_size, output_size, bias=True, activation='relu', norm='batch'):
    super(DenseBlock, self).__init__()
    self.fc = torch.nn.Linear(input_size, output_size, bias=bias)
    self.norm = norm
    if (self.norm == 'batch'):
        self.bn = torch.nn.BatchNorm1d(output_size)
    elif (self.norm == 'instance'):
        self.bn = torch.nn.InstanceNorm1d(output_size)
    self.activation = activation
    if (self.activation == 'relu'):
        self.act = torch.nn.ReLU(True)
    elif (self.activation == 'prelu'):
        self.act = torch.nn.PReLU()
    elif (self.activation == 'lrelu'):
        self.act = torch.nn.LeakyReLU(0.2, True)
    elif (self.activation == 'tanh'):
        self.act = torch.nn.Tanh()
    elif (self.activation == 'sigmoid'):
        self.act = torch.nn.Sigmoid()

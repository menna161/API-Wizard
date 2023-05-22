import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_lightning.core.lightning import LightningModule
from torch.utils.data import TensorDataset, DataLoader
from torch.optim import Adam


def __init__(self, options, data=None):
    super(LightningNet, self).__init__()
    self.options = options
    self.data = data
    self.layers = nn.ModuleList()
    n_layers = options['n_layers']
    dropout = options['dropout']
    input_dim = options['n_input']
    n_classes = options['n_classes']
    for i in range(n_layers):
        output_dim = options['n_units_l{}'.format(i)]
        self.layers.append(nn.Linear(input_dim, output_dim))
        self.layers.append(nn.Dropout(dropout))
        input_dim = output_dim
    self.layers.append(nn.Linear(input_dim, n_classes))

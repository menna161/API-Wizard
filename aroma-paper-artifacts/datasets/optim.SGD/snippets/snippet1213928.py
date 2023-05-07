from helper import *
from ordered_set import OrderedSet
from torch.utils.data import DataLoader
from data_loader import *
from model import *


def add_optimizer(self, parameters):
    '\n\t\tCreates an optimizer for training the parameters\n\n\t\tParameters\n\t\t----------\n\t\tparameters:         The parameters of the model\n\t\t\n\t\tReturns\n\t\t-------\n\t\tReturns an optimizer for learning the parameters of the model\n\t\t\n\t\t'
    if (self.p.opt == 'adam'):
        return torch.optim.Adam(parameters, lr=self.p.lr, weight_decay=self.p.l2)
    else:
        return torch.optim.SGD(parameters, lr=self.p.lr, weight_decay=self.p.l2)

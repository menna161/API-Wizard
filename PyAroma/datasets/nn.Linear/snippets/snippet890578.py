import torch
from .default import NormalNN
from .regularization import SI, EWC, EWC_online
from .exp_replay import Naive_Rehearsal, GEM
from modules.criterions import BCEauto


def init_zero_weights(m):
    with torch.no_grad():
        if (type(m) == torch.nn.Linear):
            m.weight.zero_()
            m.bias.zero_()
        elif (type(m) == torch.nn.ModuleDict):
            for l in m.values():
                init_zero_weights(l)
        else:
            assert False, 'Only support linear layer'

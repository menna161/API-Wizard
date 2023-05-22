import numpy as np
import torch
from PokerRL.game.games import ALL_ENVS
from PokerRL.game.wrappers import ALL_BUILDERS


def str_to_optim_cls(optim_string):
    if (optim_string.lower() == 'sgd'):
        return torch.optim.SGD
    elif (optim_string.lower() == 'adam'):

        def fn(parameters, lr):
            return torch.optim.Adam(parameters, lr=lr)
        return fn
    elif (optim_string.lower() == 'rms'):

        def fn(parameters, lr):
            return torch.optim.RMSprop(parameters, lr=lr)
        return fn
    elif (optim_string.lower() == 'sgdmom'):

        def fn(parameters, lr):
            return torch.optim.SGD(parameters, lr=lr, momentum=0.9, nesterov=True)
        return fn
    else:
        raise ValueError(optim_string)

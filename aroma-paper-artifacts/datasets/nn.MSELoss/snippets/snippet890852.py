import numpy as np
import torch
from PokerRL.game.games import ALL_ENVS
from PokerRL.game.wrappers import ALL_BUILDERS


def str_to_loss_cls(loss_str):
    if (loss_str.lower() == 'mse'):
        return torch.nn.MSELoss()
    elif (loss_str.lower() == 'weighted_mse'):
        return (lambda y, trgt, w: torch.mean((w * ((y - trgt) ** 2))))
    elif (loss_str.lower() == 'ce'):
        return torch.nn.CrossEntropyLoss()
    elif (loss_str.lower() == 'smoothl1'):
        return torch.nn.SmoothL1Loss()
    else:
        raise ValueError(loss_str)

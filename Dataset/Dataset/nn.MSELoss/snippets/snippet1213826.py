import torch
import torch.nn as nn
from torch.nn import functional as F
from ute.utils.arg_pars import opt
from ute.utils.logging_setup import logger


def create_model():
    torch.manual_seed(opt.seed)
    model = MLP().to(opt.device)
    loss = nn.MSELoss(reduction='sum')
    optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr, weight_decay=opt.weight_decay)
    logger.debug(str(model))
    logger.debug(str(loss))
    logger.debug(str(optimizer))
    return (model, loss, optimizer)

import os
import math
import time
import datetime
from functools import reduce
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lrs


def make_optimizer(args, my_model):
    trainable = filter((lambda x: x.requires_grad), my_model.parameters())
    if (args.optimizer == 'SGD'):
        optimizer_function = optim.SGD
        kwargs = {'momentum': args.momentum}
    elif (args.optimizer == 'ADAM'):
        optimizer_function = optim.Adam
        kwargs = {'betas': (args.beta1, args.beta2), 'eps': args.epsilon}
    elif (args.optimizer == 'RMSprop'):
        optimizer_function = optim.RMSprop
        kwargs = {'eps': args.epsilon}
    kwargs['lr'] = args.lr
    kwargs['weight_decay'] = args.weight_decay
    return optimizer_function(trainable, **kwargs)

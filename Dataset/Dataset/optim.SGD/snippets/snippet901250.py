from math import sqrt
import functools
import torch
import torch.optim as optim
from torch.nn.utils import clip_grad_norm_
import apex


def build_torch_optimizer(model, opt):
    'Builds the PyTorch optimizer.\n    Input:\n        model: The model to optimize.\n        opt: The dictionary of options.\n    Output:\n        A ``torch.optim.Optimizer`` instance.\n    '
    params = list(filter((lambda p: p.requires_grad), model.parameters()))
    betas = [0.9, 0.999]
    if (opt.optim == 'sgd'):
        optimizer = optim.SGD(params, lr=opt.learning_rate)
    elif (opt.optim == 'adagrad'):
        optimizer = optim.Adagrad(params, lr=opt.learning_rate, initial_accumulator_value=opt.adagrad_accumulator_init)
    elif (opt.optim == 'adadelta'):
        optimizer = optim.Adadelta(params, lr=opt.learning_rate)
    elif (opt.optim == 'adam'):
        optimizer = optim.Adam(params, lr=opt.learning_rate, betas=betas, eps=1e-09)
    elif (opt.optim == 'fusedadam'):
        import apex
        optimizer = apex.optimizers.FusedAdam(params, lr=opt.learning_rate, betas=betas)
    else:
        raise ValueError(('Invalid optimizer type: ' + opt.optim))
    return {'optim': optimizer, 'para': params}

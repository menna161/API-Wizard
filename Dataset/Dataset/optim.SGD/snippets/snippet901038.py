import torch
from itertools import repeat


def torch_momentum_step(params, aux_params, loss, step_size, momentum, create_graph=True):
    '\n    GD with momentum step as implemented in torch.optim.SGD\n    .. math::\n              v_{t+1} = \\mu * v_{t} + g_{t+1} \\\n              p_{t+1} = p_{t} - lr * v_{t+1}\n    '
    grads = torch.autograd.grad(loss, params, create_graph=create_graph)
    new_aux_params = [((momentum * v) + g) for (v, g) in zip(aux_params, grads)]
    return ([(w - (step_size * nv)) for (w, nv) in zip(params, new_aux_params)], new_aux_params)

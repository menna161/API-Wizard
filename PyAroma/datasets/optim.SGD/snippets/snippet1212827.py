import torch
import torch.optim as optim
from torch.nn.utils import clip_grad_norm_
import operator
import functools
from copy import copy
from math import sqrt
import types
import importlib
from onmt.utils.misc import fn_args
import apex
import apex


def build_torch_optimizer(model, opt):
    'Builds the PyTorch optimizer.\n\n    We use the default parameters for Adam that are suggested by\n    the original paper https://arxiv.org/pdf/1412.6980.pdf\n    These values are also used by other established implementations,\n    e.g. https://www.tensorflow.org/api_docs/python/tf/train/AdamOptimizer\n    https://keras.io/optimizers/\n    Recently there are slightly different values used in the paper\n    "Attention is all you need"\n    https://arxiv.org/pdf/1706.03762.pdf, particularly the value beta2=0.98\n    was used there however, beta2=0.999 is still arguably the more\n    established value, so we use that here as well\n\n    Args:\n      model: The model to optimize.\n      opt. The dictionary of options.\n\n    Returns:\n      A ``torch.optim.Optimizer`` instance.\n    '
    params = [p for p in model.parameters() if p.requires_grad]
    betas = [opt.adam_beta1, opt.adam_beta2]
    if (opt.optim == 'sgd'):
        optimizer = optim.SGD(params, lr=opt.learning_rate)
    elif (opt.optim == 'adagrad'):
        optimizer = optim.Adagrad(params, lr=opt.learning_rate, initial_accumulator_value=opt.adagrad_accumulator_init)
    elif (opt.optim == 'adadelta'):
        optimizer = optim.Adadelta(params, lr=opt.learning_rate)
    elif (opt.optim == 'adafactor'):
        optimizer = AdaFactor(params, non_constant_decay=True, enable_factorization=True, weight_decay=0)
    elif (opt.optim == 'adam'):
        optimizer = optim.Adam(params, lr=opt.learning_rate, betas=betas, eps=1e-09)
    elif (opt.optim == 'sparseadam'):
        dense = []
        sparse = []
        for (name, param) in model.named_parameters():
            if (not param.requires_grad):
                continue
            if ('embed' in name):
                sparse.append(param)
            else:
                dense.append(param)
        optimizer = MultipleOptimizer([optim.Adam(dense, lr=opt.learning_rate, betas=betas, eps=1e-08), optim.SparseAdam(sparse, lr=opt.learning_rate, betas=betas, eps=1e-08)])
    elif (opt.optim == 'fusedadam'):
        optimizer = FusedAdam(params, lr=opt.learning_rate, betas=betas)
    else:
        raise ValueError(('Invalid optimizer type: ' + opt.optim))
    if (opt.model_dtype == 'fp16'):
        import apex
        if (opt.optim != 'fusedadam'):
            loss_scale = ('dynamic' if (opt.loss_scale == 0) else opt.loss_scale)
            (model, optimizer) = apex.amp.initialize([model, model.generator], optimizer, opt_level=opt.apex_opt_level, loss_scale=loss_scale, keep_batchnorm_fp32=None)
        else:
            static_loss_scale = opt.loss_scale
            dynamic_loss_scale = (opt.loss_scale == 0)
            optimizer = apex.optimizers.FP16_Optimizer(optimizer, static_loss_scale=static_loss_scale, dynamic_loss_scale=dynamic_loss_scale)
    return optimizer

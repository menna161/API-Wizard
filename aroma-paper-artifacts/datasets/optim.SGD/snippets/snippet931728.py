import torch


def get_optimizer(parameters, cfg):
    if (cfg.method == 'sgd'):
        optimizer = torch.optim.SGD(filter((lambda p: p.requires_grad), parameters), lr=cfg.lr, momentum=0.9, weight_decay=cfg.weight_decay)
    elif (cfg.method == 'adam'):
        optimizer = torch.optim.Adam(filter((lambda p: p.requires_grad), parameters), lr=cfg.lr, weight_decay=cfg.weight_decay)
    elif (cfg.method == 'rmsprop'):
        optimizer = torch.optim.RMSprop(filter((lambda p: p.requires_grad), parameters), lr=cfg.lr, weight_decay=cfg.weight_decay)
    elif (cfg.method == 'adadelta'):
        optimizer = torch.optim.Adadelta(filter((lambda p: p.requires_grad), parameters), lr=cfg.lr, weight_decay=cfg.weight_decay)
    else:
        raise NotImplementedError
    return optimizer

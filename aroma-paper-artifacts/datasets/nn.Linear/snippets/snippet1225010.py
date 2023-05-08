import torch
import torch.nn as nn


def group_weight(weight_group, module, norm_layer, lr):
    group_decay = []
    group_no_decay = []
    for m in module.modules():
        if isinstance(m, nn.Linear):
            group_decay.append(m.weight)
            if (m.bias is not None):
                group_no_decay.append(m.bias)
        elif isinstance(m, (nn.Conv1d, nn.Conv2d, nn.Conv3d, nn.ConvTranspose2d, nn.ConvTranspose3d)):
            group_decay.append(m.weight)
            if (m.bias is not None):
                group_no_decay.append(m.bias)
        elif (isinstance(m, norm_layer) or isinstance(m, nn.BatchNorm1d) or isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm3d) or isinstance(m, nn.GroupNorm)):
            if (m.weight is not None):
                group_no_decay.append(m.weight)
            if (m.bias is not None):
                group_no_decay.append(m.bias)
        elif isinstance(m, nn.Parameter):
            group_decay.append(m)
    assert (len(list(module.parameters())) == (len(group_decay) + len(group_no_decay)))
    weight_group.append(dict(params=group_decay, lr=lr))
    weight_group.append(dict(params=group_no_decay, weight_decay=0.0, lr=lr))
    return weight_group

from logger import coil_logger
import torch.nn as nn
import torch.nn.init as init
import torch
import torch.nn.functional as F


def __init__(self, params=None, module_name='Default'):
    super(Conv, self).__init__()
    if (params is None):
        raise ValueError('Creating a NULL fully connected block')
    if ('channels' not in params):
        raise ValueError(' Missing the channel sizes parameter ')
    if ('kernels' not in params):
        raise ValueError(' Missing the kernel sizes parameter ')
    if ('strides' not in params):
        raise ValueError(' Missing the strides parameter ')
    if ('dropouts' not in params):
        raise ValueError(' Missing the dropouts parameter ')
    if ('end_layer' not in params):
        raise ValueError(' Missing the end module parameter ')
    if (len(params['dropouts']) != (len(params['channels']) - 1)):
        raise ValueError('Dropouts should be from the len of channel_sizes minus 1')
    '" ------------------ IMAGE MODULE ---------------- '
    self.layers = []
    for i in range(0, (len(params['channels']) - 1)):
        conv = nn.Conv2d(in_channels=params['channels'][i], out_channels=params['channels'][(i + 1)], kernel_size=params['kernels'][i], stride=params['strides'][i])
        dropout = nn.Dropout2d(p=params['dropouts'][i])
        relu = nn.ReLU(inplace=True)
        bn = nn.BatchNorm2d(params['channels'][(i + 1)])
        layer = nn.Sequential(*[conv, bn, dropout, relu])
        self.layers.append(layer)
    self.layers = nn.Sequential(*self.layers)
    self.module_name = module_name

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import numpy as np
import pickle
from tqdm import tqdm
import time


def __init__(self, input_size=[3, 32, 32], output_size=10, **kw):
    "\n        *** Create Pytorch net ***\n        input_size: Iterable. Size of 1 input. Example: [3,32,32] for CIFAR, [784] for MNIST\n        output_size: Integer. #labels. Example: 100 for CIFAR-100, 39 for TIMIT phonemes\n        kw:\n            act: String. Activation for all layers. Must be pre-defined in F_activations and nn_activations. Default 'relu'\n            --- CONV ---:\n                    out_channels: Iterable. #filters in each conv layer, i.e. #conv layers. If no conv layer is needed, enter []          \n                --- For the next kws, either pass an iterable of size = size of out_channels, OR leave blank to get default values ---\n                        kernel_sizes: Default all 3\n                        strides: Default all 1\n                        paddings: Default values keep output size same as input for that kernel_size. Example 2 for kernel_size=5, 1 for kernel_size=3\n                        dilations: Default all 1\n                        groups: Default all 1\n                        apply_bns: 1 to get BN layer after the current conv layer, else 0. Default all 1\n                        apply_maxpools: 1 to get maxpool layer after the current conv layer, else 0. Default all 0\n                        apply_dropouts: 1 to get dropout layer after the current conv layer, else 0. Default all 1\n                        shortcuts: 1 to start shortcut after current conv layer, else 0. All shortcuts rejoin after 2 layers. Default all 0\n                            2 consecutive elements of shortcuts cannot be 1, last 2 elements of shortcuts must be 0s\n                            The shortcut portion has added 0s to compensate for channel increase, and avg pools to compensate for dwensampling\n                    dropout_probs: Iterable of size = #1s in apply_dropouts. DROP probabilities for each dropout layer. Default first layer 0.1, all other 0.3\n                        Eg: If apply_dropouts = [1,0,1,0], then dropout_probs = [0.1,0.3]. If apply_dropouts = [0,1,1,1], then dropout_probs = [0.3,0.3,0.3]\n                    apply_gap: 1 to apply global average pooling just before MLPs, else 0. Default 1\n            --- MLP ---:\n                    hidden_mlp: Iterable. #nodes in the hidden layers only.\n                    apply_dropouts_mlp: Whether to apply dropout after current hidden layer. Iterable of size = number of hidden layers. Default all 0\n                    dropout_probs_mlp: As in dropout_probs for conv. Default all 0.5\n                    \n                    Examples:\n                        If input_size=800, output_size=10, and hidden_mlp is not given, or is [], then the config will be [800,10]. By default, apply_dropouts_mlp = [], dropout_probs_mlp = []\n                        If input_size=800, output_size=10, and hidden_mlp is [100,100], then the config will be [800,100,100,10]. apply_dropouts_mlp for example can be [1,0], then dropout_probs_mlp = [0.5] by default\n        "
    super().__init__()
    self.act = (kw['act'] if ('act' in kw) else net_kws_defaults['act'])
    self.out_channels = (kw['out_channels'] if ('out_channels' in kw) else net_kws_defaults['out_channels'])
    self.num_layers_conv = len(self.out_channels)
    self.kernel_sizes = (kw['kernel_sizes'] if ('kernel_sizes' in kw) else (self.num_layers_conv * net_kws_defaults['kernel_sizes']))
    self.strides = (kw['strides'] if ('strides' in kw) else (self.num_layers_conv * net_kws_defaults['strides']))
    self.paddings = (kw['paddings'] if ('paddings' in kw) else [((ks - 1) // 2) for ks in self.kernel_sizes])
    self.dilations = (kw['dilations'] if ('dilations' in kw) else (self.num_layers_conv * net_kws_defaults['dilations']))
    self.groups = (kw['groups'] if ('groups' in kw) else (self.num_layers_conv * net_kws_defaults['groups']))
    self.apply_bns = (kw['apply_bns'] if ('apply_bns' in kw) else (self.num_layers_conv * net_kws_defaults['apply_bns']))
    self.apply_maxpools = (kw['apply_maxpools'] if ('apply_maxpools' in kw) else (self.num_layers_conv * net_kws_defaults['apply_maxpools']))
    self.apply_gap = (kw['apply_gap'] if ('apply_gap' in kw) else net_kws_defaults['apply_gap'])
    self.apply_dropouts = (kw['apply_dropouts'] if ('apply_dropouts' in kw) else (self.num_layers_conv * net_kws_defaults['apply_dropouts']))
    if ('dropout_probs' in kw):
        self.dropout_probs = kw['dropout_probs']
    else:
        self.dropout_probs = (np.count_nonzero(self.apply_dropouts) * [net_kws_defaults['dropout_probs'][1]])
        if ((len(self.apply_dropouts) != 0) and (self.apply_dropouts[0] == 1)):
            self.dropout_probs[0] = net_kws_defaults['dropout_probs'][0]
    self.shortcuts = (kw['shortcuts'] if ('shortcuts' in kw) else (self.num_layers_conv * net_kws_defaults['shortcuts']))
    dropout_index = 0
    self.conv = nn.ModuleDict({})
    for i in range(self.num_layers_conv):
        self.conv['conv-{0}'.format(i)] = nn.Conv2d(in_channels=(input_size[0] if (i == 0) else self.out_channels[(i - 1)]), out_channels=self.out_channels[i], kernel_size=self.kernel_sizes[i], stride=self.strides[i], padding=self.paddings[i], dilation=self.dilations[i], groups=self.groups[i])
        if (self.apply_maxpools[i] == 1):
            self.conv['mp-{0}'.format(i)] = nn.MaxPool2d(kernel_size=2, ceil_mode=True)
        if (self.apply_bns[i] == 1):
            self.conv['bn-{0}'.format(i)] = nn.BatchNorm2d(self.out_channels[i])
        self.conv['act-{0}'.format(i)] = nn_activations[self.act]()
        if (self.apply_dropouts[i] == 1):
            self.conv['drop-{0}'.format(i)] = nn.Dropout(self.dropout_probs[dropout_index])
            dropout_index += 1
    if ((self.apply_gap == 1) and (self.num_layers_conv > 0)):
        self.conv['gap'] = nn.AdaptiveAvgPool2d(output_size=1)
    self.mlp_input_size = self.get_mlp_input_size(input_size, self.conv)
    self.n_mlp = [self.mlp_input_size, output_size]
    if ('hidden_mlp' in kw):
        self.n_mlp[1:1] = kw['hidden_mlp']
    self.num_hidden_layers_mlp = len(self.n_mlp[1:(- 1)])
    self.apply_dropouts_mlp = (kw['apply_dropouts_mlp'] if ('apply_dropouts_mlp' in kw) else (self.num_hidden_layers_mlp * net_kws_defaults['apply_dropouts_mlp']))
    self.dropout_probs_mlp = (kw['dropout_probs_mlp'] if ('dropout_probs_mlp' in kw) else (np.count_nonzero(self.apply_dropouts_mlp) * net_kws_defaults['dropout_probs_mlp']))
    self.mlp = nn.ModuleList([])
    for i in range((len(self.n_mlp) - 1)):
        self.mlp.append(nn.Linear(self.n_mlp[i], self.n_mlp[(i + 1)]))

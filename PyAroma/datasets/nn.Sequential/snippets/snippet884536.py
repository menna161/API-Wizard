from __future__ import division
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from utils.parse_config import *
from utils.utils import build_targets, to_cpu, non_max_suppression
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import datetime
from torch2trt import torch2trt


def create_modules(module_defs, TensorRT):
    '\n    Constructs module list of layer blocks from module configuration in module_defs\n    '
    hyperparams = module_defs.pop(0)
    output_filters = [int(hyperparams['channels'])]
    module_list = nn.ModuleList()
    for (module_i, module_def) in enumerate(module_defs):
        modules = nn.Sequential()
        if (module_def['type'] == 'convolutional'):
            bn = int(module_def['batch_normalize'])
            filters = int(module_def['filters'])
            kernel_size = int(module_def['size'])
            pad = ((kernel_size - 1) // 2)
            modules.add_module(f'conv_{module_i}', nn.Conv2d(in_channels=output_filters[(- 1)], out_channels=filters, kernel_size=kernel_size, stride=int(module_def['stride']), padding=pad, bias=(not bn)))
            if bn:
                modules.add_module(f'batch_norm_{module_i}', nn.BatchNorm2d(filters, momentum=0.9, eps=1e-05))
            if (module_def['activation'] == 'leaky'):
                modules.add_module(f'leaky_{module_i}', nn.LeakyReLU(0.1))
        elif (module_def['type'] == 'maxpool'):
            kernel_size = int(module_def['size'])
            stride = int(module_def['stride'])
            if ((kernel_size == 2) and (stride == 1)):
                modules.add_module(f'_debug_padding_{module_i}', nn.ZeroPad2d((0, 1, 0, 1)))
            maxpool = nn.MaxPool2d(kernel_size=kernel_size, stride=stride, padding=int(((kernel_size - 1) // 2)))
            modules.add_module(f'maxpool_{module_i}', maxpool)
        elif (module_def['type'] == 'upsample'):
            upsample = Upsample(scale_factor=int(module_def['stride']), mode='nearest')
            modules.add_module(f'upsample_{module_i}', upsample)
        elif (module_def['type'] == 'route'):
            layers = [int(x) for x in module_def['layers'].split(',')]
            filters = sum([output_filters[1:][i] for i in layers])
            modules.add_module(f'route_{module_i}', EmptyLayer())
        elif (module_def['type'] == 'shortcut'):
            filters = output_filters[1:][int(module_def['from'])]
            modules.add_module(f'shortcut_{module_i}', EmptyLayer())
        elif (module_def['type'] == 'yolo'):
            if TensorRT:
                pass
            else:
                anchor_idxs = [int(x) for x in module_def['mask'].split(',')]
                anchors = [int(x) for x in module_def['anchors'].split(',')]
                anchors = [(anchors[i], anchors[(i + 1)]) for i in range(0, len(anchors), 2)]
                anchors = [anchors[i] for i in anchor_idxs]
                num_classes = int(module_def['classes'])
                img_size = int(hyperparams['height'])
                yolo_layer = YOLOLayer(anchors, num_classes, img_size)
                modules.add_module(f'yolo_{module_i}', yolo_layer)
        module_list.append(modules)
        output_filters.append(filters)
    return (hyperparams, module_list)

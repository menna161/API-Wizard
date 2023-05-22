import torch
import torch.nn as nn
import torchvision
import sys
import numpy as np
from PIL import Image
import PIL
import numpy as np
import matplotlib.pyplot as plt


def get_noise(input_depth, method, spatial_size, noise_type='u', var=(1.0 / 10)):
    "Returns a pytorch.Tensor of size (1 x `input_depth` x `spatial_size[0]` x `spatial_size[1]`) \n    initialized in a specific way.\n    Args:\n        input_depth: number of channels in the tensor\n        method: `noise` for fillting tensor with noise; `meshgrid` for np.meshgrid\n        spatial_size: spatial size of the tensor to initialize\n        noise_type: 'u' for uniform; 'n' for normal\n        var: a factor, a noise will be multiplicated by. Basically it is standard deviation scaler. \n    "
    if isinstance(spatial_size, int):
        spatial_size = (spatial_size, spatial_size)
    if (method == 'noise'):
        shape = [1, input_depth, spatial_size[0], spatial_size[1]]
        net_input = torch.zeros(shape)
        fill_noise(net_input, noise_type)
        net_input *= var
    elif (method == 'meshgrid'):
        assert (input_depth == 2)
        (X, Y) = np.meshgrid((np.arange(0, spatial_size[1]) / float((spatial_size[1] - 1))), (np.arange(0, spatial_size[0]) / float((spatial_size[0] - 1))))
        meshgrid = np.concatenate([X[(None, :)], Y[(None, :)]])
        net_input = np_to_torch(meshgrid)
    else:
        assert False
    return net_input

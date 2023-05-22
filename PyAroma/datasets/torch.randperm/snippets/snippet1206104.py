import torch
import numpy as np
import torchvision.transforms as trans
import math
from scipy.fftpack import dct, idct


def block_order(image_size, channels, initial_size=1, stride=1):
    order = torch.zeros(channels, image_size, image_size)
    total_elems = ((channels * initial_size) * initial_size)
    perm = torch.randperm(total_elems)
    order[(:, :initial_size, :initial_size)] = perm.view(channels, initial_size, initial_size)
    for i in range(initial_size, image_size, stride):
        num_elems = (channels * (((2 * stride) * i) + (stride * stride)))
        perm = (torch.randperm(num_elems) + total_elems)
        num_first = ((channels * stride) * (stride + i))
        order[(:, :(i + stride), i:(i + stride))] = perm[:num_first].view(channels, (- 1), stride)
        order[(:, i:(i + stride), :i)] = perm[num_first:].view(channels, stride, (- 1))
        total_elems += num_elems
    return order.view(1, (- 1)).squeeze().long().sort()[1]

import math
import numpy as np
import torch
from skimage.color import rgb2lab
from skimage.segmentation._slic import _enforce_label_connectivity_cython
from lib.ssn.ssn import sparse_ssn_iter
import time
import argparse
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries
from model import SSNModel


@torch.no_grad()
def inference(image, nspix, n_iter, fdim=None, color_scale=0.26, pos_scale=2.5, weight=None, enforce_connectivity=True):
    '\n    generate superpixels\n\n    Args:\n        image: numpy.ndarray\n            An array of shape (h, w, c)\n        nspix: int\n            number of superpixels\n        n_iter: int\n            number of iterations\n        fdim (optional): int\n            feature dimension for supervised setting\n        color_scale: float\n            color channel factor\n        pos_scale: float\n            pixel coordinate factor\n        weight: state_dict\n            pretrained weight\n        enforce_connectivity: bool\n            if True, enforce superpixel connectivity in postprocessing\n\n    Return:\n        labels: numpy.ndarray\n            An array of shape (h, w)\n    '
    if (weight is not None):
        from model import SSNModel
        model = SSNModel(fdim, nspix, n_iter).to('cuda')
        model.load_state_dict(torch.load(weight))
        model.eval()
    else:
        model = (lambda data: sparse_ssn_iter(data, nspix, n_iter))
    (height, width) = image.shape[:2]
    nspix_per_axis = int(math.sqrt(nspix))
    pos_scale = (pos_scale * max((nspix_per_axis / height), (nspix_per_axis / width)))
    coords = torch.stack(torch.meshgrid(torch.arange(height, device='cuda'), torch.arange(width, device='cuda')), 0)
    coords = coords[None].float()
    image = rgb2lab(image)
    image = torch.from_numpy(image).permute(2, 0, 1)[None].to('cuda').float()
    inputs = torch.cat([(color_scale * image), (pos_scale * coords)], 1)
    (_, H, _) = model(inputs)
    labels = H.reshape(height, width).to('cpu').detach().numpy()
    if enforce_connectivity:
        segment_size = ((height * width) / nspix)
        min_size = int((0.06 * segment_size))
        max_size = int((3.0 * segment_size))
        labels = _enforce_label_connectivity_cython(labels[None], min_size, max_size)[0]
    return labels

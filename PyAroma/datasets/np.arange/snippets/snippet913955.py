import os
import argparse
import numpy as np
from functools import partial
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from chainer.datasets import get_mnist
from chainer_bcnn.functions import mc_dropout
from chainer_bcnn.links import Classifier
from chainer_bcnn.links import MCSampler
from chainer_bcnn.inference import Inferencer
from chainer_bcnn.utils import fixed_seed


def __init__(self, phase, indices=None, withlabel=True, ndim=3, scale=1.0, dtype=np.float32, label_dtype=np.int32, rgb_format=False):
    super(Dataset, self).__init__()
    (train, test) = get_mnist(withlabel, ndim, scale, dtype, label_dtype, rgb_format)
    if (phase == 'train'):
        dataset = train
    elif (phase == 'test'):
        dataset = test
    else:
        raise KeyError('`phase` should be `train` or `test`..')
    if (indices is not None):
        if isinstance(indices, list):
            indices = np.asarray(indices)
    else:
        indices = np.arange(len(dataset))
    assert (len(indices) <= len(dataset))
    dataset = dataset[indices]
    if withlabel:
        (images, labels) = dataset
    else:
        (images, labels) = (dataset, None)
    self._phase = phase
    self._indices = indices
    self._ndim = ndim
    self._scale = scale
    self._dtype = dtype
    self._label_dtype = label_dtype
    self._rgb_format = rgb_format
    self._images = images
    self._labels = labels

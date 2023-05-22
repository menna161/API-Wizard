import os
import sys
import collections
from copy import deepcopy
from PIL import Image
import numpy as np
import torch
import torch.utils.data as data
from torchvision import transforms
from torchvision.datasets.folder import default_loader
from sklearn.preprocessing import MultiLabelBinarizer


def __call__(self, sample):
    '\n        Parameters\n        ----------\n        sample : target label\n\n        Returns\n        -------\n        target label in multilabel format\n        '
    if isinstance(sample, int):
        return self._transformer.fit_transform([[sample]])[0]
    else:
        return self._transformer.fit_transform([sample])[0]

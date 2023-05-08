import random
import math
import numpy as np
import cv2
import collections
import numbers
from PIL import Image
import torch
import torchvision.transforms as TS


def __call__(self, image, label):
    if ((not isinstance(image, np.ndarray)) or (not isinstance(label, np.ndarray))):
        raise RuntimeError('segtransform.ToTensor() only handle np.ndarray[eg: data readed by cv2.imread()].\n')
    if ((len(image.shape) > 3) or (len(image.shape) < 2)):
        raise RuntimeError('segtransform.ToTensor() only handle np.ndarray with 3 dims or 2 dims.\n')
    if (len(image.shape) == 2):
        image = np.expand_dims(image, axis=2)
    image = torch.from_numpy(image.transpose((2, 0, 1)))
    if (not isinstance(image, torch.FloatTensor)):
        image = image.float()
    label = torch.from_numpy(label)
    if (not isinstance(label, torch.LongTensor)):
        label = label.long()
    return (image, label)

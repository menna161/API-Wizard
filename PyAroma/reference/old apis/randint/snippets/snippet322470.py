from __future__ import print_function, division
import os
import torch
from torch.autograd import Variable
from torch.utils.data import Dataset
from skimage import io
import pandas as pd
import numpy as np
from lib.transformation import AffineTnf


def get_image(self, img_name_list, idx, flip):
    img_name = os.path.join(self.dataset_image_path, img_name_list.iloc[idx])
    image = io.imread(img_name)
    if (image.ndim == 2):
        image = np.repeat(np.expand_dims(image, 2), axis=2, repeats=3)
    if self.random_crop:
        (h, w, c) = image.shape
        top = np.random.randint((h / 4))
        bottom = int((((3 * h) / 4) + np.random.randint((h / 4))))
        left = np.random.randint((w / 4))
        right = int((((3 * w) / 4) + np.random.randint((w / 4))))
        image = image[top:bottom, left:right, :]
    if flip:
        image = np.flip(image, 1)
    im_size = np.asarray(image.shape)
    image = np.expand_dims(image.transpose((2, 0, 1)), 0)
    image = torch.Tensor(image.astype(np.float32))
    image_var = Variable(image, requires_grad=False)
    image = self.affineTnf(image_var).data.squeeze(0)
    im_size = torch.Tensor(im_size.astype(np.float32))
    return (image, im_size)

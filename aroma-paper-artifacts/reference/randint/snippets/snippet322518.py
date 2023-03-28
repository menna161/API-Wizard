from __future__ import print_function, division
import os
import torch
from torch.autograd import Variable
from torch.utils.data import Dataset
from skimage import io
import pandas as pd
import numpy as np
from . import transformation as tf
import scipy.io
import matplotlib
import matplotlib.pyplot as plt


def get_image(self, img_name_list, idx, flip, category_name=None):
    img_name = os.path.join(self.dataset_image_path, img_name_list.iloc[idx])
    image = io.imread(img_name)
    if (image.ndim == 2):
        image = np.repeat(np.expand_dims(image, 2), axis=2, repeats=3)
    if self.keypoints_on:
        (keypoints, bbox) = self.get_annotations(img_name_list.iloc[idx], category_name)
    if self.random_crop:
        (h, w, c) = image.shape
        top = np.random.randint((h / 4))
        bottom = int((((3 * h) / 4) + np.random.randint((h / 4))))
        left = np.random.randint((w / 4))
        right = int((((3 * w) / 4) + np.random.randint((w / 4))))
        image = image[top:bottom, left:right, :]
    im_size = np.asarray(image.shape)
    if flip:
        image = np.flip(image, 1)
        if self.keypoints_on:
            (N, _) = keypoints.shape
            for n in range(N):
                if (keypoints[(n, 2)] > 0):
                    keypoints[(n, 0)] = (im_size[1] - keypoints[(n, 0)])
            bbox[0] = (im_size[1] - bbox[0])
            bbox[2] = (im_size[1] - bbox[2])
            tmp = bbox[0]
            bbox[0] = bbox[2]
            bbox[2] = tmp
    image = np.expand_dims(image.transpose((2, 0, 1)), 0)
    image = torch.Tensor(image.astype(np.float32))
    image_var = Variable(image, requires_grad=False)
    image = self.affineTnf(image_var).data.squeeze(0)
    im_size = torch.Tensor(im_size.astype(np.float32))
    if self.keypoints_on:
        keypoints[:, 0] = ((keypoints[:, 0] / float(im_size[1])) * float(self.out_w))
        keypoints[:, 1] = ((keypoints[:, 1] / float(im_size[0])) * float(self.out_h))
        bbox[0] = ((bbox[0] / float(im_size[1])) * float(self.out_w))
        bbox[1] = ((bbox[1] / float(im_size[0])) * float(self.out_h))
        bbox[2] = ((bbox[2] / float(im_size[1])) * float(self.out_w))
        bbox[3] = ((bbox[3] / float(im_size[0])) * float(self.out_h))
        return (image, im_size, keypoints, bbox)
    else:
        return (image, im_size)

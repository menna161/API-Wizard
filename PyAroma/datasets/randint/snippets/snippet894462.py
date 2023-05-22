from __future__ import print_function, division
import os
import torch
from torch.autograd import Variable
from torch.utils.data import Dataset
from skimage import io
import pandas as pd
import numpy as np
from lib.transformation import AffineTnf
import torchvision
import PIL
from PIL import Image


def __getitem__(self, idx):
    try:
        (image_A, im_size_A) = self.get_image(self.img_A_names, idx, self.flip[idx])
        (image_B, im_size_B) = self.get_image(self.img_B_names, idx, self.flip[idx], affine=(self.random_affine is not None))
    except:
        return self.__getitem__(np.random.randint(self.__len__()))
    image_set = self.set[idx]
    sample = {'source_image': image_A, 'target_image': image_B, 'source_im_size': im_size_A, 'target_im_size': im_size_B, 'set': image_set}
    if self.transform:
        sample = self.transform(sample)
    return sample

from __future__ import print_function
import os
import numpy as np
import torch
import torch.optim
from skimage.measure import compare_psnr
from torchvision.utils import save_image
import h5py
import cv2
from torchvision import transforms
from PIL import Image
import pandas as pd
import scipy
from google.colab import drive
from HHReLU import HHReLU
from models import *
from utils.denoising_utils import *
from HHReLU import HHReLU
from models import *
from utils.dip_utils import *


def load_image(file):
    orig_img = cv2.imread(file)
    assert (orig_img.shape == (368, 300, 3))
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    assert (orig_img.shape == (368, 300, 3))
    img = cv2.resize(orig_img, (512, 512))
    assert (img.shape == (512, 512, 3))
    img = np.transpose(img, (2, 0, 1))
    assert (img.shape == (3, 512, 512))
    img = (np.array([img]) / 255.0)
    assert (img.shape == (1, 3, 512, 512))
    return img

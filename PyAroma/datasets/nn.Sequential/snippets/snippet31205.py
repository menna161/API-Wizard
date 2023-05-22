from __future__ import print_function
import torch
import numpy as np
from PIL import Image
import random
import inspect, re
import numpy as np
import os
import collections
import math
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from skimage.transform import resize


def __init__(self):
    super(VGG16FeatureExtractor, self).__init__()
    vgg16 = models.vgg16(pretrained=True)
    self.enc_1 = nn.Sequential(*vgg16.features[:5])
    self.enc_2 = nn.Sequential(*vgg16.features[5:10])
    self.enc_3 = nn.Sequential(*vgg16.features[10:17])
    for i in range(3):
        for param in getattr(self, 'enc_{:d}'.format((i + 1))).parameters():
            param.requires_grad = False

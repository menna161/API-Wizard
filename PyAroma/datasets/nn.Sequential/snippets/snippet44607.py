import sys
import argparse
import torch
import torch.nn.init
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.backends.cudnn as cudnn
import time
import os
import sys
import cv2
import math
import numpy as np
from tqdm import tqdm
from copy import deepcopy
import random
import time
import numpy as np
import glob
import os


def __init__(self):
    super(HardNet, self).__init__()
    self.features = nn.Sequential(nn.Conv2d(1, 32, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(32, affine=False), nn.ReLU(), nn.Conv2d(32, 32, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(32, affine=False), nn.ReLU(), nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1, bias=False), nn.BatchNorm2d(64, affine=False), nn.ReLU(), nn.Conv2d(64, 64, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(64, affine=False), nn.ReLU(), nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False), nn.BatchNorm2d(128, affine=False), nn.ReLU(), nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False), nn.BatchNorm2d(128, affine=False), nn.ReLU(), nn.Dropout(0.1), nn.Conv2d(128, 128, kernel_size=8, bias=False), nn.BatchNorm2d(128, affine=False))

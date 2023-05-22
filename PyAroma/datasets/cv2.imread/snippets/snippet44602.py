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


def __init__(self, base):
    name = base.split('/')
    self.name = name[(- 1)]
    self.base = base
    for t in self.itr:
        im_path = os.path.join(base, (t + '.png'))
        im = cv2.imread(im_path, 0)
        self.N = (im.shape[0] / 65)
        setattr(self, t, np.split(im, self.N))

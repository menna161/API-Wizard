from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
from miscc.config import cfg
import torch
import torch.utils.data as data
from torch.autograd import Variable
import torchvision.transforms as transforms
import os
import sys
import numpy as np
from PIL import Image
import numpy.random as random
from miscc.utils import *
import cPickle as pickle
import pickle


def load_class_id(self, data_dir, total_num):
    if os.path.isfile((data_dir + '/class_info.pickle')):
        with open((data_dir + '/class_info.pickle'), 'rb') as f:
            class_id = pickle.load(f)
    else:
        class_id = np.arange(total_num)
    return class_id

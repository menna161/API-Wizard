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


def get_caption(self, sent_ix):
    sent_caption = np.asarray(self.captions[sent_ix]).astype('int64')
    if ((sent_caption == 0).sum() > 0):
        print('ERROR: do not need END (0) token', sent_caption)
    num_words = len(sent_caption)
    x = np.zeros((cfg.TEXT.WORDS_NUM, 1), dtype='int64')
    x_len = num_words
    if (num_words <= cfg.TEXT.WORDS_NUM):
        x[(:num_words, 0)] = sent_caption
    else:
        ix = list(np.arange(num_words))
        np.random.shuffle(ix)
        ix = ix[:cfg.TEXT.WORDS_NUM]
        ix = np.sort(ix)
        x[(:, 0)] = sent_caption[ix]
        x_len = cfg.TEXT.WORDS_NUM
    return (x, x_len)

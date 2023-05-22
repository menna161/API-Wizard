import numpy as np
from tqdm import tqdm
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from flair.data import Sentence
from flair.models import SequenceTagger
import sys
import os
import pickle
from collections import OrderedDict
import json
from lm import LanguageModel as Model
import utils


def sample(corpus, N):
    shuffle_indices = np.random.permutation(np.arange(len(corpus)))
    return np.array(corpus)[shuffle_indices][:N]

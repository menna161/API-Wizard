from os.path import join, dirname, abspath
import sys
import copy
import random
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from gensim.models import KeyedVectors
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from evidence_inference.models.utils import PaddedSequence
from evidence_inference.models.attention_distributions import TokenAttention, evaluate_model_attention_distribution
import pdb
import pdb
import pdb


def to_int_preds(y):
    return [int(np.argmax(y_i)) for y_i in y.cpu()]

import torch
from torch.autograd import Variable
import numpy as np
import os
import argparse
import random
import copy
from tqdm import tqdm
import pickle
from scorer.data_helper.json_reader import read_sorted_scores, read_articles, read_processed_scores, read_scores
from scipy.stats import spearmanr, pearsonr, kendalltau
import math
from resources import MODEL_WEIGHT_DIR


def build_model(model_type, vec_length, learn_rate=None):
    if ('linear' in model_type):
        deep_model = torch.nn.Sequential(torch.nn.Linear(vec_length, 1))
    else:
        deep_model = torch.nn.Sequential(torch.nn.Linear(vec_length, int((vec_length / 2))), torch.nn.ReLU(), torch.nn.Linear(int((vec_length / 2)), 1))
    if (learn_rate is not None):
        optimiser = torch.optim.Adam(deep_model.parameters(), lr=learn_rate)
        return (deep_model, optimiser)
    else:
        return deep_model

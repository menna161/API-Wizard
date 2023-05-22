import torch
import torch.nn as nn
from torch.utils.data.dataset import Dataset
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from itertools import combinations
from numpy.linalg import norm
from PIL import Image


def LinearBlock(self, in_features, out_features, dropout_p=0.15):
    block = [nn.Linear(in_features, out_features), nn.BatchNorm1d(out_features), nn.LeakyReLU(0.1), nn.Dropout(dropout_p)]
    return block

import torch
import torch.nn as nn
from torch.utils.data.dataset import Dataset
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from itertools import combinations
from numpy.linalg import norm
from PIL import Image


def __init__(self, num_classes=3, image_weight=0.5, text_weight=0.5):
    super(Towers, self).__init__()
    img_layers = (self.LinearBlock(64, 512) + sum([self.LinearBlock(512, 512) for i in range(4)], []))
    text_layers = (self.LinearBlock(3072, 512) + self.LinearBlock(512, 512))
    self.downsize = nn.Sequential(*self.LinearBlock(2048, 64, 0.0))
    self.img_features = nn.Sequential(*img_layers)
    self.text_features = nn.Sequential(*text_layers)
    self.shared = nn.Linear(512, num_classes)
    self.batchnorm = nn.BatchNorm1d(512)
    self.image_weight = image_weight
    self.text_weight = text_weight

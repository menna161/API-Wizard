import os
import random
import logging
from collections import Counter
import torch


def initialize_centroids(self):
    '\n        Initializes the centroids by sampling random columns from W.\n        '
    (in_features, out_features) = self.W.size()
    indices = torch.randint(low=0, high=out_features, size=(self.n_centroids,)).long()
    self.centroids = self.W[(:, indices)].t()

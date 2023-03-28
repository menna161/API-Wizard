from __future__ import print_function
import torch.utils.data as data
import os
import sys
import numpy as np
from tqdm import tqdm
import torch
import struct


@staticmethod
def generate_triplets(indices, num_triplets, n_classes):
    triplets = []
    for x in tqdm(range(num_triplets)):
        c1 = np.random.randint(0, (n_classes - 1))
        c2 = np.random.randint(0, (n_classes - 1))
        while (len(indices[c1]) < 2):
            c1 = np.random.randint(0, (n_classes - 1))
        while (c1 == c2):
            c2 = np.random.randint(0, (n_classes - 1))
        if (len(indices[c1]) == 2):
            (n1, n2) = (0, 1)
        else:
            n1 = np.random.randint(0, (len(indices[c1]) - 1))
            n2 = np.random.randint(0, (len(indices[c1]) - 1))
            while (n1 == n2):
                n2 = np.random.randint(0, (len(indices[c1]) - 1))
        if (len(indices[c2]) == 1):
            n3 = 0
        else:
            n3 = np.random.randint(0, (len(indices[c2]) - 1))
        triplets.append([indices[c1][n1], indices[c1][n2], indices[c2][n3], c1, c2])
    return triplets

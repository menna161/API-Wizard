import os, sys
import torch
from torchvision import datasets, transforms
import numpy as np
import torchvision
import matplotlib.pyplot as plt
import argparse
import numpy as np
from functools import reduce
from operator import __or__
from torch.utils.data.sampler import SubsetRandomSampler


def get_sampler(labels, n=None, n_valid=None):
    (indices,) = np.where(reduce(__or__, [(labels == i) for i in np.arange(n_labels)]))
    np.random.shuffle(indices)
    indices_valid = np.hstack([list(filter((lambda idx: (labels[idx] == i)), indices))[:n_valid] for i in range(n_labels)])
    indices_train = np.hstack([list(filter((lambda idx: (labels[idx] == i)), indices))[n_valid:(n_valid + n)] for i in range(n_labels)])
    indices_unlabelled = np.hstack([list(filter((lambda idx: (labels[idx] == i)), indices))[:] for i in range(n_labels)])
    indices_train = torch.from_numpy(indices_train)
    indices_valid = torch.from_numpy(indices_valid)
    indices_unlabelled = torch.from_numpy(indices_unlabelled)
    sampler_train = SubsetRandomSampler(indices_train)
    sampler_valid = SubsetRandomSampler(indices_valid)
    sampler_unlabelled = SubsetRandomSampler(indices_unlabelled)
    return (sampler_train, sampler_valid, sampler_unlabelled)

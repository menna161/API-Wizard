import os
import numpy as np
import torch
import torchvision as tv
from PIL import Image
from torch.utils.data.sampler import SubsetRandomSampler
from torch.utils.data import Dataset
from torchvision import datasets


def one_hot_encoding(label):
    print('one_hot_encoding process')
    cls = set(label)
    class_dict = {c: np.identity(len(cls))[(i, :)] for (i, c) in enumerate(cls)}
    one_hot = np.array(list(map(class_dict.get, label)))
    return one_hot

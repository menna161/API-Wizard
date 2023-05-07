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


def imshow(img, title):
    img = ((img / 2) + 0.5)
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.title(title)
    plt.show()

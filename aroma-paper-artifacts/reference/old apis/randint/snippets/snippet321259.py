import glob
import random
import os
import numpy as np
import torch
from scipy import io
from collections import Counter
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms
from torchvision import datasets
from skimage.transform import rescale


def sample_latent(self, size=1):
    samples = np.zeros((size, self.latents_sizes.size))
    for (lat_i, lat_size) in enumerate(self.latents_sizes):
        samples[:, lat_i] = self.rnd_state.randint(lat_size, size=size)
    return samples

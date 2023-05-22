import json
import logging
import numpy as np
import random
import torch.utils.data.dataset
import utils.data_transforms
from enum import Enum, unique
from tqdm import tqdm
from utils.io import IO


def __getitem__(self, idx):
    sample = self.file_list[idx]
    data = {}
    rand_idx = (- 1)
    if ('n_renderings' in self.options):
        rand_idx = (random.randint(0, (self.options['n_renderings'] - 1)) if self.options['shuffle'] else 0)
    for ri in self.options['required_items']:
        file_path = sample[('%s_path' % ri)]
        if (type(file_path) == list):
            file_path = file_path[rand_idx]
        data[ri] = IO.get(file_path).astype(np.float32)
    if (self.transforms is not None):
        data = self.transforms(data)
    return (sample['taxonomy_id'], sample['model_id'], data)

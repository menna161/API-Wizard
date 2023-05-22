from torch.utils.data import Dataset
import torch
import os
import numpy as np
from utils.dsp import *
import re
import config
import pandas as pd
import pickle
from torch.utils.data import DataLoader


def __getitem__(self, index):
    (speaker_id, name) = self.all_files[index]
    speaker_onehot = (np.arange(len(self.index)) == speaker_id).astype(np.long)
    audio = np.load(f'{self.path}/{speaker_id}/{name}.npy')
    return (speaker_onehot, audio)

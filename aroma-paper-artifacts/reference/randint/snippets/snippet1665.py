import os
from scipy.io.wavfile import read
import scipy.io.wavfile as wav
import subprocess as sp
import numpy as np
import argparse
import random
import os
import sys
from random import shuffle
import speechpy
import datetime
import soundfile as sf


def __call__(self, sample):
    (feature, label) = (sample['feature'], sample['label'])
    feature_cube = np.zeros((self.num_utterances, self.num_frames, self.num_coefficient), dtype=np.float32)
    if self.augmentation:
        idx = np.random.randint((feature.shape[0] - self.num_frames), size=self.num_utterances)
        for (num, index) in enumerate(idx):
            feature_cube[num, :, :] = feature[index:(index + self.num_frames), :]
    else:
        idx = range(self.num_utterances)
        for (num, index) in enumerate(idx):
            feature_cube[num, :, :] = feature[index:(index + self.num_frames), :]
    return {'feature': feature_cube[None, :, :, :], 'label': label}

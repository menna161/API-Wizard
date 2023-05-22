import sys
import tensorflow as tf
import threading
import random
import numpy as np
import os
from utils import audio
from hparams import hparams
from glob import glob
from collections import defaultdict


def _get_next_example(self, data_dir):
    'npz 1개를 읽어 처리한다. Loads a single example (input_wav, local_condition,speaker_id ) from disk'
    data_paths = self.path_dict[data_dir]
    while True:
        if (self._offset[data_dir] >= len(data_paths)):
            self._offset[data_dir] = 0
            self.rng.shuffle(data_paths)
        data_path = os.path.join(data_dir, data_paths[self._offset[data_dir]])
        self._offset[data_dir] += 1
        if os.path.exists(data_path):
            data = np.load(data_path)
        else:
            continue
        if (not self.skip_path_filter):
            break
        if (data['time_steps'] > self.sample_size):
            break
    input_wav = data['audio']
    local_condition = data['mel']
    input_wav = input_wav.reshape((- 1), 1)
    assert_ready_for_upsampling(input_wav, local_condition, self.hop_size)
    s = np.random.randint(0, ((len(local_condition) - self.max_frames) + 1))
    ts = (s * self.hop_size)
    input_wav = input_wav[(ts:(ts + (self.hop_size * self.max_frames)), :)]
    local_condition = local_condition[(s:(s + self.max_frames), :)]
    if self.gc_enable:
        return (input_wav, local_condition, self.data_dir_to_id[data_dir])
    else:
        return (input_wav, local_condition)

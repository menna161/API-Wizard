import os
import argparse
from datetime import datetime
from pathlib import Path
import pprint
from torch import optim
import platform
import torch.nn as nn


def __init__(self, **kwargs):
    'Configuration Class: set kwargs as class attributes with setattr'
    if (kwargs is not None):
        for (key, value) in kwargs.items():
            if (key == 'optimizer'):
                value = optimizer_dict[value]
            if (key == 'rnn'):
                value = rnn_dict[value]
            setattr(self, key, value)
    data_dir = project_dir.joinpath('datasets')
    self.dataset_dir = data_dir.joinpath(self.data)
    self.data_dir = self.dataset_dir.joinpath(self.mode)
    self.word2id_path = self.dataset_dir.joinpath('word2id.pkl')
    self.id2word_path = self.dataset_dir.joinpath('id2word.pkl')
    self.utter_path = self.data_dir.joinpath('utters.pkl')
    self.utter_length_path = self.data_dir.joinpath('utters_length.pkl')
    self.utter_scores_path = self.data_dir.joinpath('utters_scores.pkl')
    if ((self.mode == 'train') and (self.checkpoint is None)):
        time_now = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_path = save_dir.joinpath(self.data, self.model, time_now)
        self.logdir = str(self.save_path)
        os.makedirs(self.save_path, exist_ok=True)
    elif (self.checkpoint is not None):
        assert os.path.exists(self.checkpoint)
        self.save_path = os.path.dirname(self.checkpoint)
        self.logdir = str(self.save_path)
    self.pretrained_wv_path = None
    if ('bert' in self.data):
        self.embedding_size = 768
    if ('_25' in self.data):
        self.embedding_size = 25

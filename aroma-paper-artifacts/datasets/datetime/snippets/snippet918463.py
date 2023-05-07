import os
import argparse
from datetime import datetime
from pathlib import Path
import pprint
from torch import optim
import torch.nn as nn
from layers.rnncells import StackedGRUCell


def __init__(self, **kwargs):
    'Configuration Class: set kwargs as class attributes with setattr'
    if (kwargs is not None):
        for (key, value) in kwargs.items():
            if (key == 'optimizer'):
                value = optimizer_dict[value]
            if (key == 'rnn'):
                value = nn.GRU
            if (key == 'rnncell'):
                value = StackedGRUCell
            setattr(self, key, value)
    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir.joinpath('datasets')
    save_dir = project_dir.joinpath('results')
    self.dataset_dir = data_dir.joinpath(self.data_name)
    self.data_dir = self.dataset_dir.joinpath(self.mode)
    self.word2id_path = self.dataset_dir.joinpath('word2id.pkl')
    self.id2word_path = self.dataset_dir.joinpath('id2word.pkl')
    self.convs_path = self.data_dir.joinpath('convs.pkl')
    self.utterances_length_path = self.data_dir.joinpath('utterances_length.pkl')
    self.conversations_length_path = self.data_dir.joinpath('conversations_length.pkl')
    self.convs_users_path = self.data_dir.joinpath('convs_users.pkl')
    if ((self.mode == 'train') and (self.checkpoint is None)):
        time_now = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_path = save_dir.joinpath(self.data_name, self.model, time_now)
        self.logdir = str(self.save_path)
        os.makedirs(self.save_path, exist_ok=True)
    elif (self.checkpoint is not None):
        assert os.path.exists(self.checkpoint)
        self.save_path = os.path.dirname(self.checkpoint)
        self.logdir = str(self.save_path)
    if self.pretrained_wv:
        self.pretrained_wv_path = self.dataset_dir.joinpath('fasttext_wv.pkl')
        self.embedding_size = 300
    else:
        self.pretrained_wv_path = None
    if self.pretrained_uv:
        self.pretrained_uv_path = self.dataset_dir.joinpath('user_edge.pkl')
    else:
        self.pretrained_uv_path = None

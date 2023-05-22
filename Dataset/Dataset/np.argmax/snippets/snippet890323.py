import time
from .experiment import Experiment
from .nbsvm import preds_for_cell_content, preds_for_cell_content_max, preds_for_cell_content_multi
import dataclasses
from dataclasses import dataclass
from typing import Tuple
from axcell.helpers.training import set_seed
from fastai.text import *
import numpy as np
from pathlib import Path
import json
import argparse
import glob
import logging
import os
import random
import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from fastai.text import *
from tqdm import tqdm, trange
import tensorflow_datasets
from transformers import WEIGHTS_NAME, BertConfig, BertForSequenceClassification, BertTokenizer, RobertaConfig, RobertaForSequenceClassification, RobertaTokenizer, XLMConfig, XLMForSequenceClassification, XLMTokenizer, XLNetConfig, XLNetForSequenceClassification, XLNetTokenizer, DistilBertConfig, DistilBertForSequenceClassification, DistilBertTokenizer, DataProcessor, InputExample, AutoConfig
from transformers import AdamW, WarmupLinearSchedule
from transformers import glue_compute_metrics as compute_metrics
from transformers import glue_output_modes as output_modes
from transformers import glue_processors as processors
from transformers import glue_convert_examples_to_features as convert_examples_to_features
from transformers import AutoTokenizer, AutoModelForSequenceClassification, glue_convert_examples_to_features
from transformers.data.processors.glue import glue_processors
from torch.utils.tensorboard import SummaryWriter
from tensorboardX import SummaryWriter
from datetime import datetime
import socket
from apex import amp
import ptvsd


def evaluate(self, model, train_df, valid_df, test_df):
    data = self.get_databunch(train_df, valid_df, test_df)
    valid_probs = get_preds(self, model, data.valid_ds, ordered=True)[0].cpu().numpy()
    test_probs = get_preds(self, model, data.test_ds, ordered=True)[0].cpu().numpy()
    train_probs = get_preds(self, model, data.train_ds, ordered=True)[0].cpu().numpy()
    self._preds = []
    for (prefix, tdf, probs) in zip(['train', 'valid', 'test'], [train_df, valid_df, test_df], [train_probs, valid_probs, test_probs]):
        preds = np.argmax(probs, axis=1)
        if (self.merge_fragments and (self.merge_type != 'concat')):
            if (self.merge_type == 'vote_maj'):
                vote_results = preds_for_cell_content(tdf, probs)
            elif (self.merge_type == 'vote_avg'):
                vote_results = preds_for_cell_content_multi(tdf, probs)
            elif (self.merge_type == 'vote_max'):
                vote_results = preds_for_cell_content_max(tdf, probs)
            preds = vote_results['pred']
            true_y = vote_results['true']
        else:
            true_y = tdf['label']
            print(true_y.shape)
        self._set_results(prefix, preds, true_y)
        self._preds.append(probs)

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


@property
def experiment_name(self):
    from datetime import datetime
    import socket
    if (not self.name):
        now = datetime.now()
        d = now.strftime('%y%m%d_%H%M%S')
        h = '_'.join(socket.gethostname().split('-'))

        def short_name(name):
            return ''.join([p[0] for p in name.split('_')])

        def short_val(val):
            if isinstance(val, bool):
                return int(val)
            return val
        relevant_params = {k: v for (k, v) in dataclasses.asdict(self).items() if ((not k.startswith('_')) and hasattr(TransfoExperiment, k) and (getattr(TransfoExperiment, k) != v))}
        params = [f'{short_name(k)}_{v}' for (k, v) in relevant_params.items() if (not isinstance(v, bool))]
        bool_flags = [f'{short_name(k)}' for (k, v) in relevant_params.items() if (isinstance(v, bool) and v)]
        params_str = '.'.join((params + bool_flags))
        self.name = f'{d}.{h}.{params_str}'
    return self.name

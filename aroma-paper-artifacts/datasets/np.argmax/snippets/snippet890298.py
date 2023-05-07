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


def evaluate(args, model, eval_dataset, prefix='', eval_output_dir='/tmp/out'):
    results = {}
    eval_task = args.task_name
    if ((not os.path.exists(eval_output_dir)) and (args.local_rank in [(- 1), 0])):
        os.makedirs(eval_output_dir)
    args.eval_batch_size = (args.per_gpu_eval_batch_size * max(1, args.n_gpu))
    eval_sampler = (SequentialSampler(eval_dataset) if (args.local_rank == (- 1)) else DistributedSampler(eval_dataset))
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size)
    logger.info('***** Running evaluation {} *****'.format(prefix))
    logger.info('  Num examples = %d', len(eval_dataset))
    logger.info('  Batch size = %d', args.eval_batch_size)
    eval_loss = 0.0
    nb_eval_steps = 0
    preds = None
    out_label_ids = None
    mb = progress_bar(eval_dataloader)
    for batch in mb:
        model.eval()
        batch = tuple((t.to(args.device) for t in batch))
        with torch.no_grad():
            inputs = {'input_ids': batch[0], 'attention_mask': batch[1], 'labels': batch[3]}
            if (args.model_type != 'distilbert'):
                inputs['token_type_ids'] = (batch[2] if (args.model_type in ['bert', 'xlnet']) else None)
            outputs = model(**inputs)
            (tmp_eval_loss, logits) = outputs[:2]
            eval_loss += tmp_eval_loss.mean().item()
        nb_eval_steps += 1
        if (preds is None):
            preds = logits.detach().cpu().numpy()
            out_label_ids = inputs['labels'].detach().cpu().numpy()
        else:
            preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
            out_label_ids = np.append(out_label_ids, inputs['labels'].detach().cpu().numpy(), axis=0)
    eval_loss = (eval_loss / nb_eval_steps)
    if (args.output_mode == 'classification'):
        preds = np.argmax(preds, axis=1)
    elif (args.output_mode == 'regression'):
        preds = np.squeeze(preds)
    result = compute_metrics(eval_task, preds, out_label_ids)
    results.update(result)
    results['loss'] = eval_loss
    output_eval_file = os.path.join(eval_output_dir, prefix, 'eval_results.txt')
    with open(output_eval_file, 'w') as writer:
        logger.info('***** Eval results {} *****'.format(prefix))
        for key in sorted(result.keys()):
            logger.info('  %s = %s', key, str(result[key]))
            writer.write(('%s = %s\n' % (key, str(result[key]))))
    return results

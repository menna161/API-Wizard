import argparse
import copy
import itertools
import json
import logging
import math
import os
import random
import shutil
import sys
from collections import Counter, defaultdict, OrderedDict
from dataclasses import asdict, dataclass
from os.path import join, dirname, abspath
from typing import Callable, Dict, List, Set, Tuple, Union
import numpy as np
import transformers
import torch
import torch.nn as nn
import torch.nn.functional as F
from dacite import from_dict
from scipy import stats
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from transformers import BertTokenizer
from evidence_inference.preprocess import preprocessor
from evidence_inference.preprocess.preprocessor import PROMPT_ID_COL_NAME, LABEL, EVIDENCE_COL_NAME, EVIDENCE_START, EVIDENCE_END, STUDY_ID_COL
from evidence_inference.preprocess.representations import Document, Sentence, Token, to_structured, retokenize_with_bert
from evidence_inference.models.bert_model import initialize_models


def train_module(model: nn.Module, save_dir: str, model_name: str, train: List[Annotation], val: List[Annotation], model_pars: dict, sep_token_id: int, sampler: Callable[([Annotation], List[Tuple[(torch.IntTensor, Tuple[(torch.IntTensor, torch.IntTensor, torch.IntTensor)], int)]])], val_sampler: Callable[([Annotation], List[Tuple[(torch.IntTensor, Tuple[(torch.IntTensor, torch.IntTensor, torch.IntTensor)], int)]])], optimizer=None, scheduler=None, detokenizer=None) -> Tuple[(nn.Module, dict)]:
    'Trains a module for evidence identification or classification.\n    \n    Loosely based on the work done for the ERASER Benchmark: DeYoung et al., 2019\n\n    This method tracks loss on the entire validation set, saves intermediate\n    models, and supports restoring from an unfinished state. The best model on\n    the validation set is maintained, and the model stops training if a patience\n    (see below) number of epochs with no improvement is exceeded.\n\n    As there are likely too many negative examples to reasonably train a\n    classifier on everything, every epoch we subsample the negatives.\n\n    Args:\n        model: some model like BertClassifier\n        save_dir: a place to save intermediate and final results and models.\n        model_name: a string for saving information\n        train: a List of interned Annotation objects.\n        val: a List of interned Annotation objects.\n        #documents: a Dict of interned sentences\n        model_pars: Arbitrary parameters directory, assumed to contain:\n            lr: learning rate\n            batch_size: an int\n            sampling_method: a string, plus additional params in the dict to define creation of a sampler\n            epochs: the number of epochs to train for\n            patience: how long to wait for an improvement before giving up.\n            max_grad_norm: optional, clip gradients.\n        optimizer: what pytorch optimizer to use, if none, initialize Adam\n        scheduler: optional, do we want a scheduler involved in learning?\n        tensorize_model_inputs: should we convert our data to tensors before passing it to the model?\n                                Useful if we have a model that performs its own tokenization (e.g. BERT as a Service)\n\n    Returns:\n        the trained evidence identifier and a dictionary of intermediate results.\n    '
    logging.info(f'Beginning training {model_name} with {len(train)} annotations, {len(val)} for validation')
    output_dir = os.path.join(save_dir, f'{model_name}')
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    model_save_file = os.path.join(output_dir, f'{model_name}.pt')
    epoch_save_file = os.path.join(output_dir, f'{model_name}_epoch_data.pt')
    if (optimizer is None):
        optimizer = torch.optim.Adam(model.parameters(), lr=model_pars['lr'])
    criterion = nn.CrossEntropyLoss(reduction='none')
    batch_size = model_pars['batch_size']
    if ('oracle' in model_name):
        batch_size = (batch_size // 2)
    epochs = model_pars['epochs']
    patience = model_pars['patience']
    max_grad_norm = model_pars.get('max_grad_norm', None)
    device = next(model.parameters()).device
    results = {'sampled_epoch_train_acc': [], 'sampled_epoch_train_losses': [], 'sampled_epoch_train_f1': [], 'sampled_epoch_val_acc': [], 'sampled_epoch_val_losses': [], 'sampled_epoch_val_f1': [], 'full_epoch_val_losses': [], 'full_epoch_val_f1': [], 'full_epoch_val_acc': []}
    start_epoch = 0
    best_epoch = (- 1)
    best_val_loss = float('inf')
    best_val_f1 = float('-inf')
    best_model_state_dict = None
    epoch_data = {}
    if os.path.exists(epoch_save_file):
        model.load_state_dict(torch.load(model_save_file))
        epoch_data = torch.load(epoch_save_file)
        start_epoch = (epoch_data['epoch'] + 1)
        if bool(epoch_data.get('done', 0)):
            start_epoch = epochs
        results = epoch_data['results']
        best_epoch = start_epoch
        best_model_state_dict = OrderedDict({k: v.cpu() for (k, v) in model.state_dict().items()})
        logging.info(f'Restored training from epoch {start_epoch}')
    logging.info(f'Training evidence model from epoch {start_epoch} until epoch {epochs}')
    optimizer.zero_grad()
    sep = torch.tensor(sep_token_id, dtype=torch.int).unsqueeze(0)
    for epoch in range(start_epoch, epochs):
        epoch_train_data = list(itertools.chain.from_iterable((sampler(t) for t in train)))
        assert (len(epoch_train_data) > 0)
        train_classes = Counter((x[(- 1)] for x in epoch_train_data))
        random.shuffle(epoch_train_data)
        epoch_val_data = list(itertools.chain.from_iterable((sampler(v) for v in val)))
        assert (len(epoch_val_data) > 0)
        val_classes = Counter((x[(- 1)] for x in epoch_val_data))
        random.shuffle(epoch_val_data)
        sampled_epoch_train_loss = 0
        model.train()
        logging.info(f'Training with {(len(epoch_train_data) // batch_size)} batches with {len(epoch_train_data)} examples')
        logging.info(f'Training classes distribution: {train_classes}, valing class distribution: {val_classes}')
        hard_train_preds = []
        hard_train_truths = []
        optimizer.zero_grad()
        for batch_start in range(0, len(epoch_train_data), batch_size):
            model.train()
            batch_elements = epoch_train_data[batch_start:min((batch_start + batch_size), len(epoch_train_data))]
            (sentences, queries, targets) = zip(*filter((lambda x: x), batch_elements))
            hard_train_truths.extend(targets)
            queries = [torch.cat([i, sep, c, sep, o]).to(dtype=torch.long) for (i, c, o) in queries]
            preds = model(queries, sentences)
            hard_train_preds.extend([x.cpu().item() for x in torch.argmax(preds, dim=(- 1))])
            targets = torch.tensor(targets, dtype=torch.long, device=device)
            loss = criterion(preds, targets.to(device=preds.device)).sum()
            sampled_epoch_train_loss += loss.item()
            loss = (loss / len(preds))
            loss.backward()
            if max_grad_norm:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()
            if scheduler:
                scheduler.step()
            optimizer.zero_grad()
        sampled_epoch_train_loss /= len(epoch_train_data)
        results['sampled_epoch_train_losses'].append(sampled_epoch_train_loss)
        results['sampled_epoch_train_acc'].append(accuracy_score(hard_train_truths, hard_train_preds))
        results['sampled_epoch_train_f1'].append(classification_report(hard_train_truths, hard_train_preds, output_dict=True))
        logging.info(f"Epoch {epoch} sampled training loss {sampled_epoch_train_loss}, acc {results['sampled_epoch_train_acc'][(- 1)]}")
        with torch.no_grad():
            model.eval()
            (sampled_epoch_val_loss, _, sampled_epoch_val_hard_pred, sampled_epoch_val_truth) = make_preds_epoch(model, epoch_val_data, batch_size, sep_token_id, device, criterion)
            sampled_epoch_val_acc = accuracy_score(sampled_epoch_val_truth, sampled_epoch_val_hard_pred)
            sampled_epoch_val_f1 = classification_report(sampled_epoch_val_truth, sampled_epoch_val_hard_pred, output_dict=True)
            results['sampled_epoch_val_losses'].append(sampled_epoch_val_loss)
            results['sampled_epoch_val_acc'].append(sampled_epoch_val_acc)
            results['sampled_epoch_val_f1'].append(sampled_epoch_val_f1)
            logging.info(f'Epoch {epoch} sampled val loss {sampled_epoch_val_loss}, acc {sampled_epoch_val_acc}, f1: {sampled_epoch_val_f1}')
            all_val_data = list(itertools.chain.from_iterable((val_sampler(v) for v in val)))
            (epoch_val_loss, epoch_val_soft_pred, epoch_val_hard_pred, epoch_val_truth) = make_preds_epoch(model, all_val_data, batch_size, sep_token_id, device, criterion)
            results['full_epoch_val_losses'].append(epoch_val_loss)
            results['full_epoch_val_acc'].append(accuracy_score(epoch_val_truth, epoch_val_hard_pred))
            results['full_epoch_val_f1'].append(classification_report(epoch_val_truth, epoch_val_hard_pred, output_dict=True))
            logging.info(f"Epoch {epoch} full val loss {epoch_val_loss}, accuracy: {results['full_epoch_val_acc'][(- 1)]}, f1: {results['full_epoch_val_f1'][(- 1)]}")
            full_val_f1 = results['full_epoch_val_f1'][(- 1)]['macro avg']['f1-score']
            if (full_val_f1 > best_val_f1):
                logging.debug(f'Epoch {epoch} new best model with full val f1 {full_val_f1}')
                best_model_state_dict = OrderedDict({k: v.cpu() for (k, v) in model.state_dict().items()})
                best_epoch = epoch
                best_val_f1 = full_val_f1
                torch.save(model.state_dict(), model_save_file)
                epoch_data = {'epoch': epoch, 'results': results, 'best_val_loss': best_val_loss, 'done': 0}
                torch.save(epoch_data, epoch_save_file)
        if ((epoch - best_epoch) > patience):
            epoch_data['done'] = 1
            torch.save(epoch_data, epoch_save_file)
            break
    epoch_data['done'] = 1
    epoch_data['results'] = results
    torch.save(epoch_data, epoch_save_file)
    model.load_state_dict(best_model_state_dict)
    model = model.to(device=device)
    model.eval()
    return (model, results)

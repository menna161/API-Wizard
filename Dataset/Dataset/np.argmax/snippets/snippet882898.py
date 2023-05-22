import os
import datetime
import logging
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import numpy as np
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
from pytorch_pretrained_bert.optimization import BertAdam
from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE
from tqdm import tqdm
from tabulate import tabulate
import processors
import tools
import argparse
import printcm


@torch.no_grad()
def predict(self, eval_examples):
    'predicts the class for a list of known samples'
    eval_features = tools.convert_examples_to_features(eval_examples, self.label_list, self.max_seq_length, self.tokenizer)
    eval_examples_count = len(eval_examples)
    logger.info('***** Running evaluation *****')
    logger.info('  Num examples = %d', eval_examples_count)
    logger.info('  Batch size = %d', args.eval_batch_size)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
    self.model.eval()
    if self.fp16:
        self.model.half()
    predictions = np.array([])
    truth = np.array([f.label_id for f in eval_features], dtype=int)
    for (input_ids, input_mask, segment_ids) in tqdm(eval_dataloader, desc='test batches'):
        input_ids = input_ids.to(self.device)
        input_mask = input_mask.to(self.device)
        segment_ids = segment_ids.to(self.device)
        logits = self.model(input_ids, segment_ids, input_mask)
        logits = logits.detach().cpu().numpy()
        predictions = np.append(predictions, np.argmax(logits, axis=1))
    lookup = self.processor.get_labels()
    map_classes = (lambda x: [lookup[int(item)] for item in x])
    return (map_classes(truth), map_classes(predictions))

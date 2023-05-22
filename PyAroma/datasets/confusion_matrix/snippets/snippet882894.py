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


def run(args):
    model = BertTest(**vars(args))
    processor = processors.processor_for_task(args.task_name)
    data = processor.get_text_data_by_dataset(args.data_dir)
    table = []
    all_truth = []
    all_prediction = []
    print('datasets')
    print([f' {row[0]} - {len(row[1])} ' for row in data])
    for row in data:
        (truth, prediction) = model.predict(row[1])
        result = stat_fscore(truth, prediction)
        table.append(([row[0]] + result))
        all_truth.extend(truth)
        all_prediction.extend(prediction)
    table.append((['all'] + stat_fscore(all_truth, all_prediction)))
    sumRow = ['sum']
    for col in range(1, len(table[0])):
        rowSum = sum(map((lambda x: x[col]), table))
        sumRow.append(rowSum)
    table.append(sumRow)
    headers = ['file', 'precisionMicro', 'recallMicro', 'fscoreMicro', 'precisionMacro', 'recallMacro', 'fscoreMacro']
    print(tabulate(table, headers, tablefmt='pipe', floatfmt='.4f'))
    plt = printcm.plot_confusion_matrix(all_truth, all_prediction, classes=['negative', 'neutral', 'positive'], normalize=True, title='Bert unbalanced')
    plt.savefig((args.output_dir + 'cm.pdf'))
    return table

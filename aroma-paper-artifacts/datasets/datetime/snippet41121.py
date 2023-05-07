from __future__ import print_function
from miscc.config import cfg, cfg_from_file
from datasets import TextDataset
from trainer import condGANTrainer as trainer
import os
import sys
import time
import random
import pprint
import datetime
import dateutil.tz
import argparse
import numpy as np
from shutil import copyfile
import torch
import torchvision.transforms as transforms
from nltk.tokenize import RegexpTokenizer


def gen_example(wordtoix, algo):
    'generate images from example sentences'
    from nltk.tokenize import RegexpTokenizer
    filepath = ('%s/example_filenames.txt' % cfg.DATA_DIR)
    data_dic = {}
    with open(filepath, 'r') as f:
        filenames = f.read().decode('utf8').split('\n')
        for name in filenames:
            if (len(name) == 0):
                continue
            filepath = ('%s/%s.txt' % (cfg.DATA_DIR, name))
            with open(filepath, 'r') as f:
                print('Load from:', name)
                sentences = f.read().decode('utf8').split('\n')
                captions = []
                cap_lens = []
                for sent in sentences:
                    if (len(sent) == 0):
                        continue
                    sent = sent.replace('��', ' ')
                    tokenizer = RegexpTokenizer('\\w+')
                    tokens = tokenizer.tokenize(sent.lower())
                    if (len(tokens) == 0):
                        print('sent', sent)
                        continue
                    rev = []
                    for t in tokens:
                        t = t.encode('ascii', 'ignore').decode('ascii')
                        if ((len(t) > 0) and (t in wordtoix)):
                            rev.append(wordtoix[t])
                    captions.append(rev)
                    cap_lens.append(len(rev))
            max_len = np.max(cap_lens)
            sorted_indices = np.argsort(cap_lens)[::(- 1)]
            cap_lens = np.asarray(cap_lens)
            cap_lens = cap_lens[sorted_indices]
            cap_array = np.zeros((len(captions), max_len), dtype='int64')
            for i in range(len(captions)):
                idx = sorted_indices[i]
                cap = captions[idx]
                c_len = len(cap)
                cap_array[(i, :c_len)] = cap
            key = name[(name.rfind('/') + 1):]
            data_dic[key] = [cap_array, cap_lens, sorted_indices]
    algo.gen_example(data_dic)

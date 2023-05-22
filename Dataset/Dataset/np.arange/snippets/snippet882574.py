import numpy as np
from tqdm import tqdm
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from flair.data import Sentence
from flair.models import SequenceTagger
import sys
import os
import pickle
from collections import OrderedDict
import json
from lm import LanguageModel as Model
import utils


def segment_noise(dataset, summary):
    chunk_dict = {}
    grammar_set = []
    rands = np.random.rand(10000)
    rand_idx = 0
    gidx = 0
    batch_size = 128
    file_dir = (('data/' + dataset) + '/')
    model_file = ('model/%s/lm.model' % dataset)
    dict_file = ('model/%s/lm.dict.p' % dataset)
    train_file = ('data/%s/train.json' % dataset)
    (tokens_list, tags_list) = chunk_text(train_file)
    token_dict = pickle.load(open(dict_file, 'rb'))
    word_size = len(token_dict)
    word_dim = 256
    hidden_dim = 512
    model = Model(word_size, word_dim, hidden_dim)
    model.cuda()
    if os.path.exists(model_file):
        best_point = torch.load(model_file)
        state_dict = best_point['state_dict']
        new_state_dict = OrderedDict()
        for (k, v) in state_dict.items():
            temp = state_dict[k]
            if k.startswith('module.'):
                k = k[7:]
                new_state_dict[k] = temp
        model.load_state_dict(new_state_dict)
    model.eval()
    shuffle_indices = np.random.permutation(np.arange(len(tokens_list)))
    tokens_list = np.array(tokens_list)[shuffle_indices]
    tags_list = np.array(tags_list)[shuffle_indices]
    noised_data = []
    rev_token_dict = {token_dict[token]: token for token in token_dict}
    for _ in range(1):
        for idx in tqdm(range(0, len(tokens_list), batch_size)):
            tokens_batch = tokens_list[idx:(idx + batch_size)]
            tags_batch = tags_list[idx:(idx + batch_size)]
            probs_batch = []
            probs_indices_batch = []
            for tokens in tqdm(tokens_batch):
                if (not check_sentence([rev_token_dict[token] for token in tokens])):
                    continue
                (x_batch, x_mask) = utils.pad([tokens])
                x_batch = to_tensor(x_batch)
                x_mask = to_tensor(x_mask).float()
                ps_batch = model(x_batch, x_mask, ps_only=True)
                ps_batch = F.softmax(ps_batch, dim=(- 1))
                ps_batch = list(ps_batch.cpu().detach().numpy())
                probs_sequence = []
                probs_indices_sequence = []
                for ps in ps_batch[0]:
                    (probs, probs_indices) = nuclear_filter(ps)
                    probs_sequence.append(probs)
                    probs_indices_sequence.append(probs_indices)
                probs_batch.append(probs_sequence)
                probs_indices_batch.append(probs_indices_sequence)
            chunk_dict = {}
            grammar_set = []
            chunks_batch = []
            ctags_batch = []
            for (tokens, tags) in zip(tokens_batch, tags_batch):
                (chunks, ctags) = split_to_chunks(tokens[1:(- 1)], tags, chunk_dict, grammar_set)
                chunks_batch.append(chunks)
                ctags_batch.append(ctags)
            for chunk in chunk_dict:
                chunk_dict[chunk] = list(set(chunk_dict[chunk]))
            grammar_set = list(set(grammar_set))
            np.random.shuffle(grammar_set)
            ps_idx = 0
            for (j, (tokens, chunks, ctags)) in enumerate(tqdm(zip(tokens_batch, chunks_batch, ctags_batch), total=len(chunks_batch))):
                if (not check_sentence([rev_token_dict[token] for token in tokens])):
                    continue
                lm_chunk_inputs = []
                probs = probs_batch[ps_idx]
                probs_indices = probs_indices_batch[ps_idx]
                ps_idx += 1
                if (dataset == 'rotten'):
                    N = 20
                else:
                    N = 8
                for _ in tqdm(range(N)):
                    try:
                        new_chunks = replace_tokens(chunks, probs, probs_indices)
                        (new_chunks, new_ctags) = remove_chunks(new_chunks, ctags)
                        lm_chunk_input = insert_chunks(new_chunks, new_ctags, chunk_dict, grammar_set, rands, rand_idx, gidx)
                        lm_chunk_input = ' '.join([rev_token_dict[token] for token in lm_chunk_input])
                        lm_chunk_inputs.append(lm_chunk_input)
                    except:
                        pass
                inst = {}
                inst['summary'] = ' '.join([rev_token_dict[token] for token in tokens[1:(- 1)]])
                inst['segment_reviews'] = lm_chunk_inputs
                noised_data.append(inst)
    return noised_data

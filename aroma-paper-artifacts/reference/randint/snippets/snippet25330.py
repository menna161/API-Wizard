import os
import json
import random
import collections
from tools.common import logger, init_logger
from argparse import ArgumentParser
from tools.common import seed_everything
from model.tokenization_bert import BertTokenizer
from callback.progressbar import ProgressBar
from pathlib import Path


def create_instances_from_document(all_documents, document_index, max_seq_length, short_seq_prob, masked_lm_prob, max_predictions_per_seq, vocab_words):
    'Creates `TrainingInstance`s for a single document.\n     This method is changed to create sentence-order prediction (SOP) followed by idea from paper of ALBERT, 2019-08-28, brightmart\n    '
    document = all_documents[document_index]
    max_num_tokens = (max_seq_length - 3)
    target_seq_length = max_num_tokens
    if (random.random() < short_seq_prob):
        target_seq_length = random.randint(2, max_num_tokens)
    instances = []
    current_chunk = []
    current_length = 0
    i = 0
    while (i < len(document)):
        segment = document[i]
        current_chunk.append(segment)
        current_length += len(segment)
        if ((i == (len(document) - 1)) or (current_length >= target_seq_length)):
            if current_chunk:
                a_end = 1
                if (len(current_chunk) >= 2):
                    a_end = random.randint(1, (len(current_chunk) - 1))
                tokens_a = []
                for j in range(a_end):
                    tokens_a.extend(current_chunk[j])
                tokens_b = []
                for j in range(a_end, len(current_chunk)):
                    tokens_b.extend(current_chunk[j])
                if ((len(tokens_a) == 0) or (len(tokens_b) == 0)):
                    continue
                if (random.random() < 0.5):
                    is_random_next = True
                    temp = tokens_a
                    tokens_a = tokens_b
                    tokens_b = temp
                else:
                    is_random_next = False
                truncate_seq_pair(tokens_a, tokens_b, max_num_tokens)
                assert (len(tokens_a) >= 1)
                assert (len(tokens_b) >= 1)
                tokens = ((((['[CLS]'] + tokens_a) + ['[SEP]']) + tokens_b) + ['[SEP]'])
                segment_ids = ([0 for _ in range((len(tokens_a) + 2))] + [1 for _ in range((len(tokens_b) + 1))])
                (tokens, masked_lm_positions, masked_lm_labels) = create_masked_lm_predictions(tokens, masked_lm_prob, max_predictions_per_seq, vocab_words)
                instance = {'tokens': tokens, 'segment_ids': segment_ids, 'is_random_next': is_random_next, 'masked_lm_positions': masked_lm_positions, 'masked_lm_labels': masked_lm_labels}
                instances.append(instance)
            current_chunk = []
            current_length = 0
        i += 1
    return instances

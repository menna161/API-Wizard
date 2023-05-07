import argparse
import os
import unittest
from inspect import currentframe, getframeinfo
import numpy as np
import torch
from fairseq.data import data_utils as fairseq_data_utils
from fairseq.data.dictionary import Dictionary
from fairseq.models import BaseFairseqModel, FairseqDecoder, FairseqEncoder, FairseqEncoderDecoderModel, FairseqEncoderModel, FairseqModel
from fairseq.tasks.fairseq_task import FairseqTask
from examples.speech_recognition.data.data_utils import lengths_to_encoder_padding_mask


def get_dummy_input(T=100, D=80, B=5, K=100):
    forward_input = {}
    feature = torch.randn(B, T, D)
    src_lengths = torch.from_numpy(np.random.randint(low=1, high=T, size=B, dtype=np.int64))
    src_lengths[0] = T
    prev_output_tokens = []
    for b in range(B):
        token_length = np.random.randint(low=1, high=(src_lengths[b].item() + 1))
        tokens = np.random.randint(low=0, high=K, size=token_length, dtype=np.int64)
        prev_output_tokens.append(torch.from_numpy(tokens))
    prev_output_tokens = fairseq_data_utils.collate_tokens(prev_output_tokens, pad_idx=1, eos_idx=2, left_pad=False, move_eos_to_beginning=False)
    (src_lengths, sorted_order) = src_lengths.sort(descending=True)
    forward_input['src_tokens'] = feature.index_select(0, sorted_order)
    forward_input['src_lengths'] = src_lengths
    forward_input['prev_output_tokens'] = prev_output_tokens
    return forward_input

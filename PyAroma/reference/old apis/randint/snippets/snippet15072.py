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


def get_dummy_encoder_output(encoder_out_shape=(100, 80, 5)):
    '\n    This only provides an example to generate dummy encoder output\n    '
    (T, B, D) = encoder_out_shape
    encoder_out = {}
    encoder_out['encoder_out'] = torch.from_numpy(np.random.randn(*encoder_out_shape).astype(np.float32))
    seq_lengths = torch.from_numpy(np.random.randint(low=1, high=T, size=B))
    encoder_out['encoder_padding_mask'] = (torch.arange(T).view(1, T).expand(B, (- 1)) >= seq_lengths.view(B, 1).expand((- 1), T))
    encoder_out['encoder_padding_mask'].t_()
    return encoder_out

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


def setUpModel(self, model_cls, extra_args_setters=None):
    self.assertTrue(issubclass(model_cls, (FairseqEncoderDecoderModel, FairseqModel)), msg='This class only tests for FairseqModel subclasses')
    (task, parser) = get_dummy_task_and_parser()
    model_cls.add_args(parser)
    args = parser.parse_args([])
    if (extra_args_setters is not None):
        for args_setter in extra_args_setters:
            args_setter(args)
    model = model_cls.build_model(args, task)
    self.model = model

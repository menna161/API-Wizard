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


def setUp(self):
    args = self.setUpArgs()
    self.model = DummyEncoderModel(encoder=DummyEncoder())
    self.criterion = self.criterion_cls.build_criterion(args=args, task=DummyTask(args))

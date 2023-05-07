import argparse
import tempfile
import unittest
import tests.utils as test_utils
import torch
from fairseq import search
from fairseq.data.dictionary import Dictionary
from fairseq.models.transformer import TransformerModel
from fairseq.sequence_generator import SequenceGenerator, EnsembleModel
from fairseq.tasks.fairseq_task import FairseqTask


def setUp(self):
    (self.task, self.parser) = get_dummy_task_and_parser()
    eos = self.task.tgt_dict.eos()
    src_tokens = torch.randint(3, 50, (2, 10)).long()
    src_tokens = torch.cat((src_tokens, torch.LongTensor([[eos], [eos]])), (- 1))
    src_lengths = torch.LongTensor([2, 10])
    self.sample = {'net_input': {'src_tokens': src_tokens, 'src_lengths': src_lengths}}
    TransformerModel.add_args(self.parser)
    args = self.parser.parse_args([])
    args.encoder_layers = 2
    args.decoder_layers = 1
    self.transformer_model = TransformerModel.build_model(args, self.task)

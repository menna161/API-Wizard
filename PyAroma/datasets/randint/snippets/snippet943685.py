import argparse
import tempfile
import unittest
import torch
from fairseq.data.dictionary import Dictionary
from fairseq.models.lstm import LSTMModel
from fairseq.tasks.fairseq_task import FairseqTask


def test_assert_jit_vs_nonjit_(self):
    (task, parser) = get_dummy_task_and_parser()
    LSTMModel.add_args(parser)
    args = parser.parse_args([])
    args.criterion = ''
    model = LSTMModel.build_model(args, task)
    model.eval()
    scripted_model = torch.jit.script(model)
    scripted_model.eval()
    idx = len(task.source_dictionary)
    iter = 100
    seq_len_tensor = torch.randint(1, 10, (iter,))
    num_samples_tensor = torch.randint(1, 10, (iter,))
    for i in range(iter):
        seq_len = seq_len_tensor[i]
        num_samples = num_samples_tensor[i]
        src_token = (torch.randint(0, idx, (num_samples, seq_len)),)
        src_lengths = torch.randint(1, (seq_len + 1), (num_samples,))
        (src_lengths, _) = torch.sort(src_lengths, descending=True)
        src_lengths[0] = seq_len
        prev_output_token = (torch.randint(0, idx, (num_samples, 1)),)
        result = model(src_token[0], src_lengths, prev_output_token[0], None)
        scripted_result = scripted_model(src_token[0], src_lengths, prev_output_token[0], None)
        self.assertTensorEqual(result[0], scripted_result[0])
        self.assertTensorEqual(result[1], scripted_result[1])

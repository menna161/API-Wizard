import contextlib
from io import StringIO
import logging
import os
import random
import tempfile
import unittest
import torch
from fairseq import options
from fairseq_cli import train
from fairseq_cli import eval_lm
from fairseq_cli import validate
from tests.utils import create_dummy_data, preprocess_lm_data, preprocess_translation_data, train_translation_model, generate_main


def _create_dummy_data(filename):
    random_data = torch.rand((num_examples * maxlen))
    input_data = (97 + torch.floor((26 * random_data)).int())
    if regression:
        output_data = torch.rand((num_examples, num_classes))
    else:
        output_data = (1 + torch.floor((num_classes * torch.rand(num_examples))).int())
    with open(os.path.join(data_dir, input_dir, (filename + '.out')), 'w') as f_in:
        label_filename = ((filename + '.label') if regression else (filename + '.out'))
        with open(os.path.join(data_dir, 'label', label_filename), 'w') as f_out:
            offset = 0
            for i in range(num_examples):
                ex_len = random.randint(1, maxlen)
                ex_str = ' '.join(map(chr, input_data[offset:(offset + ex_len)]))
                print(ex_str, file=f_in)
                if regression:
                    class_str = ' '.join(map(str, output_data[i].numpy()))
                    print(class_str, file=f_out)
                else:
                    class_str = 'class{}'.format(output_data[i])
                    print(class_str, file=f_out)
                offset += ex_len

import logging
import math
from itertools import groupby
import torch
import torch.nn.functional as F
from fairseq import utils
from fairseq.criterions import FairseqCriterion, register_criterion
from examples.speech_recognition.data.data_utils import encoder_padding_mask_to_lengths
from examples.speech_recognition.utils.wer_utils import Code, EditDistance, Token


def compute_ctc_uer(logprobs, targets, input_lengths, target_lengths, blank_idx):
    '\n        Computes utterance error rate for CTC outputs\n\n        Args:\n            logprobs: (Torch.tensor)  N, T1, D tensor of log probabilities out\n                of the encoder\n            targets: (Torch.tensor) N, T2 tensor of targets\n            input_lengths: (Torch.tensor) lengths of inputs for each sample\n            target_lengths: (Torch.tensor) lengths of targets for each sample\n            blank_idx: (integer) id of blank symbol in target dictionary\n\n        Returns:\n            batch_errors: (float) errors in the batch\n            batch_total: (float)  total number of valid samples in batch\n    '
    batch_errors = 0.0
    batch_total = 0.0
    for b in range(logprobs.shape[0]):
        predicted = logprobs[b][:input_lengths[b]].argmax(1).tolist()
        target = targets[b][:target_lengths[b]].tolist()
        predicted = [p[0] for p in groupby(predicted)]
        nonblanks = []
        for p in predicted:
            if (p != blank_idx):
                nonblanks.append(p)
        predicted = nonblanks
        alignment = EditDistance(False).align(arr_to_toks(predicted), arr_to_toks(target))
        for a in alignment.codes:
            if (a != Code.match):
                batch_errors += 1
        batch_total += len(target)
    return (batch_errors, batch_total)

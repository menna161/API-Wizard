import numpy as np
import torch
import torch.nn.functional as F
from fairseq.models import register_model, register_model_architecture
from fairseq.models.nat import LevenshteinTransformerDecoder, LevenshteinTransformerModel, FairseqNATModel, ensemble_decoder
from fairseq.models.transformer import Linear
from fairseq.utils import new_arange
from fairseq.modules.transformer_sentence_encoder import init_bert_params
from fairseq import libnat
import sys


def compute_score_full(self, L, tau):
    s = ((- abs(((np.arange(0, (L - 1))[(:, None)] / 2) - np.arange(L)[(None, :)]))) / tau)
    s = (np.tril(s, 0) + np.triu((s - float('inf')), 1))
    s = np.exp((s - s.max(1, keepdims=True)))
    return (s / s.sum(1, keepdims=True))

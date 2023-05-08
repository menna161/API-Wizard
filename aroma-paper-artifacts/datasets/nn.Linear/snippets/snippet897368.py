import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.models import FairseqDecoder, FairseqLanguageModel, register_model, register_model_architecture
from fairseq.modules import LayerNorm, TransformerSentenceEncoder
from fairseq.modules.transformer_sentence_encoder import init_bert_params
from .hub_interface import RobertaHubInterface
from fairseq import hub_utils


def __init__(self, embed_dim, output_dim, activation_fn, weight=None):
    super().__init__()
    self.dense = nn.Linear(embed_dim, embed_dim)
    self.activation_fn = utils.get_activation_fn(activation_fn)
    self.layer_norm = LayerNorm(embed_dim)
    if (weight is None):
        weight = nn.Linear(embed_dim, output_dim, bias=False).weight
    self.weight = weight
    self.bias = nn.Parameter(torch.zeros(output_dim))

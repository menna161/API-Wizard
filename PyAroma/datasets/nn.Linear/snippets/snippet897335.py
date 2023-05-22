import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.models import FairseqDecoder, FairseqLanguageModel, register_model, register_model_architecture
from fairseq.modules import LayerNorm, TransformerSentenceEncoder
from fairseq.modules.transformer_sentence_encoder import init_bert_params
from .hub_interface import McbertHubInterface
from fairseq import hub_utils


def __init__(self, embed_dim, output_dim, activation_fn, embed_tokens):
    super().__init__()
    self.embed_dim = embed_dim
    self.output_dim = output_dim
    self.dense = nn.Linear(embed_dim, embed_dim)
    self.activation_fn = utils.get_activation_fn(activation_fn)
    self.layer_norm = LayerNorm(embed_dim)
    self.embed_tokens = embed_tokens
    self.bias = nn.Embedding(embed_tokens.num_embeddings, 1)

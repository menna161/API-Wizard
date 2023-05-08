import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import utils
from fairseq.models import FairseqDecoder, FairseqLanguageModel, register_model, register_model_architecture
from fairseq.modules import LayerNorm, TransformerSentenceEncoder
from fairseq.modules.transformer_sentence_encoder import init_bert_params
from .hub_interface import ElectraHubInterface
from fairseq import hub_utils


def __init__(self, embed_dim, output_dim):
    super().__init__()
    self.dense = nn.Linear(embed_dim, output_dim)

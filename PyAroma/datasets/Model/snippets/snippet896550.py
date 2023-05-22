import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq import options, utils
from fairseq.models import FairseqEncoder, FairseqIncrementalDecoder, FairseqEncoderDecoderModel, register_model, register_model_architecture
from fairseq.modules import AdaptiveSoftmax, LayerNorm, PositionalEmbedding, SinusoidalPositionalEmbedding, TransformerDecoderLayer, TransformerEncoderLayer


@classmethod
def build_model(cls, args, task):
    transformer_align(args)
    transformer_model = TransformerModel.build_model(args, task)
    return TransformerAlignModel(transformer_model.encoder, transformer_model.decoder, args)

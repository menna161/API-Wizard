import logging
import math
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq.models import BaseFairseqModel, register_model, register_model_architecture
from fairseq.modules import Fp32GroupNorm, Fp32LayerNorm, GumbelVectorQuantizer, KmeansVectorQuantizer
from fairseq.utils import buffered_arange


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_wav2vec_architecture(args)
    model = Wav2VecModel(args)
    logger.info(model)
    return model

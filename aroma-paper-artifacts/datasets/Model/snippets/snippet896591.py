import sys
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import BaseFairseqModel, register_model, register_model_architecture


@classmethod
def build_model(cls, args, task):
    'Build a new model instance.'
    base_wav2vec_architecture(args)
    model = Wav2VecModel(args)
    print(model)
    return model

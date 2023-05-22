from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.seq2vec_encoders import PytorchSeq2VecWrapper
from allennlp.modules.feedforward import FeedForward
from allennlp.nn.activations import Activation


def _init_weights(self, module):
    ' Initialize the weights '
    if isinstance(module, nn.Linear):
        module.weight.data.normal_(mean=0.0, std=0.02)
    elif isinstance(module, nn.LayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)
    if (isinstance(module, nn.Linear) and (module.bias is not None)):
        module.bias.data.zero_()

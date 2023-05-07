from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.seq2vec_encoders import PytorchSeq2VecWrapper
from allennlp.modules.feedforward import FeedForward
from allennlp.nn.activations import Activation


def __init__(self, neural_ir_model: nn.Module, representation_size: int, vocab_size: int):
    super(PreTrain_MLM_POD_Head, self).__init__()
    self.neural_ir_model = neural_ir_model
    self.mlm_head = nn.Linear(representation_size, vocab_size)
    self.loss_fct = torch.nn.CrossEntropyLoss()
    self.loss_fct2 = torch.nn.BCEWithLogitsLoss(reduction='none')
    self.loss_fct3 = torch.nn.BCEWithLogitsLoss(reduction='mean')
    self.apply(self._init_weights)
    self.check_inter_passage_pod = False
    self.doc_pass_pod = True

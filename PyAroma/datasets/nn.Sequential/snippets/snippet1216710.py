from typing import Dict, List, Any
import torch
import torch.nn.functional as F
import torch.nn.parallel
from allennlp.data.vocabulary import Vocabulary
from allennlp.models.model import Model
from allennlp.modules import TextFieldEmbedder, Seq2SeqEncoder, FeedForward, InputVariationalDropout, TimeDistributed
from allennlp.training.metrics import CategoricalAccuracy
from allennlp.modules.matrix_attention import BilinearMatrixAttention
from utils.detector import SimpleDetector
from allennlp.nn.util import masked_softmax, weighted_sum, replace_masked_values
from allennlp.nn import InitializerApplicator
from models.multiatt.henG import Graph_reasoning
import torch.nn as nn


def __init__(self, vocab: Vocabulary, span_encoder: Seq2SeqEncoder, reasoning_encoder: Seq2SeqEncoder, input_dropout: float=0.3, hidden_dim_maxpool: int=1024, class_embs: bool=True, reasoning_use_obj: bool=True, reasoning_use_answer: bool=True, reasoning_use_question: bool=True, pool_reasoning: bool=True, pool_answer: bool=True, pool_question: bool=False, initializer: InitializerApplicator=InitializerApplicator()):
    super(HGL_Model, self).__init__(vocab)
    self.detector = SimpleDetector(pretrained=True, average_pool=True, semantic=class_embs, final_dim=512)
    self.rnn_input_dropout = (TimeDistributed(InputVariationalDropout(input_dropout)) if (input_dropout > 0) else None)
    self.span_encoder = TimeDistributed(span_encoder)
    self.reasoning_encoder = TimeDistributed(reasoning_encoder)
    self.Graph_reasoning = Graph_reasoning(512)
    self.QAHG = BilinearMatrixAttention(matrix_1_dim=span_encoder.get_output_dim(), matrix_2_dim=span_encoder.get_output_dim())
    self.VAHG = BilinearMatrixAttention(matrix_1_dim=span_encoder.get_output_dim(), matrix_2_dim=self.detector.final_dim)
    self.reasoning_use_obj = reasoning_use_obj
    self.reasoning_use_answer = reasoning_use_answer
    self.reasoning_use_question = reasoning_use_question
    self.pool_reasoning = pool_reasoning
    self.pool_answer = pool_answer
    self.pool_question = pool_question
    dim = sum([d for (d, to_pool) in [(reasoning_encoder.get_output_dim(), self.pool_reasoning), (span_encoder.get_output_dim(), self.pool_answer), (span_encoder.get_output_dim(), self.pool_question)] if to_pool])
    self.final_mlp = torch.nn.Sequential(torch.nn.Dropout(input_dropout, inplace=False), torch.nn.Linear(dim, hidden_dim_maxpool), torch.nn.ReLU(inplace=True), torch.nn.Dropout(input_dropout, inplace=False), torch.nn.Linear(hidden_dim_maxpool, 1))
    self._accuracy = CategoricalAccuracy()
    self._loss = torch.nn.CrossEntropyLoss()
    initializer(self)

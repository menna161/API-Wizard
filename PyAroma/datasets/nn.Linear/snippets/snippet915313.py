import copy
import logging
from typing import Dict, Tuple
import numpy
import torch
import torch.nn.functional as F
from machamp.model.machamp_decoder import MachampDecoder
from machamp.modules.allennlp.bilinear_matrix_attention import BilinearMatrixAttention
from machamp.modules.allennlp.chu_liu_edmonds import decode_mst


def __init__(self, task: str, vocabulary, input_dim: int, device: str, loss_weight: float=1.0, metric: str='las', topn: int=1, tag_representation_dim: int=256, arc_representation_dim: int=768, **kwargs) -> None:
    super().__init__(task, vocabulary, loss_weight, metric, device, **kwargs)
    self.input_dim = input_dim
    arc_representation_dim = arc_representation_dim
    self.head_arc_feedforward = torch.nn.Linear(self.input_dim, arc_representation_dim).to(self.device)
    self.child_arc_feedforward = copy.deepcopy(self.head_arc_feedforward)
    self.arc_attention = BilinearMatrixAttention(arc_representation_dim, arc_representation_dim, use_input_biases=True).to(self.device)
    num_labels = len(self.vocabulary.get_vocab(task))
    self.topn = topn
    self.head_tag_feedforward = torch.nn.Linear(self.input_dim, tag_representation_dim).to(self.device)
    self.child_tag_feedforward = copy.deepcopy(self.head_tag_feedforward)
    self.tag_bilinear = torch.nn.modules.Bilinear(tag_representation_dim, tag_representation_dim, num_labels).to(self.device)
    self._head_sentinel = torch.nn.Parameter(torch.randn([1, 1, self.input_dim], device=self.device))

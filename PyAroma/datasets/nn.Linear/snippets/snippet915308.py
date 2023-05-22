import logging
from typing import cast, List
import torch
import torch.nn.functional as F
from machamp.model.machamp_decoder import MachampDecoder
from machamp.modules.allennlp.conditional_random_field import ConditionalRandomField, allowed_transitions


def __init__(self, task: str, vocabulary, input_dim: int, device: str, loss_weight: float=1.0, metric: str='accuracy', topn: int=1, **kwargs) -> None:
    super().__init__(task, vocabulary, loss_weight, metric, device, **kwargs)
    nlabels = len(self.vocabulary.get_vocab(task))
    self.input_dim = input_dim
    self.hidden_to_label = torch.nn.Linear(input_dim, nlabels)
    self.hidden_to_label.to(device)
    constraints = allowed_transitions('BIO', vocabulary.inverse_namespaces[task])
    self.crf_layer = ConditionalRandomField(nlabels, constraints)
    self.loss_function = torch.nn.CrossEntropyLoss(ignore_index=0)
    if (topn != 1):
        logger.info('Top-n for crf is not supported for now, as it is unclear how to get the probabilities. We disabled it automatically')
        topn = 1
    self.topn = topn

import torch
import torch.nn.functional as F
from machamp.model.machamp_decoder import MachampDecoder


def __init__(self, task, vocabulary, input_dim, device, loss_weight: float=1.0, topn: int=1, metric: str='accuracy', **kwargs):
    super().__init__(task, vocabulary, loss_weight, metric, device, **kwargs)
    nlabels = len(self.vocabulary.get_vocab(task))
    self.hidden_to_label = torch.nn.Linear(input_dim, nlabels)
    self.hidden_to_label.to(device)
    self.loss_function = torch.nn.CrossEntropyLoss(reduction='sum', ignore_index=(- 100))
    self.topn = topn

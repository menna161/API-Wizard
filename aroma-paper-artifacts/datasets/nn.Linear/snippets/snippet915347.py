import torch
import torch.nn.functional as F
from machamp.model.machamp_decoder import MachampDecoder


def __init__(self, task: str, vocabulary, input_dim: int, device: str, loss_weight: float=1.0, metric: str='accuracy', topn: int=1, **kwargs) -> None:
    super().__init__(task, vocabulary, loss_weight, metric, device, **kwargs)
    nlabels = len(self.vocabulary.get_vocab(task))
    self.input_dim = input_dim
    self.hidden_to_label = torch.nn.Linear(input_dim, nlabels)
    self.hidden_to_label.to(device)
    self.loss_function = torch.nn.CrossEntropyLoss(ignore_index=(- 100))
    self.topn = topn

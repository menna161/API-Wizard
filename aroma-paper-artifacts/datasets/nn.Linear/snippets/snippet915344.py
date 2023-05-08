import torch
from machamp.model.machamp_decoder import MachampDecoder


def __init__(self, task, vocabulary, input_dim, device, loss_weight: float=1.0, topn: int=1, metric: str='avg_dist', **kwargs):
    super().__init__(task, vocabulary, loss_weight, metric, device, **kwargs)
    self.hidden_to_label = torch.nn.Linear(input_dim, 1)
    self.hidden_to_label.to(device)
    self.loss_function = torch.nn.MSELoss()
    self.topn = topn

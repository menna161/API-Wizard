import torch.optim
from . import FairseqOptimizer, register_optimizer


def __init__(self, args, params):
    super().__init__(args)
    self._optimizer = torch.optim.SGD(params, **self.optimizer_config)

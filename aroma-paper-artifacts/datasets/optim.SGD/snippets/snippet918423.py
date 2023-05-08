import torch
from nnunet.training.network_training.nnUNetTrainerV2 import nnUNetTrainerV2


def initialize_optimizer_and_scheduler(self):
    current_momentum = 0.99
    min_momentum = 0.9
    if (self.epoch > 800):
        current_momentum = (current_momentum - (((current_momentum - min_momentum) / 200) * (self.epoch - 800)))
    self.print_to_log_file('current momentum', current_momentum)
    assert (self.network is not None), 'self.initialize_network must be called first'
    if (self.optimizer is None):
        self.optimizer = torch.optim.SGD(self.network.parameters(), self.initial_lr, weight_decay=self.weight_decay, momentum=0.99, nesterov=True)
    else:
        self.optimizer.param_groups[0]['momentum'] = current_momentum
    self.lr_scheduler = None

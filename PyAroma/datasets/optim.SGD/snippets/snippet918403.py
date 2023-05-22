import torch
from nnunet.training.network_training.nnUNetTrainer import nnUNetTrainer
from nnunet.training.network_training.nnUNetTrainerV2 import nnUNetTrainerV2
from torch.optim import lr_scheduler


def initialize_optimizer_and_scheduler(self):
    self.optimizer = torch.optim.SGD(self.network.parameters(), self.initial_lr, weight_decay=self.weight_decay, momentum=0.99, nesterov=True)
    self.lr_scheduler = lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.2, patience=self.lr_scheduler_patience, verbose=True, threshold=self.lr_scheduler_eps, threshold_mode='abs')

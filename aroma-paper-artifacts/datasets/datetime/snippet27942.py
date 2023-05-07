import os
import glob
from datetime import datetime
import numpy as np
import torch
from . import meters
from . import utils
from .dataloaders import get_data_loaders
from tensorboardX import SummaryWriter


def train(self):
    'Perform training.'
    if self.archive_code:
        utils.archive_code(os.path.join(self.checkpoint_dir, 'archived_code.zip'), filetypes=['.py', '.yml'])
    utils.dump_yaml(os.path.join(self.checkpoint_dir, 'configs.yml'), self.cfgs)
    start_epoch = 0
    self.metrics_trace.reset()
    self.train_iter_per_epoch = len(self.train_loader)
    self.model.to_device(self.device)
    self.model.init_optimizers()
    if self.resume:
        start_epoch = self.load_checkpoint(optim=True)
    if self.use_logger:
        from tensorboardX import SummaryWriter
        self.logger = SummaryWriter(os.path.join(self.checkpoint_dir, 'logs', datetime.now().strftime('%Y%m%d-%H%M%S')))
        self.viz_input = self.val_loader.__iter__().__next__()
    print(f'{self.model.model_name}: optimizing to {self.num_epochs} epochs')
    for epoch in range(start_epoch, self.num_epochs):
        self.current_epoch = epoch
        metrics = self.run_epoch(self.train_loader, epoch)
        self.metrics_trace.append('train', metrics)
        with torch.no_grad():
            metrics = self.run_epoch(self.val_loader, epoch, is_validation=True)
            self.metrics_trace.append('val', metrics)
        if (((epoch + 1) % self.save_checkpoint_freq) == 0):
            self.save_checkpoint((epoch + 1), optim=True)
        self.metrics_trace.plot(pdf_path=os.path.join(self.checkpoint_dir, 'metrics.pdf'))
        self.metrics_trace.save(os.path.join(self.checkpoint_dir, 'metrics.json'))
    print(f'Training completed after {(epoch + 1)} epochs.')

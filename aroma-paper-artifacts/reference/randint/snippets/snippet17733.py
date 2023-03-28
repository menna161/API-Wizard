import importlib
import os
import time
import torch
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data.distributed
import torchvision
from torchvision import datasets, transforms, models
import horovod.torch as hvd
from advex_uar.common.loader import StridedImageFolder


def _val_epoch(self, epoch):
    self.model.eval()
    val_std_loss = Metric('val_std_loss')
    val_std_acc = Metric('val_std_acc')
    val_adv_acc = Metric('val_adv_acc')
    val_adv_loss = Metric('val_adv_loss')
    val_max_adv_acc = Metric('val_max_adv_acc')
    val_max_adv_loss = Metric('val_max_adv_loss')
    for (batch_idx, (data, target)) in enumerate(self.val_loader):
        if self.cuda:
            (data, target) = (data.cuda(non_blocking=True), target.cuda(non_blocking=True))
        with torch.no_grad():
            output = self.model(data)
            val_std_loss.update(F.cross_entropy(output, target))
            val_std_acc.update(accuracy(output, target))
        if self.attack:
            rand_target = torch.randint(0, (len(self.val_dataset.classes) - 1), target.size(), dtype=target.dtype, device='cuda')
            rand_target = torch.remainder(((target + rand_target) + 1), len(self.val_dataset.classes))
            data_adv = self.attack(self.model, data, rand_target, avoid_target=False, scale_eps=self.scale_eps)
            data_max_adv = self.attack(self.model, data, rand_target, avoid_target=False, scale_eps=False)
            with torch.no_grad():
                output_adv = self.model(data_adv)
                val_adv_loss.update(F.cross_entropy(output_adv, target))
                val_adv_acc.update(accuracy(output_adv, target))
                output_max_adv = self.model(data_max_adv)
                val_max_adv_loss.update(F.cross_entropy(output_max_adv, target))
                val_max_adv_acc.update(accuracy(output_max_adv, target))
        self.model.eval()
    if (hvd.rank() == 0):
        log_dict = {'val_std_loss': val_std_loss.avg.item(), 'val_std_acc': val_std_acc.avg.item(), 'val_adv_loss': val_adv_loss.avg.item(), 'val_adv_acc': val_adv_acc.avg.item(), 'val_adv_loss': val_max_adv_loss.avg.item(), 'val_max_adv_acc': val_max_adv_acc.avg.item()}
        self.logger.log(log_dict, epoch)
    if self.verbose:
        print(log_dict)
    self.optimizer.synchronize()
    self.optimizer.zero_grad()

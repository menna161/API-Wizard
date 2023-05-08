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


def _train_epoch(self, epoch):
    self.model.train()
    train_std_loss = Metric('train_std_loss')
    train_std_acc = Metric('train_std_acc')
    train_adv_loss = Metric('train_adv_loss')
    train_adv_acc = Metric('train_adv_acc')
    if self.attack:
        self.attack.set_epoch(epoch)
    for (batch_idx, (data, target)) in enumerate(self.train_loader):
        if self.cuda:
            (data, target) = (data.cuda(non_blocking=True), target.cuda(non_blocking=True))
        self._adjust_learning_rate(epoch, batch_idx)
        loss = torch.zeros([], dtype=torch.float32, device='cuda')
        if ((not self.attack) or (self.attack_loss == 'avg')):
            output = self.model(data)
            loss += self._compute_loss(output, target)
            train_std_loss.update(loss)
            train_std_acc.update(accuracy(output, target))
        else:
            with torch.no_grad():
                self.model.eval()
                output = self.model(data)
                train_std_loss_val = self._compute_loss(output, target)
                train_std_loss.update(train_std_loss_val)
                train_std_acc.update(accuracy(output, target))
                self.model.train()
        if self.attack:
            if self.rand_target:
                attack_target = torch.randint(0, (len(self.val_dataset.classes) - 1), target.size(), dtype=target.dtype, device='cuda')
                attack_target = torch.remainder(((target + attack_target) + 1), len(self.val_dataset.classes))
            adv_loss = torch.zeros([], dtype=torch.float32, device='cuda')
            if self.rand_target:
                data_adv = self.attack(self.model, data, attack_target, avoid_target=False, scale_eps=self.scale_eps)
            else:
                data_adv = self.attack(self.model, data, target, avoid_target=True, scale_eps=self.scale_eps)
            output_adv = self.model(data_adv)
            adv_loss = self._compute_loss(output_adv, target)
            train_adv_loss.update(adv_loss)
            train_adv_acc.update(accuracy(output_adv, target))
            loss += adv_loss
            if (self.attack_loss == 'avg'):
                loss /= 2.0
        self.optimizer.synchronize()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    if (hvd.rank() == 0):
        log_dict = {'train_std_loss': train_std_loss.avg.item(), 'train_std_acc': train_std_acc.avg.item(), 'train_adv_loss': train_adv_loss.avg.item(), 'train_adv_acc': train_adv_acc.avg.item()}
        print(log_dict)
        self.logger.log(log_dict, epoch)

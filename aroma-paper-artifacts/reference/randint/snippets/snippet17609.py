import importlib
import os
import subprocess
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
import torch.utils.data
from torchvision import datasets, transforms, models
from advex_uar.common.loader import StridedImageFolder
from advex_uar.eval.cifar10c import CIFAR10C
from advex_uar.train.trainer import Metric, accuracy, correct


def evaluate(self):
    self.model.eval()
    std_loss = Accumulator('std_loss')
    adv_loss = Accumulator('adv_loss')
    std_corr = Accumulator('std_corr')
    adv_corr = Accumulator('adv_corr')
    std_logits = Accumulator('std_logits')
    adv_logits = Accumulator('adv_logits')
    seen_classes = []
    adv_images = Accumulator('adv_images')
    first_batch_images = Accumulator('first_batch_images')
    for (batch_idx, (data, target)) in enumerate(self.val_loader):
        if self.cuda:
            (data, target) = (data.cuda(non_blocking=True), target.cuda(non_blocking=True))
        with torch.no_grad():
            output = self.model(data)
            std_logits.update(output.cpu())
            loss = F.cross_entropy(output, target, reduction='none').cpu()
            std_loss.update(loss)
            corr = correct(output, target)
            corr = corr.view(corr.size()[0]).cpu()
            std_corr.update(corr)
        rand_target = torch.randint(0, (self.nb_classes - 1), target.size(), dtype=target.dtype, device='cuda')
        rand_target = torch.remainder(((target + rand_target) + 1), self.nb_classes)
        data_adv = self.attack(self.model, data, rand_target, avoid_target=False, scale_eps=False)
        for idx in range(target.size()[0]):
            if (target[idx].cpu() not in seen_classes):
                seen_classes.append(target[idx].cpu())
                orig_image = norm_to_pil_image(data[idx].detach().cpu())
                adv_image = norm_to_pil_image(data_adv[idx].detach().cpu())
                adv_images.update((orig_image, adv_image, target[idx].cpu()))
        if (batch_idx == 0):
            for idx in range(target.size()[0]):
                orig_image = norm_to_pil_image(data[idx].detach().cpu())
                adv_image = norm_to_pil_image(data_adv[idx].detach().cpu())
                first_batch_images.update((orig_image, adv_image))
        with torch.no_grad():
            output_adv = self.model(data_adv)
            adv_logits.update(output_adv.cpu())
            loss = F.cross_entropy(output_adv, target, reduction='none').cpu()
            adv_loss.update(loss)
            corr = correct(output_adv, target)
            corr = corr.view(corr.size()[0]).cpu()
            adv_corr.update(corr)
        run_output = {'std_loss': std_loss.avg, 'std_acc': std_corr.avg, 'adv_loss': adv_loss.avg, 'adv_acc': adv_corr.avg}
        print('Batch', batch_idx)
        print(run_output)
        if ((batch_idx % 20) == 0):
            self.logger.log(run_output, batch_idx)
    summary_dict = {'std_acc': std_corr.avg.item(), 'adv_acc': adv_corr.avg.item()}
    self.logger.log_summary(summary_dict)
    for (orig_img, adv_img, target) in adv_images.vals:
        self.logger.log_image(orig_img, 'orig_{}.png'.format(target))
        self.logger.log_image(adv_img, 'adv_{}.png'.format(target))
    for (idx, imgs) in enumerate(first_batch_images.vals):
        (orig_img, adv_img) = imgs
        self.logger.log_image(orig_img, 'init_orig_{}.png'.format(idx))
        self.logger.log_image(adv_img, 'init_adv_{}.png'.format(idx))
    self.logger.end()
    print(std_loss.avg, std_corr.avg, adv_loss.avg, adv_corr.avg)

import os
import math
import numpy as np
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F


def test_one_epoch(self, net_model, args):
    '\n        Sampling from ddpm\n        Inputs:\n            net_model   : The net in reverse process of DDPM\n            args        : Hyper-parameters\n        Outputs:\n            noisy       : The noise sampled from N(0, 1)\n            sampled_img : The image sampled via reverse process of DDPM\n        '
    with torch.no_grad():
        print('model load weight done.')
        net_model.eval()
        self.ddpm_sampler = GaussianDiffusionSampler(net_model, self.beta_1, self.beta_T, self.T).to(self.device)
        noisy_img = torch.randn(size=[args.batch_size, 3, 32, 32], device=self.device)
        noisy = torch.clamp(((noisy_img * 0.5) + 0.5), 0, 1)
        sampled_img = self.ddpm_sampler(noisy_img)
        return (noisy, sampled_img)

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import partial
from collections import OrderedDict
from config import config
from resnet import get_resnet50


def forward(self, x, gt=None):
    (b, c, h, w, l) = x.shape
    if self.training:
        gt = gt.view(b, 1, h, w, l).float()
        for_encoder = torch.cat([x, gt], dim=1)
        enc = self.encoder(for_encoder)
        pred_mean = self.mean(enc)
        pred_log_var = self.log_var(enc)
        decoder_x = self.decoder_x(x)
        out_samples = []
        out_samples_gsnn = []
        for i in range(config.samples):
            std = pred_log_var.mul(0.5).exp_()
            eps = torch.randn([b, self.latent_size, (h // 4), (w // 4), (l // 4)]).cuda()
            z1 = ((eps * std) + pred_mean)
            z2 = torch.randn([b, self.latent_size, (h // 4), (w // 4), (l // 4)]).cuda()
            sketch = self.decoder(torch.cat([decoder_x, z1], dim=1))
            out_samples.append(sketch)
            sketch_gsnn = self.decoder(torch.cat([decoder_x, z2], dim=1))
            out_samples_gsnn.append(sketch_gsnn)
        sketch = torch.cat([torch.unsqueeze(out_sample, dim=0) for out_sample in out_samples])
        sketch = torch.mean(sketch, dim=0)
        sketch_gsnn = torch.cat([torch.unsqueeze(out_sample, dim=0) for out_sample in out_samples_gsnn])
        sketch_gsnn = torch.mean(sketch_gsnn, dim=0)
        return (pred_mean, pred_log_var, sketch_gsnn, sketch)
    else:
        out_samples = []
        for i in range(config.samples):
            z = torch.randn([b, self.latent_size, (h // 4), (w // 4), (l // 4)]).cuda()
            decoder_x = self.decoder_x(x)
            out = self.decoder(torch.cat([decoder_x, z], dim=1))
            out_samples.append(out)
        sketch_gsnn = torch.cat([torch.unsqueeze(out_sample, dim=0) for out_sample in out_samples])
        sketch_gsnn = torch.mean(sketch_gsnn, dim=0)
        return (None, None, sketch_gsnn, None)

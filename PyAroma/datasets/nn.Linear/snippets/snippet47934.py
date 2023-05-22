from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, device, num_classes, num_colors, args):
    super(MLP, self).__init__()
    self.batch_norm = args.batch_norm
    self.patch_size = args.patch_size
    self.batch_size = args.batch_size
    self.num_colors = num_colors
    self.num_classes = num_classes
    self.device = device
    self.out_channels = args.out_channels
    self.seen_tasks = []
    self.num_samples = args.var_samples
    self.latent_dim = args.var_latent_dim
    self.encoder = nn.Sequential(OrderedDict([('encoder_layer1', SingleLinearLayer(1, (self.num_colors * (self.patch_size ** 2)), 400, batch_norm=self.batch_norm)), ('encoder_layer2', SingleLinearLayer(2, 400, 400, batch_norm=self.batch_norm))]))
    self.latent_mu = nn.Linear(400, self.latent_dim, bias=False)
    self.latent_std = nn.Linear(400, self.latent_dim, bias=False)
    self.classifier = nn.Sequential(nn.Linear(self.latent_dim, num_classes, bias=False))
    self.decoder = nn.Sequential(OrderedDict([('decoder_layer0', SingleLinearLayer(0, self.latent_dim, 400, batch_norm=self.batch_norm)), ('decoder_layer1', SingleLinearLayer(1, 400, 400, batch_norm=self.batch_norm)), ('decoder_layer2', nn.Linear(400, (self.out_channels * (self.patch_size ** 2)), bias=False))]))

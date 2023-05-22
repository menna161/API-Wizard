from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, device, num_classes, num_colors, args):
    super(MLP, self).__init__()
    self.batch_norm = args.batch_norm
    self.patch_size = args.patch_size
    self.batch_size = args.batch_size
    self.dropout = args.dropout
    self.num_colors = num_colors
    self.num_classes = num_classes
    self.device = device
    self.variational = False
    self.joint = False
    if args.train_var:
        self.variational = True
        self.num_samples = args.var_samples
        self.latent_dim = args.var_latent_dim
    else:
        self.latent_dim = 400
    if args.joint:
        self.joint = True
    self.encoder = nn.Sequential(OrderedDict([('encoder_layer1', SingleLinearLayer(1, (self.num_colors * (self.patch_size ** 2)), 400, batch_norm=self.batch_norm, dropout=self.dropout)), ('encoder_layer2', SingleLinearLayer(2, 400, 400, batch_norm=self.batch_norm, dropout=self.dropout))]))
    if self.variational:
        self.latent_mu = nn.Linear(400, self.latent_dim, bias=False)
        self.latent_std = nn.Linear(400, self.latent_dim, bias=False)
    if self.joint:
        self.classifier = nn.Sequential(nn.Linear(self.latent_dim, num_classes, bias=False))
        if self.variational:
            self.latent_decoder = SingleLinearLayer(0, self.latent_dim, 400, batch_norm=self.batch_norm)
        self.decoder = nn.Sequential(OrderedDict([('decoder_layer1', SingleLinearLayer(1, 400, 400, batch_norm=self.batch_norm, dropout=self.dropout)), ('decoder_layer2', nn.Linear(400, (self.num_colors * (self.patch_size ** 2)), bias=False))]))
    else:
        self.classifier = nn.Sequential(nn.Linear(self.latent_dim, num_classes, bias=False))

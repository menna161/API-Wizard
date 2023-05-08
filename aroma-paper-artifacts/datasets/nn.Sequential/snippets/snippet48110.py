from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, device, num_classes, num_colors, args):
    super(DCNN, self).__init__()
    self.batch_norm = args.batch_norm
    self.patch_size = args.patch_size
    self.batch_size = args.batch_size
    self.num_colors = num_colors
    self.num_classes = num_classes
    self.dropout = args.dropout
    self.device = device
    self.inner_kernel_size = 4
    self.inner_padding = 0
    self.outer_padding = 1
    if (args.patch_size < 32):
        self.inner_kernel_size = 3
        self.inner_padding = 1
        self.outer_padding = 0
    self.variational = False
    self.joint = False
    if args.train_var:
        self.variational = True
        self.num_samples = args.var_samples
        self.latent_dim = args.var_latent_dim
    else:
        self.latent_dim = 1024
    if args.joint:
        self.joint = True
    self.encoder = nn.Sequential(OrderedDict([('encoder_layer1', SingleConvLayer(1, self.num_colors, 128, kernel_size=4, stride=2, padding=1, batch_norm=self.batch_norm, dropout=self.dropout)), ('encoder_layer2', SingleConvLayer(2, 128, 256, kernel_size=4, stride=2, padding=1, batch_norm=self.batch_norm, dropout=self.dropout)), ('encoder_layer3', SingleConvLayer(3, 256, 512, kernel_size=4, stride=2, padding=1, batch_norm=self.batch_norm, dropout=self.dropout)), ('encoder_layer4', SingleConvLayer(4, 512, 1024, kernel_size=self.inner_kernel_size, stride=2, padding=0, batch_norm=self.batch_norm, dropout=self.dropout))]))
    (self.enc_channels, self.enc_spatial_dim_x, self.enc_spatial_dim_y) = get_feat_size(self.encoder, self.patch_size, self.num_colors)
    if self.variational:
        self.latent_mu = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), self.latent_dim, bias=False)
        self.latent_std = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), self.latent_dim, bias=False)
        self.latent_feat_out = self.latent_dim
    else:
        self.latent_feat_out = ((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels)
    if self.joint:
        self.classifier = nn.Sequential(nn.Linear(self.latent_feat_out, num_classes, bias=False))
        if self.variational:
            self.latent_decoder = SingleLinearLayer(0, self.latent_feat_out, ((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), batch_norm=self.batch_norm)
        self.decoder = nn.Sequential(OrderedDict([('decoder_layer1', SingleConvLayer(1, 1024, 512, kernel_size=4, stride=2, padding=self.inner_padding, batch_norm=self.batch_norm, is_transposed=True, dropout=self.dropout)), ('decoder_layer2', SingleConvLayer(2, 512, 256, kernel_size=4, stride=2, padding=self.outer_padding, batch_norm=self.batch_norm, is_transposed=True, dropout=self.dropout)), ('decoder_layer3', SingleConvLayer(3, 256, 128, kernel_size=4, stride=2, padding=self.outer_padding, batch_norm=self.batch_norm, is_transposed=True, dropout=self.dropout)), ('decoder_layer4', nn.ConvTranspose2d(128, self.num_colors, kernel_size=4, stride=2, padding=1, bias=False))]))
    else:
        self.classifier = nn.Sequential(nn.Linear(self.latent_feat_out, num_classes, bias=False))

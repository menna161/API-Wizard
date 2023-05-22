from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, device, num_classes, num_colors, args):
    super(WRN, self).__init__()
    self.widen_factor = args.wrn_widen_factor
    self.depth = args.wrn_depth
    self.batch_norm = args.batch_norm
    self.patch_size = args.patch_size
    self.batch_size = args.batch_size
    self.num_colors = num_colors
    self.num_classes = num_classes
    self.dropout = args.dropout
    self.device = device
    self.nChannels = [args.wrn_embedding_size, (16 * self.widen_factor), (32 * self.widen_factor), (64 * self.widen_factor)]
    assert (((self.depth - 4) % 6) == 0)
    self.num_block_layers = int(((self.depth - 4) / 6))
    self.variational = False
    self.joint = False
    if args.train_var:
        self.variational = True
        self.num_samples = args.var_samples
        self.latent_dim = args.var_latent_dim
    if args.joint:
        self.joint = True
    self.encoder = nn.Sequential(OrderedDict([('encoder_conv1', nn.Conv2d(num_colors, self.nChannels[0], kernel_size=3, stride=1, padding=1, bias=False)), ('encoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[0], self.nChannels[1], WRNBasicBlock, batchnorm=self.batch_norm, dropout=self.dropout)), ('encoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[2], WRNBasicBlock, batchnorm=self.batch_norm, stride=2, dropout=self.dropout)), ('encoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[3], WRNBasicBlock, batchnorm=self.batch_norm, stride=2, dropout=self.dropout)), ('encoder_bn1', nn.BatchNorm2d(self.nChannels[3], eps=self.batch_norm)), ('encoder_act1', nn.ReLU(inplace=True))]))
    (self.enc_channels, self.enc_spatial_dim_x, self.enc_spatial_dim_y) = get_feat_size(self.encoder, self.patch_size, self.num_colors)
    if self.variational:
        self.latent_mu = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_x) * self.enc_channels), self.latent_dim, bias=False)
        self.latent_std = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), self.latent_dim, bias=False)
        self.latent_feat_out = self.latent_dim
    else:
        self.latent_feat_out = ((self.enc_spatial_dim_x * self.enc_spatial_dim_x) * self.enc_channels)
        self.latent_dim = self.latent_feat_out
        print(self.latent_dim)
    if self.joint:
        self.classifier = nn.Sequential(nn.Linear(self.latent_feat_out, num_classes, bias=False))
        if self.variational:
            self.latent_decoder = nn.Linear(self.latent_feat_out, ((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), bias=False)
        self.decoder = nn.Sequential(OrderedDict([('decoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[3], self.nChannels[2], WRNBasicBlock, dropout=self.dropout, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample1', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[1], WRNBasicBlock, dropout=self.dropout, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample2', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[0], WRNBasicBlock, dropout=self.dropout, batchnorm=self.batch_norm, stride=1)), ('decoder_bn1', nn.BatchNorm2d(self.nChannels[0], eps=self.batch_norm)), ('decoder_act1', nn.ReLU(inplace=True)), ('decoder_conv1', nn.Conv2d(self.nChannels[0], self.num_colors, kernel_size=3, stride=1, padding=1, bias=False))]))
    else:
        self.classifier = nn.Sequential(nn.Linear(self.latent_feat_out, num_classes, bias=False))

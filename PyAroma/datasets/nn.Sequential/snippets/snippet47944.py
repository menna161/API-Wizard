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
    self.device = device
    self.out_channels = args.out_channels
    self.double_blocks = args.double_wrn_blocks
    self.seen_tasks = []
    self.num_samples = args.var_samples
    self.latent_dim = args.var_latent_dim
    self.nChannels = [args.wrn_embedding_size, (16 * self.widen_factor), (32 * self.widen_factor), (64 * self.widen_factor), (64 * self.widen_factor), (64 * self.widen_factor), (64 * self.widen_factor)]
    if self.double_blocks:
        assert (((self.depth - 2) % 12) == 0)
        self.num_block_layers = int(((self.depth - 2) / 12))
        self.encoder = nn.Sequential(OrderedDict([('encoder_conv1', nn.Conv2d(num_colors, self.nChannels[0], kernel_size=3, stride=1, padding=1, bias=False)), ('encoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[0], self.nChannels[1], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[2], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[3], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block4', WRNNetworkBlock(self.num_block_layers, self.nChannels[3], self.nChannels[4], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block5', WRNNetworkBlock(self.num_block_layers, self.nChannels[4], self.nChannels[5], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block6', WRNNetworkBlock(self.num_block_layers, self.nChannels[5], self.nChannels[6], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_bn1', nn.BatchNorm2d(self.nChannels[6], eps=self.batch_norm)), ('encoder_act1', nn.ReLU(inplace=True))]))
    else:
        assert (((self.depth - 2) % 6) == 0)
        self.num_block_layers = int(((self.depth - 2) / 6))
        self.encoder = nn.Sequential(OrderedDict([('encoder_conv1', nn.Conv2d(num_colors, self.nChannels[0], kernel_size=3, stride=1, padding=1, bias=False)), ('encoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[0], self.nChannels[1], WRNBasicBlock, batchnorm=self.batch_norm)), ('encoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[2], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[3], WRNBasicBlock, batchnorm=self.batch_norm, stride=2)), ('encoder_bn1', nn.BatchNorm2d(self.nChannels[3], eps=self.batch_norm)), ('encoder_act1', nn.ReLU(inplace=True))]))
    (self.enc_channels, self.enc_spatial_dim_x, self.enc_spatial_dim_y) = get_feat_size(self.encoder, self.patch_size, self.num_colors)
    self.latent_mu = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_x) * self.enc_channels), self.latent_dim, bias=False)
    self.latent_std = nn.Linear(((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), self.latent_dim, bias=False)
    self.classifier = nn.Sequential(nn.Linear(self.latent_dim, num_classes, bias=False))
    self.latent_decoder = nn.Linear(self.latent_dim, ((self.enc_spatial_dim_x * self.enc_spatial_dim_y) * self.enc_channels), bias=False)
    if self.double_blocks:
        self.decoder = nn.Sequential(OrderedDict([('decoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[6], self.nChannels[5], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample1', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[5], self.nChannels[4], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample2', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[4], self.nChannels[3], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample3', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block4', WRNNetworkBlock(self.num_block_layers, self.nChannels[3], self.nChannels[2], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample4', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block5', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[1], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample5', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block6', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[0], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_bn1', nn.BatchNorm2d(self.nChannels[0], eps=self.batch_norm)), ('decoder_act1', nn.ReLU(inplace=True)), ('decoder_upsample6', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_conv1', nn.Conv2d(self.nChannels[0], self.out_channels, kernel_size=3, stride=1, padding=1, bias=False))]))
    else:
        self.decoder = nn.Sequential(OrderedDict([('decoder_block1', WRNNetworkBlock(self.num_block_layers, self.nChannels[3], self.nChannels[2], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample1', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block2', WRNNetworkBlock(self.num_block_layers, self.nChannels[2], self.nChannels[1], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_upsample2', nn.Upsample(scale_factor=2, mode='nearest')), ('decoder_block3', WRNNetworkBlock(self.num_block_layers, self.nChannels[1], self.nChannels[0], WRNBasicBlock, batchnorm=self.batch_norm, stride=1)), ('decoder_bn1', nn.BatchNorm2d(self.nChannels[0], eps=self.batch_norm)), ('decoder_act1', nn.ReLU(inplace=True)), ('decoder_conv1', nn.Conv2d(self.nChannels[0], self.out_channels, kernel_size=3, stride=1, padding=1, bias=False))]))

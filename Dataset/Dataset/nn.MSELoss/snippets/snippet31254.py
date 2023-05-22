import torch
import torch.nn as nn
import numpy as np


def __init__(self, gan_type='wgan_gp', target_real_label=1.0, target_fake_label=0.0):
    super(GANLoss, self).__init__()
    self.register_buffer('real_label', torch.tensor(target_real_label))
    self.register_buffer('fake_label', torch.tensor(target_fake_label))
    self.gan_type = gan_type
    if (gan_type == 'wgan_gp'):
        self.loss = nn.MSELoss()
    elif (gan_type == 'lsgan'):
        self.loss = nn.MSELoss()
    elif (gan_type == 'vanilla'):
        self.loss = nn.BCELoss()
    elif (gan_type == 're_s_gan'):
        self.loss = nn.BCEWithLogitsLoss()
    elif (gan_type == 're_avg_gan'):
        self.loss = nn.BCEWithLogitsLoss()
    else:
        raise ValueError(('GAN type [%s] not recognized.' % gan_type))

import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from .vgg import Vgg19
import math
import cv2
import numpy as np
import scipy.stats as st
import code


def __init__(self, gan_mode, target_real_label=1.0, target_fake_label=0.0):
    ' Initialize the GANLoss class.\n\n        Parameters:\n            gan_mode (str) - - the type of GAN objective. It currently supports vanilla, lsgan, and wgangp.\n            target_real_label (bool) - - label for a real image\n            target_fake_label (bool) - - label of a fake image\n\n        Note: Do not use sigmoid as the last layer of Discriminator.\n        LSGAN needs no sigmoid. vanilla GANs will handle it with BCEWithLogitsLoss.\n        '
    super(GANLoss, self).__init__()
    self.register_buffer('real_label', torch.tensor(target_real_label))
    self.register_buffer('fake_label', torch.tensor(target_fake_label))
    self.gan_mode = gan_mode
    if (gan_mode == 'lsgan'):
        self.loss = nn.MSELoss()
    elif (gan_mode == 'vanilla'):
        self.loss = nn.BCEWithLogitsLoss()
    elif (gan_mode in ['wgangp']):
        self.loss = None
    else:
        raise NotImplementedError(('gan mode %s not implemented' % gan_mode))

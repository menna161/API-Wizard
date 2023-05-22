import torch
from torch.nn import functional as F
import util.util as util
from models import networks
from models.shift_net.base_model import BaseModel
import time
import torchvision.transforms as transforms
import os
import numpy as np
from PIL import Image


def initialize(self, opt):
    BaseModel.initialize(self, opt)
    self.opt = opt
    self.isTrain = opt.isTrain
    self.loss_names = ['G_GAN', 'G_L1', 'D', 'style', 'content', 'tv']
    if self.opt.show_flow:
        self.visual_names = ['real_A', 'fake_B', 'real_B', 'flow_srcs']
    else:
        self.visual_names = ['real_A', 'fake_B', 'real_B']
    if self.isTrain:
        self.model_names = ['G', 'D']
    else:
        self.model_names = ['G']
    self.mask_global = torch.zeros(self.opt.batchSize, 1, opt.fineSize, opt.fineSize, dtype=torch.bool)
    self.mask_global.zero_()
    self.mask_global[(:, :, (int((self.opt.fineSize / 4)) + self.opt.overlap):((int((self.opt.fineSize / 2)) + int((self.opt.fineSize / 4))) - self.opt.overlap), (int((self.opt.fineSize / 4)) + self.opt.overlap):((int((self.opt.fineSize / 2)) + int((self.opt.fineSize / 4))) - self.opt.overlap))] = 1
    if (len(opt.gpu_ids) > 0):
        self.use_gpu = True
        self.mask_global = self.mask_global.to(self.device)
    if opt.add_mask2input:
        input_nc = (opt.input_nc + 1)
    else:
        input_nc = opt.input_nc
    (self.netG, self.ng_innerCos_list, self.ng_shift_list) = networks.define_G(input_nc, opt.output_nc, opt.ngf, opt.which_model_netG, opt, self.mask_global, opt.norm, opt.use_spectral_norm_G, opt.init_type, self.gpu_ids, opt.init_gain)
    if self.isTrain:
        use_sigmoid = False
        if (opt.gan_type == 'vanilla'):
            use_sigmoid = True
        self.netD = networks.define_D(opt.input_nc, opt.ndf, opt.which_model_netD, opt.n_layers_D, opt.norm, use_sigmoid, opt.use_spectral_norm_D, opt.init_type, self.gpu_ids, opt.init_gain)
    self.vgg16_extractor = util.VGG16FeatureExtractor()
    if (len(opt.gpu_ids) > 0):
        self.vgg16_extractor = self.vgg16_extractor.to(self.gpu_ids[0])
        self.vgg16_extractor = torch.nn.DataParallel(self.vgg16_extractor, self.gpu_ids)
    if self.isTrain:
        self.old_lr = opt.lr
        self.criterionGAN = networks.GANLoss(gan_type=opt.gan_type).to(self.device)
        self.criterionL1 = torch.nn.L1Loss()
        self.criterionL1_mask = networks.Discounted_L1(opt).to(self.device)
        self.criterionL2_style_loss = torch.nn.MSELoss()
        self.criterionL2_content_loss = torch.nn.MSELoss()
        self.tv_criterion = networks.TVLoss(self.opt.tv_weight)
        self.schedulers = []
        self.optimizers = []
        if (self.opt.gan_type == 'wgan_gp'):
            opt.beta1 = 0
            self.optimizer_G = torch.optim.Adam(self.netG.parameters(), lr=opt.lr, betas=(opt.beta1, 0.9))
            self.optimizer_D = torch.optim.Adam(self.netD.parameters(), lr=opt.lr, betas=(opt.beta1, 0.9))
        else:
            self.optimizer_G = torch.optim.Adam(self.netG.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
            self.optimizer_D = torch.optim.Adam(self.netD.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
        self.optimizers.append(self.optimizer_G)
        self.optimizers.append(self.optimizer_D)
        for optimizer in self.optimizers:
            self.schedulers.append(networks.get_scheduler(optimizer, opt))
    if ((not self.isTrain) or opt.continue_train):
        self.load_networks(opt.which_epoch)
    self.print_networks(opt.verbose)

import torch
import itertools
from .base_model import BaseModel
from . import networks
from . import vgg
import torch.nn.functional as F
import numpy as np
import skimage.measure as measure
import code
import torchvision.transforms as transforms


def __init__(self, opt):
    'Initialize the CycleGAN class.\n\n        Parameters:\n            opt (Option class)-- stores all the experiment flags; needs to be a subclass of BaseOptions\n        '
    BaseModel.__init__(self, opt)
    torch.nn.Module.__init__(self)
    self.loss_names = ['idt_T', 'res', 'MP', 'G', 'T', 'idt_R', 'R']
    if self.isTrain:
        self.visual_names = ['fake_Ts', 'fake_Rs']
    else:
        self.visual_names = ['fake_Ts', 'real_T', 'real_I', 'fake_Rs']
    if self.isTrain:
        self.model_names = ['G_T', 'G_R', 'D']
    else:
        self.model_names = ['G_T', 'G_R']
    self.vgg = vgg.Vgg19(requires_grad=False).to(self.device)
    self.netG_T = networks.define_G((opt.input_nc * 3), opt.input_nc, opt.ngf, opt.netG, opt.norm, (not opt.no_dropout), opt.init_type, opt.init_gain, self.gpu_ids)
    self.netG_R = networks.define_G((opt.input_nc * 3), opt.output_nc, opt.ngf, opt.netG, opt.norm, (not opt.no_dropout), opt.init_type, opt.init_gain, self.gpu_ids)
    self.netD = networks.define_D(opt.input_nc, opt.ndf, opt.netD, opt.n_layers_D, opt.norm, opt.init_type, opt.init_gain, self.gpu_ids)
    if self.isTrain:
        torch.nn.utils.clip_grad_norm_(self.netG_T.parameters(), 0.25)
        torch.nn.utils.clip_grad_norm_(self.netG_R.parameters(), 0.25)
        self.criterionGAN = networks.GANLoss(opt.gan_mode).to(self.device)
        self.criterionGradient = torch.nn.L1Loss()
        self.criterionVgg = networks.VGGLoss1(self.device, vgg=self.vgg, normalize=False)
        self.optimizer_G = torch.optim.Adam(itertools.chain(self.netG_T.parameters(), self.netG_R.parameters()), lr=opt.lr, betas=(opt.beta1, 0.999))
        self.optimizer_D = torch.optim.Adam(itertools.chain(self.netD.parameters()), lr=opt.lr, betas=(opt.beta1, 0.999))
        self.optimizers.append(self.optimizer_G)
        self.optimizers.append(self.optimizer_D)
    self.criterionIdt = torch.nn.MSELoss()
    resSize = 64
    self.k_sz = np.linspace(opt.batch_size, self.opt.blurKernel, 80)
    self.t_h = torch.zeros(opt.batch_size, (opt.ngf * 4), resSize, resSize).to(self.device)
    self.t_c = torch.zeros(opt.batch_size, (opt.ngf * 4), resSize, resSize).to(self.device)
    self.r_h = torch.zeros(opt.batch_size, (opt.ngf * 4), resSize, resSize).to(self.device)
    self.r_c = torch.zeros(opt.batch_size, (opt.ngf * 4), resSize, resSize).to(self.device)
    self.fake_T = torch.zeros(self.opt.batch_size, 3, 256, 256).to(self.device)
    self.fake_Ts = [self.fake_T]
    self.trainFlag = True
    " We use both real-world data and synthetic data. If 'self.isNatural' is True, the data loaded is real-world\n        image paris. Otherwise, we use 'self.syn' to synthesize data."
    self.isNatural = False
    self.syn = networks.SynData(self.device)
    self.real_I = None
    self.real_T = None
    self.real_T2 = None
    self.real_T4 = None
    self.alpha = None

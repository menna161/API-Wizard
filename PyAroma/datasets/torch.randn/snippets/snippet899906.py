import os
import torch.optim as optim
import torch.autograd as autograd
import torch
import numpy as np
from tqdm import tqdm
from tensorboardX import SummaryWriter
from networks import get_network
from util.utils import TrainClock, cycle


def train(self, dataloader):
    'training process'
    data = cycle(dataloader)
    one = torch.FloatTensor([1])
    mone = (one * (- 1))
    one = one.cuda()
    mone = mone.cuda()
    pbar = tqdm(range(self.n_iters))
    for iteration in pbar:
        for p in self.netD.parameters():
            p.requires_grad = True
        for iter_d in range(self.critic_iters):
            real_data = next(data)
            real_data = real_data.cuda()
            real_data.requires_grad_(True)
            self.netD.zero_grad()
            D_real = self.netD(real_data)
            D_real = D_real.mean()
            D_real.backward(mone)
            noise = torch.randn(self.batch_size, self.n_dim)
            noise = noise.cuda()
            fake = self.netG(noise).detach()
            inputv = fake
            D_fake = self.netD(inputv)
            D_fake = D_fake.mean()
            D_fake.backward(one)
            gradient_penalty = self.calc_gradient_penalty(self.netD, real_data, fake.data)
            gradient_penalty.backward()
            D_cost = ((D_fake - D_real) + gradient_penalty)
            Wasserstein_D = (D_real - D_fake)
            self.optimizerD.step()
        for p in self.netD.parameters():
            p.requires_grad = False
        self.netG.zero_grad()
        noise = torch.randn(self.batch_size, self.n_dim)
        noise = noise.cuda()
        noise.requires_grad_(True)
        fake = self.netG(noise)
        G = self.netD(fake)
        G = G.mean()
        G.backward(mone)
        G_cost = (- G)
        self.optimizerG.step()
        pbar.set_postfix({'D_loss': D_cost.item(), 'G_loss': G_cost.item()})
        self.train_tb.add_scalars('loss', {'D_loss': D_cost.item(), 'G_loss': G_cost.item()}, global_step=iteration)
        self.train_tb.add_scalar('wasserstein distance', Wasserstein_D.item(), global_step=iteration)
        self.clock.tick()
        if ((self.clock.step % self.save_frequency) == 0):
            self.save_ckpt()

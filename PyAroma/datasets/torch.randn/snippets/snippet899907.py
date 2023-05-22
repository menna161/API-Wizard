import os
import torch.optim as optim
import torch.autograd as autograd
import torch
import numpy as np
from tqdm import tqdm
from tensorboardX import SummaryWriter
from networks import get_network
from util.utils import TrainClock, cycle


def generate(self, n_samples):
    'generate samples'
    self.eval()
    chunk_num = (n_samples // self.batch_size)
    generated_z = []
    for i in range(chunk_num):
        noise = torch.randn(self.batch_size, self.n_dim).cuda()
        with torch.no_grad():
            fake = self.netG(noise).detach().cpu().numpy()
        generated_z.append(fake)
        print('chunk {} finished.'.format(i))
    remains = (n_samples - (self.batch_size * chunk_num))
    noise = torch.randn(remains, self.n_dim).cuda()
    with torch.no_grad():
        fake = self.netG(noise).detach().cpu().numpy()
    generated_z.append(fake)
    generated_z = np.concatenate(generated_z, axis=0)
    return generated_z

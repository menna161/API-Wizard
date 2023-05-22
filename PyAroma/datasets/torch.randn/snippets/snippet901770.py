from __future__ import print_function
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torch import nn, optim
from torch.nn import functional as F
from torchvision import datasets, transforms
from torchvision.utils import save_image


def run():
    for epoch in range(1, (args.epochs + 1)):
        train(epoch)
        test(epoch)
        sample = Variable(torch.randn(64, 200))
        if args.cuda:
            sample = sample.cuda()
        sample = model.decode(sample).cpu()
        save_image(sample.data.view(64, 1, 28, 28), (('results/sample_' + str(epoch)) + '.png'))

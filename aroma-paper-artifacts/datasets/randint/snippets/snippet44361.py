import argparse
import os
import random
import shutil
import time
import warnings
import sys
import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import models_lpf
import models_fconv_lpf
import torchvision.models as models
import resnet_fconv
import vgg_fconv
from IPython import embed
import matplotlib.pyplot as plt
import os
import models_lpf.resnet
import models_fconv_lpf.resnet
import models_lpf.vgg
import models_fconv_lpf.vgg


def validate_shift(val_loader, model, args):
    batch_time = AverageMeter()
    consist = AverageMeter()
    model.eval()
    with torch.no_grad():
        end = time.time()
        for ep in range(args.epochs_shift):
            for (i, (input, target)) in enumerate(val_loader):
                if (args.gpu is not None):
                    input = input.cuda(args.gpu, non_blocking=True)
                target = target.cuda(args.gpu, non_blocking=True)
                off0 = np.random.randint((32 + args.shift_inc), size=2)
                off1 = np.random.randint((32 + args.shift_inc), size=2)
                output0 = model(input[(:, :, off0[0]:(off0[0] + 224), off0[1]:(off0[1] + 224))])
                output1 = model(input[(:, :, off1[0]:(off1[0] + 224), off1[1]:(off1[1] + 224))])
                cur_agree = agreement(output0, output1).type(torch.FloatTensor).to(output0.device)
                consist.update(cur_agree.item(), input.size(0))
                batch_time.update((time.time() - end))
                end = time.time()
                if ((i % args.print_freq) == 0):
                    print('Ep [{0}/{1}]:\tTest: [{2}/{3}]\tTime {batch_time.val:.3f} ({batch_time.avg:.3f})\tConsist {consist.val:.4f} ({consist.avg:.4f})\t'.format(ep, args.epochs_shift, i, len(val_loader), batch_time=batch_time, consist=consist))
        print(' * Consistency {consist.avg:.3f}'.format(consist=consist))
    return consist.avg

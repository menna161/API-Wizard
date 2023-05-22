import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F

if (__name__ == '__main__'):
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    ntimes = 100
    model = FastSCNN(4)
    model.cuda()
    model.eval()
    with torch.no_grad():
        x = torch.randn(1, 3, 320, 320)
        x = x.cuda()
        out = model(x)
        start = time.time()
        for i in range(ntimes):
            model(x)
        print('fps is :', (1.0 / ((time.time() - start) / ntimes)))

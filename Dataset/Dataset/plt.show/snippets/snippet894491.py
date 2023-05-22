import torch
from torch.autograd import Variable
import matplotlib.pyplot as plt
import numpy as np


def plot_image(im, batch_idx=0, return_im=False):
    if (im.dim() == 4):
        im = im[(batch_idx, :, :, :)]
    mean = Variable(torch.FloatTensor([0.485, 0.456, 0.406]).view(3, 1, 1))
    std = Variable(torch.FloatTensor([0.229, 0.224, 0.225]).view(3, 1, 1))
    if im.is_cuda:
        mean = mean.cuda()
        std = std.cuda()
    im = (im.mul(std).add(mean) * 255.0)
    im = im.permute(1, 2, 0).data.cpu().numpy().astype(np.uint8)
    if return_im:
        return im
    plt.imshow(im)
    plt.show()

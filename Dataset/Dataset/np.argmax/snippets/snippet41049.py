from __future__ import print_function
from six.moves import range
from PIL import Image
import torch.backends.cudnn as cudnn
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import os
import time
import numpy as np
import torchfile
from miscc.config import cfg
from miscc.utils import mkdir_p
from miscc.utils import weights_init
from miscc.utils import save_img_results, save_model
from miscc.utils import compute_discriminator_loss, compute_generator_loss
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from miscc.utils import load_validation_data
from tensorboard import summary
from tensorboard import FileWriter
from model import STAGE1_G, STAGE1_D
from PIL import Image, ImageDraw, ImageFont
import cPickle as pickle
import torchvision
import torchvision.utils as vutils


def sample(self, data_loader, num_samples=25, draw_bbox=True, max_objects=4):
    from PIL import Image, ImageDraw, ImageFont
    import cPickle as pickle
    import torchvision
    import torchvision.utils as vutils
    (netG, _) = self.load_network_stageI()
    netG.eval()
    save_dir = (((cfg.NET_G[:cfg.NET_G.find('.pth')] + '_samples_') + str(max_objects)) + '_objects')
    print('saving to:', save_dir)
    mkdir_p(save_dir)
    nz = cfg.Z_DIM
    noise = Variable(torch.FloatTensor(9, nz))
    if cfg.CUDA:
        noise = noise.cuda()
    imsize = 64
    count = 0
    for (i, data) in enumerate(data_loader, 0):
        if (count == num_samples):
            break
        (real_img_cpu, transformation_matrices, label_one_hot, bbox) = data
        (transf_matrices, transf_matrices_inv) = tuple(transformation_matrices)
        transf_matrices_inv = transf_matrices_inv.detach()
        real_img = Variable(real_img_cpu)
        if cfg.CUDA:
            real_img = real_img.cuda()
            label_one_hot = label_one_hot.cuda()
            transf_matrices_inv = transf_matrices_inv.cuda()
        transf_matrices_inv_batch = transf_matrices_inv.view(1, max_objects, 2, 3).repeat(9, 1, 1, 1)
        label_one_hot_batch = label_one_hot.view(1, max_objects, 13).repeat(9, 1, 1)
        noise.data.normal_(0, 1)
        inputs = (noise, transf_matrices_inv_batch, label_one_hot_batch)
        with torch.no_grad():
            fake_imgs = nn.parallel.data_parallel(netG, inputs, self.gpus)
        data_img = torch.FloatTensor(20, 3, imsize, imsize).fill_(0)
        data_img[0] = real_img
        data_img[1:10] = fake_imgs
        if draw_bbox:
            for idx in range(max_objects):
                (x, y, w, h) = tuple([int((imsize * x)) for x in bbox[(0, idx)]])
                w = ((imsize - 1) if (w > (imsize - 1)) else w)
                h = ((imsize - 1) if (h > (imsize - 1)) else h)
                if ((x <= (- 1)) or (y <= (- 1))):
                    break
                data_img[(:10, :, y, x:(x + w))] = 1
                data_img[(:10, :, y:(y + h), x)] = 1
                data_img[(:10, :, (y + h), x:(x + w))] = 1
                data_img[(:10, :, y:(y + h), (x + w))] = 1
        shape_dict = {0: 'cube', 1: 'cylinder', 2: 'sphere', 3: 'empty'}
        color_dict = {0: 'gray', 1: 'red', 2: 'blue', 3: 'green', 4: 'brown', 5: 'purple', 6: 'cyan', 7: 'yellow', 8: 'empty'}
        text_img = Image.new('L', ((imsize * 10), imsize), color='white')
        d = ImageDraw.Draw(text_img)
        label = label_one_hot_batch[0]
        label = label.cpu().numpy()
        label_shape = label[(:, :4)]
        label_color = label[(:, 4:)]
        label_shape = np.argmax(label_shape, axis=1)
        label_color = np.argmax(label_color, axis=1)
        label_combined = ', '.join([((color_dict[label_color[_]] + ' ') + shape_dict[label_shape[_]]) for _ in range(max_objects)])
        d.text((10, 10), label_combined)
        text_img = torchvision.transforms.functional.to_tensor(text_img)
        text_img = torch.chunk(text_img, 10, 2)
        text_img = torch.cat([text_img[i].view(1, 1, imsize, imsize) for i in range(10)], 0)
        data_img[10:] = text_img
        vutils.save_image(data_img, '{}/vis_{}.png'.format(save_dir, count), normalize=True, nrow=10)
        count += 1
    print('Saved {} files to {}'.format(count, save_dir))

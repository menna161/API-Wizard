from __future__ import division
from tools.model import load_model
from config.configs_kf import *
from lib.utils.visual import *
import torchvision.transforms as st
from sklearn.metrics import confusion_matrix
import numpy as np
from tqdm import tqdm_notebook as tqdm
from tools.ckpt import *
import time
import itertools


def fusion_prediction(nets, image, scales, batch_size=1, num_class=7, wsize=(512, 512)):
    pred_all = np.zeros((image.shape[:2] + (num_class,)))
    for scale_rate in scales:
        img = image.copy()
        img = scale(img, scale_rate)
        pred = np.zeros((img.shape[:2] + (num_class,)))
        stride = img.shape[1]
        window_size = img.shape[:2]
        total = (count_sliding_window(img, step=stride, window_size=wsize) // batch_size)
        for (i, coords) in enumerate(tqdm(grouper(batch_size, sliding_window(img, step=stride, window_size=window_size)), total=total, leave=False)):
            image_patches = [np.copy(img[(x:(x + w), y:(y + h))]).transpose((2, 0, 1)) for (x, y, w, h) in coords]
            imgs_flip = [patch[(:, ::(- 1), :)] for patch in image_patches]
            imgs_mirror = [patch[(:, :, ::(- 1))] for patch in image_patches]
            image_patches = np.concatenate((image_patches, imgs_flip, imgs_mirror), axis=0)
            image_patches = np.asarray(image_patches)
            image_patches = torch.from_numpy(image_patches).cuda()
            for net in nets:
                outs = net(image_patches)
                outs = outs.data.cpu().numpy()
                (b, _, _, _) = outs.shape
                for (out, (x, y, w, h)) in zip(outs[(0:(b // 3), :, :, :)], coords):
                    out = out.transpose((1, 2, 0))
                    pred[(x:(x + w), y:(y + h))] += out
                for (out, (x, y, w, h)) in zip(outs[((b // 3):((2 * b) // 3), :, :, :)], coords):
                    out = out[(:, ::(- 1), :)]
                    out = out.transpose((1, 2, 0))
                    pred[(x:(x + w), y:(y + h))] += out
                for (out, (x, y, w, h)) in zip(outs[(((2 * b) // 3):b, :, :, :)], coords):
                    out = out[(:, :, ::(- 1))]
                    out = out.transpose((1, 2, 0))
                    pred[(x:(x + w), y:(y + h))] += out
                del outs
        pred_all += scale(pred, (1.0 / scale_rate))
    return pred_all

from IPython import embed
import argparse
import itertools
from operator import itemgetter
import os
import re
import time
from PIL import Image
from tensorboardX import SummaryWriter
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, transforms, utils
import tqdm
import wandb
from baseline import PixelCNN
from layers import PONO
from masking import *
from model import OurPixelCNN
from utils import *
from apex import amp
from celeba_data import get_celeba_dataloader


def sample(model, generation_idx, mask_init, mask_undilated, mask_dilated, batch_to_complete, obs):
    model.eval()
    if (args.sample_region == 'full'):
        data = torch.zeros(sample_batch_size, obs[0], obs[1], obs[2])
        data = data.cuda()
        sample_idx = generation_idx
        context = None
        batch_to_complete = None
    else:
        if (args.sample_region == 'center'):
            offset1 = ((- args.sample_size_h) // 2)
            offset2 = ((- args.sample_size_w) // 2)
        elif (args.sample_region == 'random_near_center'):
            offset1 = int(np.random.randint(((- obs[1]) // 4), (obs[1] // 4)))
            offset2 = int(np.random.randint(((- obs[2]) // 4), (obs[2] // 4)))
        elif (args.sample_region == 'top'):
            offset1 = (- (obs[1] // 2))
            offset2 = (- (obs[2] // 2))
        elif (args.sample_region == 'custom'):
            assert ((args.sample_offset1 is not None) and (args.sample_offset2 is not None))
            offset1 = args.sample_offset1
            offset2 = args.sample_offset2
        else:
            raise NotImplementedError(f'Unknown sampling region {args.sample_region}')
        sample_region = set()
        for i in range(((obs[1] // 2) + offset1), (((obs[1] // 2) + offset1) + args.sample_size_h)):
            for j in range(((obs[2] // 2) + offset2), (((obs[2] // 2) + offset2) + args.sample_size_w)):
                sample_region.add((i, j))
        sample_idx = []
        num_added = 0
        for (i, j) in generation_idx:
            if ((i, j) in sample_region):
                sample_idx.append([i, j])
                num_added += 1
        sample_idx = np.array(sample_idx, dtype=np.int)
        logger.info(f'Sample idx {sample_idx}')
        data = batch_to_complete.clone().cuda()
        print('batch_to_complete', type(batch_to_complete), batch_to_complete.shape, 'data', type(data), data.shape)
        data[(:, :, sample_idx[(:, 0)], sample_idx[(:, 1)])] = 0
        context = rescaling_inv(data).cpu()
        batch_to_complete = rescaling_inv(batch_to_complete).cpu()
        logger.info(f'Example context: {context.numpy()}')
    logger.info(f'Before sampling, data has range {data.min().item()}-{data.max().item()} (mean {data.mean().item()}), dtype={data.dtype} {type(data)}')
    for (n_pix, (i, j)) in enumerate(tqdm.tqdm(sample_idx, desc='Sampling pixels')):
        data_v = Variable(data)
        t1 = time.time()
        out = model(data_v, sample=True, mask_init=mask_init, mask_undilated=mask_undilated, mask_dilated=mask_dilated)
        t2 = time.time()
        out_sample = sample_op(out, i, j)
        if args.sample_quantize:
            out_sample = quantize(out_sample)
        logger.info('%d %d,%d Time to infer logits=%f s, sample=%f s', n_pix, i, j, (t2 - t1), (time.time() - t2))
        data[(:, :, i, j)] = out_sample
        logger.info(f'Sampled pixel {i},{j}, with batchwise range {out_sample.min().item()}-{out_sample.max().item()} (mean {out_sample.mean().item()}), dtype={out_sample.dtype} {type(out_sample)}')
        if (((n_pix <= 256) and ((n_pix % 32) == 0)) or ((n_pix % 256) == 0)):
            sample_save_path = os.path.join(run_dir, f"{args.mode}_{args.sample_region}_{args.sample_size_h}x{args.sample_size_w}_o1{args.sample_offset1}_o2{args.sample_offset2}_obs{obs2str(obs)}_ep{checkpoint_epochs}_order{sample_order_i}_{n_pix}of{len(sample_idx)}pix{('_quantize' if args.sample_quantize else '')}.png")
            utils.save_image(rescaling_inv(data), sample_save_path, nrow=4, padding=5, pad_value=1, scale_each=False)
            if (not args.disable_wandb):
                wandb.log({sample_save_path: wandb.Image(sample_save_path)}, step=n_pix)
    data = rescaling_inv(data).cpu()
    if ((batch_to_complete is not None) and (context is not None)):
        difference = torch.abs((data - batch_to_complete))
        logger.info(f'Context range {context.min()}-{context.max()}. Data range {data.min()}-{data.max()}. batch_to_complete range {batch_to_complete.min()}-{batch_to_complete.max()}')
        data = torch.stack([context, data, batch_to_complete, difference], dim=1).view((- 1), *data.shape[1:])
    return data

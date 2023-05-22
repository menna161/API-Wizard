import sys
import os
from os import path, makedirs, listdir
import numpy as np
import random
import torch
from torch import nn
from torch.autograd import Variable
from zoo.models import SeResNext50_9ch_Unet
import timeit
import cv2
import pandas as pd
from tqdm import tqdm
from utils import preprocess_inputs, parse_img_id

if (__name__ == '__main__'):
    t0 = timeit.default_timer()
    fold = int(sys.argv[1])
    vis_dev = str(fold)
    if (fold > 3):
        vis_dev = str((fold - 4))
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = vis_dev
    val_files = df[(df['fold'] == fold)]['id'].values
    pred_folder = '/wdata/pred_50_9ch_oof_0'
    makedirs(pred_folder, exist_ok=True)
    snapshot_name = 'res50_9ch_fold_{0}_best_0'.format(fold)
    model = nn.DataParallel(SeResNext50_9ch_Unet()).cuda()
    checkpoint = torch.load(path.join(models_folder, snapshot_name))
    model.load_state_dict(checkpoint['state_dict'])
    print("loaded checkpoint '{}' (epoch {}, dice {})".format(snapshot_name, checkpoint['epoch'], checkpoint['best_score']))
    model.eval()
    other_outputs = []
    with torch.no_grad():
        for f in tqdm(val_files):
            f = (f + '.png')
            img = cv2.imread(path.join(test_dir, f), cv2.IMREAD_COLOR)
            img2 = cv2.imread(path.join(test_dir2, f), cv2.IMREAD_COLOR)
            img3 = cv2.imread(path.join(test_dir3, f), cv2.IMREAD_COLOR)
            img = np.concatenate([img, img2, img3], axis=2)
            img = cv2.copyMakeBorder(img, 14, 14, 14, 14, cv2.BORDER_REFLECT_101)
            inp = []
            inp.append(img)
            inp = np.asarray(inp, dtype='float')
            inp = preprocess_inputs(inp)
            inp = torch.from_numpy(inp.transpose((0, 3, 1, 2))).float()
            inp = Variable(inp).cuda()
            (nadir, cat_inp, coord_inp) = parse_img_id(f)
            nadir = torch.from_numpy(np.asarray([(nadir / 60.0)]).copy()).float()
            cat_inp = torch.from_numpy(cat_inp.copy()[(np.newaxis, ...)]).float()
            coord_inp = torch.from_numpy(coord_inp.copy()[(np.newaxis, ...)]).float()
            (msk, _) = model(inp, nadir, cat_inp, coord_inp)
            msk = torch.sigmoid(msk)
            msk = msk.cpu().numpy()
            msk = msk[0]
            msk = (msk * 255)
            msk = msk.astype('uint8')
            msk = np.rollaxis(msk, 0, 3)
            msk = msk[(14:(- 14), 14:(- 14), ...)]
            cv2.imwrite(path.join(pred_folder, f), msk[(..., :3)], [cv2.IMWRITE_PNG_COMPRESSION, 9])
    elapsed = (timeit.default_timer() - t0)
    print('Time: {:.3f} min'.format((elapsed / 60)))

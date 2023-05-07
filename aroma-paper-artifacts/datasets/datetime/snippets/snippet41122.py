from __future__ import print_function
from miscc.config import cfg, cfg_from_file
from datasets import TextDataset
from trainer import condGANTrainer as trainer
import os
import sys
import time
import random
import pprint
import datetime
import dateutil.tz
import argparse
import numpy as np
from shutil import copyfile
import torch
import torchvision.transforms as transforms
from nltk.tokenize import RegexpTokenizer

if (__name__ == '__main__'):
    args = parse_args()
    if (args.cfg_file is not None):
        cfg_from_file(args.cfg_file)
    if (args.gpu_id != (- 1)):
        cfg.GPU_ID = args.gpu_id
    else:
        cfg.CUDA = False
    if (args.data_dir != ''):
        cfg.DATA_DIR = args.data_dir
    print('Using config:')
    pprint.pprint(cfg)
    if (args.manualSeed is None):
        args.manualSeed = random.randint(1, 10000)
    random.seed(args.manualSeed)
    np.random.seed(args.manualSeed)
    torch.manual_seed(args.manualSeed)
    if cfg.CUDA:
        torch.cuda.manual_seed_all(args.manualSeed)
    if (args.resume == ''):
        resume = False
        now = datetime.datetime.now(dateutil.tz.tzlocal())
        timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
        output_dir = ('../../../output/%s_%s_%s' % (cfg.DATASET_NAME, cfg.CONFIG_NAME, timestamp))
    else:
        assert os.path.isdir(args.resume)
        resume = True
        output_dir = args.resume
    (split_dir, bshuffle) = ('train', True)
    eval = False
    if (not cfg.TRAIN.FLAG):
        split_dir = 'test'
        eval = True
    imsize = (cfg.TREE.BASE_SIZE * (2 ** (cfg.TREE.BRANCH_NUM - 1)))
    image_transform = transforms.Compose([transforms.Resize((268, 268)), transforms.ToTensor()])
    dataset = TextDataset(cfg.DATA_DIR, cfg.IMG_DIR, split_dir, base_size=cfg.TREE.BASE_SIZE, transform=image_transform, eval=eval)
    assert dataset
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=cfg.TRAIN.BATCH_SIZE, drop_last=True, shuffle=bshuffle, num_workers=int(cfg.WORKERS))
    algo = trainer(output_dir, dataloader, dataset.n_words, dataset.ixtoword, resume)
    start_t = time.time()
    if cfg.TRAIN.FLAG:
        if (not resume):
            copyfile(sys.argv[0], ((output_dir + '/') + sys.argv[0]))
            copyfile('trainer.py', ((output_dir + '/') + 'trainer.py'))
            copyfile('model.py', ((output_dir + '/') + 'model.py'))
            copyfile('miscc/utils.py', ((output_dir + '/') + 'utils.py'))
            copyfile('miscc/losses.py', ((output_dir + '/') + 'losses.py'))
            copyfile('datasets.py', ((output_dir + '/') + 'datasets.py'))
            copyfile(args.cfg_file, ((output_dir + '/') + 'cfg_file.yml'))
        algo.train()
    else:
        'generate images from pre-extracted embeddings'
        if cfg.B_VALIDATION:
            algo.sample(split_dir, num_samples=25, draw_bbox=True)
        else:
            gen_example(dataset.wordtoix, algo, num_samples=30000)
    end_t = time.time()

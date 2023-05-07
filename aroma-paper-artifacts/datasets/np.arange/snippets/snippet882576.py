import argparse
import numpy as np
import torch
import torch.nn as nn
import os
from tqdm import tqdm
from lm import LM
import utils


def train(args):
    word_dict = utils.get_lm_dict(args.train_file)
    word_size = len(word_dict)
    x_train = utils.lm_data(args.train_file, word_dict)
    x_dev = utils.lm_data(args.dev_file, word_dict)
    model = LM(word_size, args.word_dim, args.hidden_dim)
    model.cuda()
    optimizer = torch.optim.Adagrad(model.parameters(), lr=0.1, initial_accumulator_value=0.1)
    best_loss = 1000
    if os.path.exists(args.model_file):
        best_point = torch.load(args.model_file)
        model.load_state_dict(best_point['state_dict'])
        optimizer.load_state_dict(best_point['optimizer'])
    eval_count = args.eval_every
    stop_count = args.stop_after
    for epoch in range(args.num_epoch):
        if (stop_count <= 0):
            break
        shuffle_indices = np.random.permutation(np.arange(len(x_train)))
        x_shuffle = np.array(x_train)[shuffle_indices]
        losses = []
        train_iterator = tqdm(range(0, len(x_shuffle), args.batch_size))
        for i in train_iterator:
            if (stop_count <= 0):
                train_iterator.close()
                break
            model.train()
            (x_batch, x_mask) = utils.pad(x_shuffle[i:(i + args.batch_size)])
            x_batch = torch.tensor(x_batch).cuda()
            x_mask = torch.tensor(x_mask).float().cuda()
            batch_loss = model(x_batch, x_mask)
            losses.append(batch_loss.item())
            batch_loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 3)
            optimizer.step()
            optimizer.zero_grad()
            eval_count -= len(x_batch)
            if (eval_count <= 0):
                with torch.no_grad():
                    shuffle_indices = np.random.permutation(np.arange(len(x_dev)))[:2000]
                    x_dev = np.array(x_dev)[shuffle_indices]
                    train_loss = np.mean(losses)
                    dev_loss = []
                    for j in tqdm(range(0, len(x_dev), args.batch_size)):
                        model.eval()
                        (x_batch, x_mask) = utils.pad(x_dev[j:(j + args.batch_size)])
                        x_batch = torch.tensor(x_batch).cuda()
                        x_mask = torch.tensor(x_mask).float().cuda()
                        batch_loss = model(x_batch, x_mask)
                        dev_loss.append(batch_loss.item())
                    dev_loss = np.mean(dev_loss)
                    if (best_loss >= dev_loss):
                        best_loss = dev_loss
                        stop_count = args.stop_after
                        torch.save({'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}, args.model_file)
                    else:
                        stop_count -= 1
                    tqdm.write(('Epoch: %d, Batch: %d, Train Loss: %.4f, Dev Loss: %.4f' % (epoch, i, train_loss, dev_loss)))
                    losses = []
                    eval_count = args.eval_every

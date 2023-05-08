import os
import sys
from datetime import datetime
from lib.config import cfg
from lib.utils import Timer, has_nan
import torch
from torch.optim import SGD, Adam, lr_scheduler
from torch.autograd import Variable


def train(self, train_loader, val_loader=None):
    ' Given data queues, train the network '
    save_dir = os.path.join(cfg.DIR.OUT_PATH)
    if (not os.path.exists(save_dir)):
        os.makedirs(save_dir)
    train_timer = Timer()
    data_timer = Timer()
    training_losses = []
    lr_steps = [int(k) for k in cfg.TRAIN.LEARNING_RATES.keys()]
    self.lr_scheduler = lr_scheduler.MultiStepLR(self.optimizer, lr_steps, gamma=0.1)
    start_iter = 0
    if cfg.TRAIN.RESUME_TRAIN:
        self.load(cfg.CONST.WEIGHTS)
        start_iter = cfg.TRAIN.INITIAL_ITERATION
    train_loader_iter = iter(train_loader)
    for train_ind in range(start_iter, (cfg.TRAIN.NUM_ITERATION + 1)):
        self.lr_scheduler.step()
        data_timer.tic()
        try:
            (batch_img, batch_voxel) = train_loader_iter.next()
        except StopIteration:
            train_loader_iter = iter(train_loader)
            (batch_img, batch_voxel) = train_loader_iter.next()
        data_timer.toc()
        if self.net.is_x_tensor4:
            batch_img = batch_img[0]
        train_timer.tic()
        loss = self.train_loss(batch_img, batch_voxel)
        train_timer.toc()
        training_losses.append(loss.item())
        if (train_ind in lr_steps):
            print(('Learing rate decreased to %f: ' % cfg.TRAIN.LEARNING_RATES[str(train_ind)]))
        if ((train_ind % cfg.TRAIN.PRINT_FREQ) == 0):
            print(('%s Iter: %d Loss: %f' % (datetime.now(), train_ind, loss)))
        if (((train_ind % cfg.TRAIN.VALIDATION_FREQ) == 0) and (val_loader is not None)):
            val_losses = 0
            val_num_iter = min(cfg.TRAIN.NUM_VALIDATION_ITERATIONS, len(val_loader))
            val_loader_iter = iter(val_loader)
            for i in range(val_num_iter):
                (batch_img, batch_voxel) = val_loader_iter.next()
                val_loss = self.train_loss(batch_img, batch_voxel)
                val_losses += val_loss
            var_losses_mean = (val_losses / val_num_iter)
            print(('%s Test loss: %f' % (datetime.now(), var_losses_mean)))
        if ((train_ind % cfg.TRAIN.NAN_CHECK_FREQ) == 0):
            nan_or_max_param = max_or_nan(self.net.parameters())
            if has_nan(nan_or_max_param):
                print('NAN detected')
                break
        if ((((train_ind % cfg.TRAIN.SAVE_FREQ) == 0) and (not (train_ind == 0))) or (train_ind == cfg.TRAIN.NUM_ITERATION)):
            self.save(training_losses, save_dir, train_ind)
        if (loss.item() > cfg.TRAIN.LOSS_LIMIT):
            print('Cost exceeds the threshold. Stop training')
            break

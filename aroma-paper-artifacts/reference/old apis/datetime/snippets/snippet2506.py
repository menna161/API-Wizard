import os
import sys
import theano
import theano.tensor as T
import numpy as np
from datetime import datetime
from lib.config import cfg
from lib.utils import Timer


def train(self, train_queue, val_queue=None):
    ' Given data queues, train the network '
    save_dir = os.path.join(cfg.DIR.OUT_PATH)
    if (not os.path.exists(save_dir)):
        os.makedirs(save_dir)
    train_timer = Timer()
    data_timer = Timer()
    training_losses = []
    start_iter = 0
    if cfg.TRAIN.RESUME_TRAIN:
        self.net.load(cfg.CONST.WEIGHTS)
        start_iter = cfg.TRAIN.INITIAL_ITERATION
    lr = cfg.TRAIN.DEFAULT_LEARNING_RATE
    lr_steps = [int(k) for k in cfg.TRAIN.LEARNING_RATES.keys()]
    print(('Set the learning rate to %f.' % lr))
    self.set_lr(lr)
    for train_ind in range(start_iter, (cfg.TRAIN.NUM_ITERATION + 1)):
        data_timer.tic()
        (batch_img, batch_voxel) = train_queue.get()
        data_timer.toc()
        if self.net.is_x_tensor4:
            batch_img = batch_img[0]
        train_timer.tic()
        loss = self.train_loss(batch_img, batch_voxel)
        train_timer.toc()
        training_losses.append(loss)
        if (train_ind in lr_steps):
            self.set_lr(np.float(cfg.TRAIN.LEARNING_RATES[str(train_ind)]))
            print(('Learing rate decreased to %f: ' % self.lr.get_value()))
        if ((train_ind % cfg.TRAIN.PRINT_FREQ) == 0):
            print(('%s Iter: %d Loss: %f' % (datetime.now(), train_ind, loss)))
        if (((train_ind % cfg.TRAIN.VALIDATION_FREQ) == 0) and (val_queue is not None)):
            val_losses = []
            for i in range(cfg.TRAIN.NUM_VALIDATION_ITERATIONS):
                (batch_img, batch_voxel) = val_queue.get()
                (_, val_loss, _) = self.test_output(batch_img, batch_voxel)
                val_losses.append(val_loss)
            print(('%s Test loss: %f' % (datetime.now(), np.mean(val_losses))))
        if ((train_ind % cfg.TRAIN.NAN_CHECK_FREQ) == 0):
            max_param = max_or_nan(self.net.params)
            if np.isnan(max_param):
                print('NAN detected')
                break
        if (((train_ind % cfg.TRAIN.SAVE_FREQ) == 0) and (not (train_ind == 0))):
            self.save(training_losses, save_dir, train_ind)
        if (loss > cfg.TRAIN.LOSS_LIMIT):
            print('Cost exceeds the threshold. Stop training')
            break

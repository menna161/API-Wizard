from __future__ import division
import os
import time
from shutil import copyfile
from glob import glob
import tensorflow as tf
import numpy as np
import config
from collections import namedtuple
from module import *
from utils import *
from ops import *
from metrics import *


def train(self, args):
    self.lr = tf.placeholder(tf.float32, None, name='learning_rate')
    if (self.model == 'base'):
        self.d_optim = tf.train.AdamOptimizer(self.lr, beta1=args.beta1).minimize(self.d_loss, var_list=self.d_vars)
    else:
        self.d_optim = tf.train.AdamOptimizer(self.lr, beta1=args.beta1).minimize(self.D_loss, var_list=self.d_vars)
    self.g_optim = tf.train.AdamOptimizer(self.lr, beta1=args.beta1).minimize(self.g_loss, var_list=self.g_vars)
    init_op = tf.global_variables_initializer()
    self.sess.run(init_op)
    log_dir = './logs/{}2{}_{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d)
    self.writer = tf.summary.FileWriter(log_dir, self.sess.graph)
    dataA = glob('./datasets/{}/train/*.*'.format(self.dataset_A_dir))
    dataB = glob('./datasets/{}/train/*.*'.format(self.dataset_B_dir))
    if (self.model == 'partial'):
        data_mixed = (dataA + dataB)
    if (self.model == 'full'):
        data_mixed = glob('./datasets/JCP_mixed/*.*')
    counter = 1
    start_time = time.time()
    if args.continue_train:
        if self.load(args.checkpoint_dir):
            print(' [*] Load SUCCESS')
        else:
            print(' [!] Load failed...')
    for epoch in range(args.epoch):
        np.random.shuffle(dataA)
        np.random.shuffle(dataB)
        if (self.model != 'base'):
            np.random.shuffle(data_mixed)
        batch_idxs = (min(min(len(dataA), len(dataB)), args.train_size) // self.batch_size)
        lr = (args.lr if (epoch < args.epoch_step) else ((args.lr * (args.epoch - epoch)) / (args.epoch - args.epoch_step)))
        for idx in range(0, batch_idxs):
            batch_files = list(zip(dataA[(idx * self.batch_size):((idx + 1) * self.batch_size)], dataB[(idx * self.batch_size):((idx + 1) * self.batch_size)]))
            batch_images = [load_npy_data(batch_file) for batch_file in batch_files]
            batch_images = np.array(batch_images).astype(np.float32)
            gaussian_noise = np.abs(np.random.normal(0, self.sigma_d, [self.batch_size, self.time_step, self.pitch_range, self.input_c_dim]))
            if (self.model == 'base'):
                (fake_A, fake_B, _, summary_str, g_loss_a2b, g_loss_b2a, cycle_loss, g_loss) = self.sess.run([self.fake_A, self.fake_B, self.g_optim, self.g_sum, self.g_loss_a2b, self.g_loss_b2a, self.cycle_loss, self.g_loss], feed_dict={self.real_data: batch_images, self.gaussian_noise: gaussian_noise, self.lr: lr})
                (_, summary_str, da_loss, db_loss, d_loss) = self.sess.run([self.d_optim, self.d_sum, self.da_loss, self.db_loss, self.d_loss], feed_dict={self.real_data: batch_images, self.fake_A_sample: fake_A, self.fake_B_sample: fake_B, self.lr: lr, self.gaussian_noise: gaussian_noise})
                print('=================================================================')
                print(('Epoch: [%2d] [%4d/%4d] time: %4.4f, d_loss: %6.2f, G_loss: %6.2f' % (epoch, idx, batch_idxs, (time.time() - start_time), d_loss, g_loss)))
                print(('++++++++++G_loss_A2B: %6.2f G_loss_B2A: %6.2f Cycle_loss: %6.2f DA_loss: %6.2f DB_loss: %6.2f' % (g_loss_a2b, g_loss_b2a, cycle_loss, da_loss, db_loss)))
            else:
                batch_files_mixed = data_mixed[(idx * self.batch_size):((idx + 1) * self.batch_size)]
                batch_images_mixed = [(np.load(batch_file) * 1.0) for batch_file in batch_files_mixed]
                batch_images_mixed = np.array(batch_images_mixed).astype(np.float32)
                (fake_A, fake_B, _, summary_str, g_loss_a2b, g_loss_b2a, cycle_loss, g_loss) = self.sess.run([self.fake_A, self.fake_B, self.g_optim, self.g_sum, self.g_loss_a2b, self.g_loss_b2a, self.cycle_loss, self.g_loss], feed_dict={self.real_data: batch_images, self.gaussian_noise: gaussian_noise, self.lr: lr, self.real_mixed: batch_images_mixed})
                self.writer.add_summary(summary_str, counter)
                [fake_A, fake_B] = self.pool([fake_A, fake_B])
                (_, summary_str, da_loss, db_loss, d_loss, da_all_loss, db_all_loss, d_all_loss, D_loss) = self.sess.run([self.d_optim, self.d_sum, self.da_loss, self.db_loss, self.d_loss, self.da_all_loss, self.db_all_loss, self.d_all_loss, self.D_loss], feed_dict={self.real_data: batch_images, self.fake_A_sample: fake_A, self.fake_B_sample: fake_B, self.lr: lr, self.gaussian_noise: gaussian_noise, self.real_mixed: batch_images_mixed})
                self.writer.add_summary(summary_str, counter)
                print('=================================================================')
                print(('Epoch: [%2d] [%4d/%4d] time: %4.4f D_loss: %6.2f, d_loss: %6.2f, d_all_loss: %6.2f, G_loss: %6.2f' % (epoch, idx, batch_idxs, (time.time() - start_time), D_loss, d_loss, d_all_loss, g_loss)))
                print(('++++++++++G_loss_A2B: %6.2f G_loss_B2A: %6.2f Cycle_loss: %6.2f DA_loss: %6.2f DB_loss: %6.2f, DA_all_loss: %6.2f DB_all_loss: %6.2f' % (g_loss_a2b, g_loss_b2a, cycle_loss, da_loss, db_loss, da_all_loss, db_all_loss)))
            counter += 1
            if (np.mod(counter, args.print_freq) == 1):
                sample_dir = os.path.join(self.sample_dir, '{}2{}_{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, self.model, self.sigma_d))
                if (not os.path.exists(sample_dir)):
                    os.makedirs(sample_dir)
                self.sample_model(sample_dir, epoch, idx)
            if (np.mod(counter, batch_idxs) == 1):
                self.save(args.checkpoint_dir, counter)

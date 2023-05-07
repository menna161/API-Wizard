import numpy as np
import tensorflow as tf
from random import shuffle
from collections import namedtuple
from module import *
from ops import *
from utils import *
from glob import glob


def train(self, args):
    self.lr = tf.placeholder(tf.float32, None, name='learning_rate')
    self.d_optim = tf.train.AdamOptimizer(self.lr, beta1=args.beta1).minimize(self.d_loss, var_list=self.d_vars)
    init_op = tf.global_variables_initializer()
    self.sess.run(init_op)
    log_dir = './logs/classifier_{}2{}_{}_{}'.format(self.dataset_A_dir, self.dataset_B_dir, self.now_datetime, str(self.sigma_c))
    self.writer = tf.summary.FileWriter(log_dir, self.sess.graph)
    counter = 1
    dataA = glob('./datasets/{}/train/*.*'.format(self.dataset_A_dir))
    dataB = glob('./datasets/{}/train/*.*'.format(self.dataset_B_dir))
    labelA = [(1.0, 0.0) for _ in range(len(dataA))]
    labelB = [(0.0, 1.0) for _ in range(len(dataB))]
    data_origin = (dataA + dataB)
    label_origin = (labelA + labelB)
    training_list = []
    for pair in zip(data_origin, label_origin):
        training_list.append(pair)
    print('Successfully create training list!')
    dataA = glob('./datasets/{}/test/*.*'.format(self.dataset_A_dir))
    dataB = glob('./datasets/{}/test/*.*'.format(self.dataset_B_dir))
    labelA = [(1.0, 0.0) for _ in range(len(dataA))]
    labelB = [(0.0, 1.0) for _ in range(len(dataB))]
    data_origin = (dataA + dataB)
    label_origin = (labelA + labelB)
    testing_list = []
    for pair in zip(data_origin, label_origin):
        testing_list.append(pair)
    print('Successfully create testing list!')
    data_test = [((np.load(pair[0]) * 2.0) - 1.0) for pair in testing_list]
    data_test = np.array(data_test).astype(np.float32)
    gaussian_noise = np.random.normal(0, self.sigma_c, [data_test.shape[0], data_test.shape[1], data_test.shape[2], data_test.shape[3]])
    data_test += gaussian_noise
    label_test = [pair[1] for pair in testing_list]
    label_test = np.array(label_test).astype(np.float32).reshape(len(label_test), 2)
    for epoch in range(args.epoch):
        shuffle(training_list)
        batch_idx = (len(training_list) // self.batch_size)
        lr = (args.lr if (epoch < args.epoch_step) else ((args.lr * (args.epoch - epoch)) / (args.epoch - args.epoch_step)))
        for idx in range(batch_idx):
            batch = training_list[(idx * self.batch_size):((idx + 1) * self.batch_size)]
            batch_data = [((np.load(pair[0]) * 2.0) - 1.0) for pair in batch]
            batch_data = np.array(batch_data).astype(np.float32)
            batch_label = [pair[1] for pair in batch]
            batch_label = np.array(batch_label).astype(np.float32).reshape(len(batch_label), 2)
            (_, summary_str, d_loss) = self.sess.run([self.d_optim, self.d_loss_sum, self.d_loss], feed_dict={self.origin_train: batch_data, self.label_train: batch_label, self.lr: lr})
            self.writer.add_summary(summary_str, counter)
            counter += 1
        self.save(args.checkpoint_dir, epoch)
        accuracy_test = self.sess.run(self.accuracy_test, feed_dict={self.origin_test: data_test, self.label_test: label_test})
        print('epoch:', epoch, 'testing accuracy:', accuracy_test, 'loss:', d_loss)

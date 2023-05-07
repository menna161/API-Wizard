from ..layers import SpectralNormalization, GenResBlock, SelfAttention, DiscResBlock, DiscOptResBlock
import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_cifar10 import load_cifar10_with_labels
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.hinge_loss import hinge_loss_generator, hinge_loss_discriminator
import datetime
from tqdm import tqdm
import logging
import imageio


def fit(self, train_ds=None, epochs=100, gen_optimizer='Adam', disc_optimizer='Adam', verbose=1, gen_learning_rate=0.0001, disc_learning_rate=0.0004, beta_1=0, beta_2=0.9, tensorboard=False, save_model=None):
    'Function to train the model\n\n        Args:\n            train_ds (tf.data object): training data\n            epochs (int, optional): number of epochs to train the model. Defaults to ``100``\n            gen_optimizer (str, optional): optimizer used to train generator. Defaults to ``Adam``\n            disc_optimizer (str, optional): optimizer used to train discriminator. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            gen_learning_rate (float, optional): learning rate of the generator optimizer. Defaults to ``0.0001``\n            disc_learning_rate (float, optional): learning rate of the discriminator optimizer. Defaults to ``0.0002``\n            beta_1 (float, optional): decay rate of the first momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            beta_2 (float, optional): decay rate of the second momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n        '
    self.__load_model()
    kwargs = {}
    kwargs['learning_rate'] = gen_learning_rate
    if (gen_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    self.generator_optimizer = getattr(tf.keras.optimizers, gen_optimizer)(**kwargs)
    kwargs = {}
    kwargs['learning_rate'] = disc_learning_rate
    if (disc_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    self.discriminator_optimizer = getattr(tf.keras.optimizers, disc_optimizer)(**kwargs)
    if tensorboard:
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        train_log_dir = (('logs/gradient_tape/' + current_time) + '/train')
        train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    steps = 0
    average_generator_loss = tf.keras.metrics.Mean()
    average_discriminator_loss = tf.keras.metrics.Mean()
    try:
        total = tf.data.experimental.cardinality(train_ds).numpy()
    except BaseException:
        total = 0
    for epoch in range(epochs):
        average_generator_loss.reset_states()
        average_discriminator_loss.reset_states()
        pbar = tqdm(total=total, desc=('Epoch - ' + str((epoch + 1))))
        for (i, batch) in enumerate(train_ds):
            (image_batch, label_batch) = batch
            label_batch = tf.squeeze(label_batch)
            train_stats = self.train_step(image_batch, label_batch)
            G_loss = train_stats['g_loss']
            D_loss = train_stats['d_loss']
            average_generator_loss(G_loss)
            average_discriminator_loss(D_loss)
            steps += 1
            pbar.update(1)
            pbar.set_postfix(disc_loss=average_discriminator_loss.result().numpy(), gen_loss=average_generator_loss.result().numpy())
            if tensorboard:
                with train_summary_writer.as_default():
                    tf.summary.scalar('discr_loss', D_loss.numpy(), step=steps)
                    tf.summary.scalar('genr_loss', G_loss.numpy(), step=steps)
        pbar.close()
        del pbar
        if (verbose == 1):
            print('Epoch:', (epoch + 1), 'D_loss:', average_generator_loss.result().numpy(), 'G_loss', average_discriminator_loss.result().numpy())
    if (save_model is not None):
        assert isinstance(save_model, str), 'Not a valid directory'
        if (save_model[(- 1)] != '/'):
            self.gen_model.save_weights((save_model + '/generator_checkpoint'))
            self.disc_model.save_weights((save_model + '/discriminator_checkpoint'))
        else:
            self.gen_model.save_weights((save_model + 'generator_checkpoint'))
            self.disc_model.save_weights((save_model + 'discriminator_checkpoint'))

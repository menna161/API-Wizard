import cv2
import os
from tensorflow.keras.layers import Dropout, BatchNormalization, Lambda
from tensorflow.keras.layers import Dense, Reshape, Input, ReLU, Conv2D
from tensorflow.keras.layers import Conv2DTranspose, Embedding, Flatten
from tensorflow.keras import Model
import imageio
import numpy as np
from ..datasets.load_custom_data import load_custom_data_AE
from ..datasets.load_mnist import load_mnist_AE
from ..datasets.load_cifar10 import load_cifar10_AE
import datetime
from ..losses.mse_loss import mse_loss
import tensorflow as tf
from tqdm.auto import tqdm


def fit(self, train_ds=None, epochs=100, optimizer='Adam', verbose=1, learning_rate=0.0003, tensorboard=False, save_model=None):
    'Function to train the model\n\n        Args:\n            train_ds (tf.data object): training data\n            epochs (int, optional): number of epochs to train the model. Defaults to ``100``\n            optimizer (str, optional): optimizer used to train the model. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            learning_rate (float, optional): learning rate of the optimizer. Defaults to ``0.001``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n        '
    assert (train_ds is not None), 'Initialize training data through train_ds parameter'
    self.__load_model()
    kwargs = {}
    kwargs['learning_rate'] = learning_rate
    optimizer = getattr(tf.keras.optimizers, optimizer)(**kwargs)
    if tensorboard:
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        train_log_dir = (('logs/gradient_tape/' + current_time) + '/train')
        train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    steps = 0
    total_loss = tf.keras.metrics.Mean()
    VecQuant_loss = tf.keras.metrics.Mean()
    reconstruction_loss = tf.keras.metrics.Mean()
    try:
        total = tf.data.experimental.cardinality(train_ds).numpy()
    except:
        total = 0
    for epoch in range(epochs):
        total_loss.reset_states()
        reconstruction_loss.reset_states()
        VecQuant_loss.reset_states()
        pbar = tqdm(total=total, desc=('Epoch - ' + str((epoch + 1))))
        for data in train_ds:
            with tf.GradientTape() as tape:
                (vq_loss, data_recon, perplexity) = self.model(data)
                recon_err = (mse_loss(data_recon, data) / self.data_var)
                loss = (vq_loss + recon_err)
            gradients = tape.gradient(loss, self.model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
            total_loss(loss)
            reconstruction_loss(recon_err)
            VecQuant_loss(vq_loss)
            steps += 1
            pbar.update(1)
            if tensorboard:
                with train_summary_writer.as_default():
                    tf.summary.scalar('vq_loss', vq_loss.numpy(), step=steps)
                    tf.summary.scalar('reconstruction_loss', recon_err.numpy(), step=steps)
        pbar.close()
        del pbar
        if (verbose == 1):
            print('Epoch:', (epoch + 1), 'total_loss:', total_loss.result().numpy(), 'vq_loss:', VecQuant_loss.result().numpy(), 'reconstruction loss:', reconstruction_loss.result().numpy())
    if (save_model is not None):
        assert isinstance(save_model, str), 'Not a valid directory'
        if (save_model[(- 1)] != '/'):
            self.model.save_weights((save_model + '/vq_vae_checkpoint'))
        else:
            self.model.save_weights((save_model + 'vq_vae_checkpoint'))
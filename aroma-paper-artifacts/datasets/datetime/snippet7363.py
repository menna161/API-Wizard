import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_mnist import load_mnist
from ..datasets.load_cifar10 import load_cifar10
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
from ..losses.infogan_loss import auxillary_loss
import datetime
from tqdm import tqdm
import logging
import imageio


def fit(self, train_ds=None, epochs=100, gen_optimizer='Adam', disc_optimizer='Adam', verbose=1, gen_learning_rate=0.0001, disc_learning_rate=0.0002, beta_1=0.5, tensorboard=False, save_model=None):
    'Function to train the model\n\n        Args:\n            train_ds (tf.data object): training data\n            epochs (int, optional): number of epochs to train the model. Defaults to ``100``\n            gen_optimizer (str, optional): optimizer used to train generator. Defaults to ``Adam``\n            disc_optimizer (str, optional): optimizer used to train discriminator. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            gen_learning_rate (float, optional): learning rate of the generator optimizer. Defaults to ``0.0001``\n            disc_learning_rate (float, optional): learning rate of the discriminator optimizer. Defaults to ``0.0002``\n            beta_1 (float, optional): decay rate of the first momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n        '
    assert (train_ds is not None), 'No Input data found'
    self.__load_model()
    kwargs = {}
    kwargs['learning_rate'] = gen_learning_rate
    if (gen_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    gen_optimizer = getattr(tf.keras.optimizers, gen_optimizer)(**kwargs)
    kwargs = {}
    kwargs['learning_rate'] = disc_learning_rate
    if (disc_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    disc_optimizer = getattr(tf.keras.optimizers, disc_optimizer)(**kwargs)
    if tensorboard:
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        train_log_dir = (('logs/gradient_tape/' + current_time) + '/train')
        train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    steps = 0
    generator_loss = tf.keras.metrics.Mean()
    discriminator_loss = tf.keras.metrics.Mean()
    total_batches = tf.data.experimental.cardinality(train_ds).numpy()
    for epoch in range(epochs):
        generator_loss.reset_states()
        discriminator_loss.reset_states()
        pbar = tqdm(total=total_batches, desc=('Epoch - ' + str((epoch + 1))))
        for data in train_ds:
            batch_size = data.shape[0]
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                Z = np.random.randn(batch_size, self.noise_dim)
                label_input = tf.keras.utils.to_categorical(np.random.randint(0, self.n_classes, batch_size), self.n_classes)
                code_input = np.random.randn(batch_size, self.code_dim)
                c = np.concatenate((Z, label_input, code_input), axis=1)
                gen_imgs = self.gen_model(c, training=True)
                (real_output, _, _) = self.disc_model(data, training=True)
                (fake_output, discrete, cont_out) = self.disc_model(gen_imgs, training=True)
                info_loss = auxillary_loss(discrete, label_input, code_input, cont_out)
                gen_loss = (gan_generator_loss(fake_output) + info_loss)
                disc_loss = (gan_discriminator_loss(real_output, fake_output) + info_loss)
                generator_grads = gen_tape.gradient(gen_loss, self.gen_model.trainable_variables)
                discriminator_grads = disc_tape.gradient(disc_loss, self.disc_model.trainable_variables)
                gen_optimizer.apply_gradients(zip(generator_grads, self.gen_model.trainable_variables))
                disc_optimizer.apply_gradients(zip(discriminator_grads, self.disc_model.trainable_variables))
                generator_loss.update_state(gen_loss)
                discriminator_loss.update_state(disc_loss)
                pbar.update(1)
                pbar.set_postfix(disc_loss=discriminator_loss.result().numpy(), gen_loss=generator_loss.result().numpy())
                steps += 1
                if tensorboard:
                    with train_summary_writer.as_default():
                        tf.summary.scalar('discr_loss', disc_loss.numpy(), step=steps)
                        tf.summary.scalar('genr_loss', gen_loss.numpy(), step=steps)
        pbar.close()
        del pbar
        if verbose:
            print('Epoch:', (epoch + 1), 'D_loss:', generator_loss.result().numpy(), 'G_loss', discriminator_loss.result().numpy())
    if (save_model is not None):
        assert isinstance(save_model, str), 'Not a valid directory'
        if (save_model[(- 1)] != '/'):
            self.gen_model.save_weights((save_model + '/generator_checkpoint'))
            self.disc_model.save_weights((save_model + '/discriminator_checkpoint'))
        else:
            self.gen_model.save_weights((save_model + 'generator_checkpoint'))
            self.disc_model.save_weights((save_model + 'discriminator_checkpoint'))

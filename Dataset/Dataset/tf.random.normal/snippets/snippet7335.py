import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from ..datasets.load_mnist import load_mnist_with_labels
from ..datasets.load_cifar10 import load_cifar10_with_labels
from ..datasets.load_custom_data import load_custom_data_with_labels
from ..losses.minmax_loss import gan_discriminator_loss, gan_generator_loss
import datetime
import imageio
from tqdm.auto import tqdm


def fit(self, train_ds=None, epochs=100, gen_optimizer='Adam', disc_optimizer='Adam', verbose=1, gen_learning_rate=0.0001, disc_learning_rate=0.0002, beta_1=0.5, tensorboard=False, save_model=None):
    'Function to train the model\n\n        Args:\n            train_ds (tf.data object): training data\n            epochs (int, optional): number of epochs to train the model. Defaults to ``100``\n            gen_optimizer (str, optional): optimizer used to train generator. Defaults to ``Adam``\n            disc_optimizer (str, optional): optimizer used to train discriminator. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            gen_learning_rate (float, optional): learning rate of the generator optimizer. Defaults to ``0.0001``\n            disc_learning_rate (float, optional): learning rate of the discriminator optimizer. Defaults to ``0.0002``\n            beta_1 (float, optional): decay rate of the first momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n        '
    assert (train_ds is not None), 'Initialize training data through train_ds parameter'
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
    try:
        total = tf.data.experimental.cardinality(train_ds).numpy()
    except:
        total = 0
    for epoch in range(epochs):
        generator_loss.reset_states()
        discriminator_loss.reset_states()
        pbar = tqdm(total=total, desc=('Epoch - ' + str((epoch + 1))))
        for (data, labels) in train_ds:
            sampled_labels = np.random.randint(0, 10, data.shape[0]).reshape((- 1), 1)
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                noise = tf.random.normal([data.shape[0], self.noise_dim])
                fake_imgs = self.gen_model([noise, sampled_labels])
                real_output = self.disc_model([data, labels], training=True)
                fake_output = self.disc_model([fake_imgs, sampled_labels], training=True)
                G_loss = gan_generator_loss(fake_output)
                D_loss = gan_discriminator_loss(real_output, fake_output)
            gradients_of_generator = gen_tape.gradient(G_loss, self.gen_model.trainable_variables)
            gradients_of_discriminator = disc_tape.gradient(D_loss, self.disc_model.trainable_variables)
            gen_optimizer.apply_gradients(zip(gradients_of_generator, self.gen_model.trainable_variables))
            disc_optimizer.apply_gradients(zip(gradients_of_discriminator, self.disc_model.trainable_variables))
            generator_loss(G_loss)
            discriminator_loss(D_loss)
            steps += 1
            pbar.update(1)
            pbar.set_postfix(disc_loss=discriminator_loss.result().numpy(), gen_loss=generator_loss.result().numpy())
            if tensorboard:
                with train_summary_writer.as_default():
                    tf.summary.scalar('discr_loss', D_loss.numpy(), step=steps)
                    tf.summary.scalar('genr_loss', G_loss.numpy(), step=steps)
        pbar.close()
        del pbar
        if (verbose == 1):
            print('Epoch:', (epoch + 1), 'D_loss:', generator_loss.result().numpy(), 'G_loss', discriminator_loss.result().numpy())
    if (save_model is not None):
        assert isinstance(save_model, str), 'Not a valid directory'
        if (save_model[(- 1)] != '/'):
            self.gen_model.save_weights((save_model + '/generator_checkpoint'))
            self.disc_model.save_weights((save_model + '/discriminator_checkpoint'))
        else:
            self.gen_model.save_weights((save_model + 'generator_checkpoint'))
            self.disc_model.save_weights((save_model + 'discriminator_checkpoint'))

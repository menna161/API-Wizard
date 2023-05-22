import os
from tensorflow.keras.layers import Dropout, Concatenate, BatchNormalization
from tensorflow.keras.layers import LeakyReLU, Conv2DTranspose, ZeroPadding2D
from tensorflow.keras.layers import Dense, Reshape, Flatten, ReLU
from tensorflow.keras.layers import Input, Conv2D
from tensorflow.keras import Model
from ..losses.minmax_loss import gan_generator_loss, gan_discriminator_loss
from ..losses.cyclegan_loss import cycle_loss, identity_loss
from ..datasets.load_cyclegan_datasets import cyclegan_dataloader
from .pix2pix import Pix2Pix
import tensorflow as tf
import numpy as np
import datetime
import cv2
import imageio
from tqdm.auto import tqdm


def fit(self, trainA=None, trainB=None, testA=None, testB=None, epochs=150, gen_g_optimizer='Adam', gen_f_optimizer='Adam', disc_x_optimizer='Adam', disc_y_optimizer='Adam', verbose=1, gen_g_learning_rate=0.0002, gen_f_learning_rate=0.0002, disc_x_learning_rate=0.0002, disc_y_learning_rate=0.0002, beta_1=0.5, tensorboard=False, save_model=None, LAMBDA=100, save_img_per_epoch=30):
    'Function to train the model\n\n        Args:\n            trainA (tf.data object): training data A\n            trainB (tf.data object): training data B\n            testA (tf.data object): testing data A\n            testB (tf.data object): testing data B\n            epochs (int, optional): number of epochs to train the model. Defaults to ``150``\n            gen_g_optimizer (str, optional): optimizer used to train generator `G`. Defaults to ``Adam``\n            gen_F_optimizer (str, optional): optimizer used to train generator `F`. Defaults to ``Adam``\n            disc_x_optimizer (str, optional): optimizer used to train discriminator `X`. Defaults to ``Adam``\n            disc_y_optimizer (str, optional): optimizer used to train discriminator `Y`. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            gen_g_learning_rate (float, optional): learning rate of the generator `G` optimizer. Defaults to ``2e-4``\n            gen_f_learning_rate (float, optional): learning rate of the generator `F` optimizer. Defaults to ``2e-4``\n            disc_x_learning_rate (float, optional): learning rate of the discriminator `X` optimizer. Defaults to ``2e-4``\n            disc_y_learning_rate (float, optional): learning rate of the discriminator `Y` optimizer. Defaults to ``2e-4``\n            beta_1 (float, optional): decay rate of the first momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n            LAMBDA (int, optional): used to calculate generator loss. Defaults to ``100``\n            save_img_per_epoch (int, optional): frequency of saving images during training. Defaults to ``30``\n        '
    assert (trainA is not None), 'Initialize training data A through trainA parameter'
    assert (trainB is not None), 'Initialize training data B through trainB parameter'
    assert (testA is not None), 'Initialize testing data A through testA parameter'
    assert (testB is not None), 'Initialize testing data B through testB parameter'
    self.LAMBDA = LAMBDA
    self.__load_model()
    kwargs = {}
    kwargs['learning_rate'] = gen_g_learning_rate
    if (gen_g_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    gen_g_optimizer = getattr(tf.keras.optimizers, gen_g_optimizer)(**kwargs)
    kwargs = {}
    kwargs['learning_rate'] = gen_f_learning_rate
    if (gen_f_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    gen_f_optimizer = getattr(tf.keras.optimizers, gen_f_optimizer)(**kwargs)
    kwargs = {}
    kwargs['learning_rate'] = disc_x_learning_rate
    if (disc_x_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    disc_x_optimizer = getattr(tf.keras.optimizers, disc_x_optimizer)(**kwargs)
    kwargs = {}
    kwargs['learning_rate'] = disc_y_learning_rate
    if (disc_y_optimizer == 'Adam'):
        kwargs['beta_1'] = beta_1
    disc_y_optimizer = getattr(tf.keras.optimizers, disc_y_optimizer)(**kwargs)
    if tensorboard:
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        train_log_dir = (('logs/gradient_tape/' + current_time) + '/train')
        train_summary_writer = tf.summary.create_file_writer(train_log_dir)
    steps = 0
    curr_dir = os.getcwd()
    try:
        os.mkdir(os.path.join(curr_dir, 'cyclegan_samples'))
    except OSError:
        pass
    self.save_img_dir = os.path.join(curr_dir, 'cyclegan_samples')
    generator_g_loss = tf.keras.metrics.Mean()
    discriminator_x_loss = tf.keras.metrics.Mean()
    generator_f_loss = tf.keras.metrics.Mean()
    discriminator_y_loss = tf.keras.metrics.Mean()
    try:
        total = tf.data.experimental.cardinality(trainA).numpy()
    except:
        total = 0
    total = (total if (total > 0) else len(list(trainA)))
    for epoch in range(epochs):
        generator_g_loss.reset_states()
        generator_f_loss.reset_states()
        discriminator_x_loss.reset_states()
        discriminator_y_loss.reset_states()
        pbar = tqdm(total=total, desc=('Epoch - ' + str((epoch + 1))))
        for (image_x, image_y) in tf.data.Dataset.zip((trainA, trainB)):
            with tf.GradientTape(persistent=True) as tape:
                fake_y = self.gen_model_g(image_x, training=True)
                cycled_x = self.gen_model_f(fake_y, training=True)
                fake_x = self.gen_model_f(image_y, training=True)
                cycled_y = self.gen_model_g(fake_x, training=True)
                same_x = self.gen_model_f(image_x, training=True)
                same_y = self.gen_model_g(image_y, training=True)
                disc_real_x = self.disc_model_x(image_x, training=True)
                disc_real_y = self.disc_model_y(image_y, training=True)
                disc_fake_x = self.disc_model_x(fake_x, training=True)
                disc_fake_y = self.disc_model_y(fake_y, training=True)
                gen_g_loss = gan_generator_loss(disc_fake_y)
                gen_f_loss = gan_generator_loss(disc_fake_x)
                total_cycle_loss = (cycle_loss(image_x, cycled_x, self.LAMBDA) + cycle_loss(image_y, cycled_y, self.LAMBDA))
                total_gen_g_loss = ((gen_g_loss + total_cycle_loss) + identity_loss(image_y, same_y, self.LAMBDA))
                total_gen_f_loss = ((gen_f_loss + total_cycle_loss) + identity_loss(image_x, same_x, self.LAMBDA))
                disc_x_loss = gan_discriminator_loss(disc_real_x, disc_fake_x)
                disc_y_loss = gan_discriminator_loss(disc_real_y, disc_fake_y)
            generator_g_gradients = tape.gradient(total_gen_g_loss, self.gen_model_g.trainable_variables)
            generator_f_gradients = tape.gradient(total_gen_f_loss, self.gen_model_f.trainable_variables)
            discriminator_x_gradients = tape.gradient(disc_x_loss, self.disc_model_x.trainable_variables)
            discriminator_y_gradients = tape.gradient(disc_y_loss, self.disc_model_y.trainable_variables)
            gen_g_optimizer.apply_gradients(zip(generator_g_gradients, self.gen_model_g.trainable_variables))
            gen_f_optimizer.apply_gradients(zip(generator_f_gradients, self.gen_model_f.trainable_variables))
            disc_x_optimizer.apply_gradients(zip(discriminator_x_gradients, self.disc_model_x.trainable_variables))
            disc_y_optimizer.apply_gradients(zip(discriminator_y_gradients, self.disc_model_y.trainable_variables))
            generator_g_loss(total_gen_g_loss)
            generator_f_loss(total_gen_f_loss)
            discriminator_x_loss(disc_x_loss)
            discriminator_y_loss(disc_y_loss)
            steps += 1
            pbar.update(1)
            pbar.set_postfix(disc_x_loss=discriminator_x_loss.result().numpy(), disc_y_loss=discriminator_y_loss.result().numpy(), gen_g_loss=generator_g_loss.result().numpy(), gen_f_loss=generator_f_loss.result().numpy())
            if tensorboard:
                with train_summary_writer.as_default():
                    tf.summary.scalar('Generator_G_loss', total_gen_g_loss.numpy(), step=steps)
                    tf.summary.scalar('Generator_F_loss', total_gen_f_loss.numpy(), step=steps)
                    tf.summary.scalar('Discriminator_X_loss', disc_x_loss.numpy(), step=steps)
                    tf.summary.scalar('Discriminator_Y_loss', disc_y_loss.numpy(), step=steps)
        if ((epoch % save_img_per_epoch) == 0):
            for image in testA.take(1):
                self._save_samples(self.gen_model_g, image, str(epoch))
        if (verbose == 1):
            print('Epoch:', (epoch + 1), 'Generator_G_loss:', generator_g_loss.result().numpy(), 'Generator_F_loss:', generator_f_loss.result().numpy(), 'Discriminator_X_loss:', discriminator_x_loss.result().numpy(), 'Discriminator_Y_loss:', discriminator_y_loss.result().numpy())
    if (save_model is not None):
        assert isinstance(save_model, str), 'Not a valid directory'
        if (save_model[(- 1)] != '/'):
            self.gen_model_g.save_weights((save_model + '/generator_g_checkpoint'))
            self.gen_model_f.save_weights((save_model + '/generator_f_checkpoint'))
            self.disc_model_x.save_weights((save_model + '/discrimnator_x_checkpoint'))
            self.disc_model_y.save_weights((save_model + '/discrimnator_y_checkpoint'))
        else:
            self.gen_model_g.save_weights((save_model + 'generator_g_checkpoint'))
            self.gen_model_f.save_weights((save_model + 'generator_f_checkpoint'))
            self.disc_model_x.save_weights((save_model + 'discrimnator_x_checkpoint'))
            self.disc_model_y.save_weights((save_model + 'discrimnator_y_checkpoint'))

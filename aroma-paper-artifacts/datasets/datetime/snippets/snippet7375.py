import os
from tensorflow.keras.layers import Dropout, Concatenate, BatchNormalization
from tensorflow.keras.layers import LeakyReLU, Conv2DTranspose, ZeroPadding2D
from tensorflow.keras.layers import Dense, Reshape, Flatten
from tensorflow.keras.layers import Conv2D, ReLU, Input
from tensorflow.keras import Model
from ..datasets.load_pix2pix_datasets import pix2pix_dataloader
from ..losses.pix2pix_loss import pix2pix_generator_loss, pix2pix_discriminator_loss
import imageio
import cv2
import tensorflow as tf
import numpy as np
import datetime
from tqdm.auto import tqdm


def fit(self, train_ds=None, test_ds=None, epochs=150, gen_optimizer='Adam', disc_optimizer='Adam', verbose=1, gen_learning_rate=0.0002, disc_learning_rate=0.0002, beta_1=0.5, tensorboard=False, save_model=None, LAMBDA=100, save_img_per_epoch=30):
    'Function to train the model\n\n        Args:\n            train_ds (tf.data object): training data\n            test_ds (tf.data object): testing data\n            epochs (int, optional): number of epochs to train the model. Defaults to ``150``\n            gen_optimizer (str, optional): optimizer used to train generator. Defaults to ``Adam``\n            disc_optimizer (str, optional): optimizer used to train discriminator. Defaults to ``Adam``\n            verbose (int, optional): 1 - prints training outputs, 0 - no outputs. Defaults to ``1``\n            gen_learning_rate (float, optional): learning rate of the generator optimizer. Defaults to ``2e-4``\n            disc_learning_rate (float, optional): learning rate of the discriminator optimizer. Defaults to ``2e-4``\n            beta_1 (float, optional): decay rate of the first momement. set if ``Adam`` optimizer is used. Defaults to ``0.5``\n            tensorboard (bool, optional): if true, writes loss values to ``logs/gradient_tape`` directory\n                which aids visualization. Defaults to ``False``\n            save_model (str, optional): Directory to save the trained model. Defaults to ``None``\n            LAMBDA (int, optional): used to calculate generator loss. Defaults to ``100``\n            save_img_per_epoch (int, optional): frequency of saving images during training. Defaults to ``30``\n        '
    assert (train_ds is not None), 'Initialize training data through train_ds parameter'
    assert (test_ds is not None), 'Initialize testing data through test_ds parameter'
    self.LAMBDA = LAMBDA
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
    curr_dir = os.getcwd()
    try:
        os.mkdir(os.path.join(curr_dir, 'pix2pix_samples'))
    except OSError:
        pass
    self.save_img_dir = os.path.join(curr_dir, 'pix2pix_samples')
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
        for (input_image, target_image) in train_ds:
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                gen_output = self.gen_model(input_image, training=True)
                disc_real_output = self.disc_model([input_image, target_image], training=True)
                disc_gen_output = self.disc_model([input_image, gen_output], training=True)
                (gen_total_loss, gan_loss, l1_loss) = pix2pix_generator_loss(disc_gen_output, gen_output, target_image, self.LAMBDA)
                disc_loss = pix2pix_discriminator_loss(disc_real_output, disc_gen_output)
            gen_gradients = gen_tape.gradient(gen_total_loss, self.gen_model.trainable_variables)
            gen_optimizer.apply_gradients(zip(gen_gradients, self.gen_model.trainable_variables))
            disc_gradients = disc_tape.gradient(disc_loss, self.disc_model.trainable_variables)
            disc_optimizer.apply_gradients(zip(disc_gradients, self.disc_model.trainable_variables))
            generator_loss(gen_total_loss)
            discriminator_loss(disc_loss)
            steps += 1
            pbar.update(1)
            pbar.set_postfix(disc_loss=discriminator_loss.result().numpy(), gen_loss=generator_loss.result().numpy())
            if tensorboard:
                with train_summary_writer.as_default():
                    tf.summary.scalar('discr_loss', disc_loss.numpy(), step=steps)
                    tf.summary.scalar('total_gen_loss', gen_total_loss.numpy(), step=steps)
                    tf.summary.scalar('gan_loss', gan_loss.numpy(), step=steps)
                    tf.summary.scalar('l1_loss', l1_loss.numpy(), step=steps)
        if ((epoch % save_img_per_epoch) == 0):
            for (input_image, target_image) in test_ds.take(1):
                self._save_samples(self.gen_model, input_image, target_image, str(epoch))
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

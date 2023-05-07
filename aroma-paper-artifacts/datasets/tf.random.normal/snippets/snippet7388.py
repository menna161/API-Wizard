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


@tf.function
def train_step(self, images, labels):
    with tf.GradientTape() as disc_tape:
        bs = images.shape[0]
        noise = tf.random.normal([bs, self.noise_dim])
        fake_labels = tf.convert_to_tensor(np.random.randint(0, self.n_classes, bs))
        generated_images = self.gen_model(noise, labels)
        real_output = self.disc_model(images, labels, training=True)
        fake_output = self.disc_model(generated_images, fake_labels, training=True)
        disc_loss = hinge_loss_discriminator(real_output, fake_output)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, self.disc_model.trainable_variables)
        self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.disc_model.trainable_variables))
    with tf.GradientTape() as gen_tape:
        noise = tf.random.normal([bs, self.noise_dim])
        fake_labels = tf.random.uniform((bs,), 0, 10, dtype=tf.int32)
        generated_images = self.gen_model(noise, fake_labels)
        fake_output = self.disc_model(generated_images, fake_labels, training=False)
        gen_loss = hinge_loss_generator(fake_output)
        gradients_of_generator = gen_tape.gradient(gen_loss, self.gen_model.trainable_variables)
        self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.gen_model.trainable_variables))
        train_stats = {'d_loss': disc_loss, 'g_loss': gen_loss, 'd_grads': gradients_of_discriminator, 'g_grads': gradients_of_generator}
        return train_stats

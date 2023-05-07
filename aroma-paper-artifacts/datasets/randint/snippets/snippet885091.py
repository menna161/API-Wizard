from keras.utils import multi_gpu_model
import numpy as np
import tensorflow as tf
import pickle
from keras.models import Model, Input
from keras.optimizers import Adam, RMSprop
from keras.layers import Dense
from keras.layers import Conv2D, Conv2DTranspose
from keras.layers import Flatten, Add
from keras.layers import Concatenate, Activation
from keras.layers import LeakyReLU, BatchNormalization, Lambda
from keras import backend as K
import os


def train(g_par, d_par, gan_model, dataset_real, u_sampled_data, n_epochs, n_batch, n_critic, clip_val, n_patch, f):
    bat_per_epo = int((dataset_real.shape[0] / n_batch))
    half_batch = int((n_batch / 2))
    for i in range(n_epochs):
        for j in range(bat_per_epo):
            for k in range(n_critic):
                ix = np.random.randint(0, dataset_real.shape[0], half_batch)
                X_real = dataset_real[ix]
                y_real = np.ones((half_batch, n_patch, n_patch, 1))
                ix_1 = np.random.randint(0, u_sampled_data.shape[0], half_batch)
                X_fake = g_par.predict(u_sampled_data[ix_1])
                y_fake = (- np.ones((half_batch, n_patch, n_patch, 1)))
                (X, y) = (np.vstack((X_real, X_fake)), np.vstack((y_real, y_fake)))
                (d_loss, accuracy) = d_par.train_on_batch(X, y)
                for l in d_par.layers:
                    weights = l.get_weights()
                    weights = [np.clip(w, (- clip_val), clip_val) for w in weights]
                    l.set_weights(weights)
            ix = np.random.randint(0, dataset_real.shape[0], n_batch)
            X_r = dataset_real[ix]
            X_gen_inp = u_sampled_data[ix]
            y_gan = np.ones((n_batch, n_patch, n_patch, 1))
            g_loss = gan_model.train_on_batch([X_gen_inp], [y_gan, X_r, X_r])
            f.write(('>%d, %d/%d, d=%.3f, acc = %.3f,  w=%.3f,  mae=%.3f,  mssim=%.3f, g=%.3f' % ((i + 1), (j + 1), bat_per_epo, d_loss, accuracy, g_loss[1], g_loss[2], g_loss[3], g_loss[0])))
            f.write('\n')
            print(('>%d, %d/%d, d=%.3f, acc = %.3f, g=%.3f' % ((i + 1), (j + 1), bat_per_epo, d_loss, accuracy, g_loss[0])))
        filename = ('/home/cs-mri-gan/gen_weights_a5_%04d.h5' % (i + 1))
        g_save = g_par.get_layer('model_3')
        g_save.save_weights(filename)
    f.close()

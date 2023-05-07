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


def define_gan_model(gen_model, dis_model, inp_shape):
    dis_model.trainable = False
    inp = Input(shape=inp_shape)
    out_g = gen_model(inp)
    out_dis = dis_model(out_g)
    out_g1 = out_g
    model = Model(inputs=inp, outputs=[out_dis, out_g, out_g1])
    model.summary()
    return model

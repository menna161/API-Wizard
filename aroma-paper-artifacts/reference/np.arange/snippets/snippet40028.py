from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import keras
from keras.callbacks import ModelCheckpoint, LambdaCallback
from keras.optimizers import RMSprop, SGD, Adam
import numpy as np
import argparse
import os
from os import path
import time
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import misc
from densemapnet import Settings
from densemapnet import DenseMapNet
from keras import objectives
from keras import backend as K
import tensorflow as tf
import tifffile


def train_batch(self, epochs=1, lr=0.001, seq=1):
    count = (self.settings.num_dataset + 1)
    checkdir = 'checkpoint'
    try:
        os.mkdir(checkdir)
    except FileExistsError:
        print('Folder exists: ', checkdir)
    is_model_compiled = False
    indexes = np.arange(1, count)
    np.random.shuffle(indexes)
    for i in indexes:
        filename = self.settings.dataset
        filename += ('.densemapnet.weights.%d-%d.h5' % (seq, i))
        filepath = os.path.join(checkdir, filename)
        checkpoint = ModelCheckpoint(filepath=filepath, save_weights_only=True, verbose=1, save_best_only=False)
        callbacks = [checkpoint]
        self.load_train_data(i)
        if (self.network is None):
            self.network = DenseMapNet(settings=self.settings)
            self.model = self.network.build_model()
        if (not is_model_compiled):
            print('Using loss=mae on final conv layer')
            self.model.compile(loss=_loss_mae_disparity, optimizer=Adam(lr=lr))
            is_model_compiled = True
        if self.settings.model_weights:
            if self.settings.notrain:
                self.predict_disparity()
                return
        x = [self.train_lx, self.train_rx]
        self.model.fit(x, self.train_dx, epochs=epochs, batch_size=self.settings.batch_size, shuffle=True, callbacks=callbacks)

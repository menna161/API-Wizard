import cv2
import argparse
import numpy as np
from keras.callbacks import ModelCheckpoint, LambdaCallback
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras import backend as K
import tensorflow as tf
import time
import os
from scipy import misc
from model_icnet import build_icnet
import memory_saving_gradients


def train_model(self):
    checkdir = 'checkpoint'
    try:
        os.mkdir(checkdir)
    except FileExistsError:
        print('Folder exists: ', checkdir)
    lr = (self.args.lr + self.args.decay)
    for i in range(1, (self.args.n_epochs + 1)):
        lr = (lr - self.args.decay)
        indexes = np.arange(1, (self.args.n_trains + 1))
        np.random.shuffle(indexes)
        is_compiled = False
        for j in indexes:
            self.load_train_data(j)
            filename = ('us3d.icnet.weights.%d-%d.h5' % (i, j))
            filepath = os.path.join(checkdir, filename)
            checkpoint = ModelCheckpoint(filepath=filepath, save_weights_only=True, verbose=1, save_best_only=False)
            predict_callback = LambdaCallback(on_epoch_end=(lambda epoch, logs: self.compute_accuracy()))
            callbacks = [checkpoint, predict_callback]
            height = self.train_images[0].shape[0]
            width = self.train_images[0].shape[1]
            bands = self.train_images[0].shape[2]
            myloss = tversky_loss
            if (self.model is None):
                self.model = build_icnet(height, width, bands, self.n_classes, weights_path=self.args.checkpoint, train=True)
            if (not is_compiled):
                self.model.compile(optimizer=Adam(lr=lr), loss=myloss, loss_weights=[1.0, 0.4, 0.16])
                is_compiled = True
            self.model.fit(self.train_images, [self.Y1, self.Y2, self.Y3], epochs=1, batch_size=self.args.batch_size, shuffle=True, callbacks=callbacks)

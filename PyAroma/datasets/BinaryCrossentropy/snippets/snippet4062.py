import os
import time
from datetime import datetime
import tensorflow as tf
import tensorflow_addons as tfa
from absl import flags, logging
from deepray.base.callbacks import LearningRateScheduler, CSVLogger, LossAndErrorPrintingCallback


def build_loss(self):
    if (self.VOC_SIZE[self.LABEL] == 2):
        return tf.keras.losses.BinaryCrossentropy()
    else:
        return tf.keras.losses.SparseCategoricalCrossentropy()

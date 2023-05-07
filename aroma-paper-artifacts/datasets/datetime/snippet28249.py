import time
import datetime
import logging
from typing import Optional, Dict
from collections import defaultdict
import tensorflow as tf
from tensorflow.python import keras
from tensorflow.python.keras.callbacks import Callback
from config import Config


def on_multi_batch_end(self, batch, logs, multi_batch_elapsed):
    nr_samples_in_multi_batch = (self.config.TRAIN_BATCH_SIZE * self.config.NUM_BATCHES_TO_LOG_PROGRESS)
    throughput = (nr_samples_in_multi_batch / multi_batch_elapsed)
    if (self.avg_throughput is None):
        self.avg_throughput = throughput
    else:
        self.avg_throughput = ((0.5 * throughput) + (0.5 * self.avg_throughput))
    remained_batches = (self.config.train_steps_per_epoch - (batch + 1))
    remained_samples = (remained_batches * self.config.TRAIN_BATCH_SIZE)
    remained_time_sec = (remained_samples / self.avg_throughput)
    self.config.log('Train: during epoch #{epoch} batch {batch}/{tot_batches} ({batch_precision}%) -- throughput (#samples/sec): {throughput} -- epoch ETA: {epoch_ETA} -- loss: {loss:.4f}'.format(epoch=(self.training_status.nr_epochs_trained + 1), batch=(batch + 1), batch_precision=int((((batch + 1) / self.config.train_steps_per_epoch) * 100)), tot_batches=self.config.train_steps_per_epoch, throughput=int(throughput), epoch_ETA=str(datetime.timedelta(seconds=int(remained_time_sec))), loss=logs['loss']))

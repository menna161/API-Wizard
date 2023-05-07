import tensorflow as tf
import sys
import numpy as np
from tensorpack import *

if (__name__ == '__main__'):
    dataset_train = get_data()
    config = TrainConfig(model=Model(), dataflow=dataset_train, callbacks=[], max_epoch=100, steps_per_epoch=50)
    trainer = SyncMultiGPUTrainerReplicated(NUM_GPU, mode=('hierarchical' if (NUM_GPU == 8) else 'cpu'))
    launch_train_with_config(config, trainer)

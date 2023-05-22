import tensorflow as tf
import numpy as np
from tensorpack import *

if (__name__ == '__main__'):
    dataset_train = get_data()
    config = TrainConfig(model=Model(), data=StagingInput(QueueInput(dataset_train)), callbacks=[], max_epoch=100, steps_per_epoch=200)
    launch_train_with_config(config, SimpleTrainer())

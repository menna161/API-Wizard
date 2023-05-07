import tensorflow as tf
import numpy as np
import sys
from tensorpack import *

if (__name__ == '__main__'):
    dataset_train = get_data()
    config = TrainConfig(model=Model(), data=StagingInput(QueueInput(dataset_train)), callbacks=[], extra_callbacks=[ProgressBar(['cost'])], max_epoch=200, steps_per_epoch=50)
    if (NUM_GPU == 1):
        trainer = SimpleTrainer()
    else:
        trainer = SyncMultiGPUTrainerReplicated(NUM_GPU, mode='nccl')
    launch_train_with_config(config, trainer)

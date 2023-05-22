import tensorflow as tf
from tensorpack import *

if (__name__ == '__main__'):
    dataset_train = get_data('train')
    dataset_test = get_data('test')
    config = TrainConfig(model=Model(), data=QueueInput(dataset_train, queue=tf.FIFOQueue(300, [tf.float32, tf.int32])), callbacks=[], extra_callbacks=[ProgressBar(['cost', 'train_error']), MergeAllSummaries()], max_epoch=200)
    launch_train_with_config(config, SimpleTrainer())

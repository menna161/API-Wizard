import tensorflow as tf
import numpy as np
import datetime
import os
import argparse
import matplotlib.pyplot as plt
from matplotlib import gridspec
from tensorflow.examples.tutorials.mnist import input_data


def form_results():
    '\n    Forms folders for each run to store the tensorboard files, saved models and the log files.\n    :return: three string pointing to tensorboard, saved models and log paths respectively.\n    '
    folder_name = '/{0}_{1}_{2}_{3}_{4}_{5}_Supervised'.format(datetime.datetime.now(), z_dim, learning_rate, batch_size, n_epochs, beta1)
    tensorboard_path = ((results_path + folder_name) + '/Tensorboard')
    saved_model_path = ((results_path + folder_name) + '/Saved_models/')
    log_path = ((results_path + folder_name) + '/log')
    if (not os.path.exists((results_path + folder_name))):
        os.mkdir((results_path + folder_name))
        os.mkdir(tensorboard_path)
        os.mkdir(saved_model_path)
        os.mkdir(log_path)
    return (tensorboard_path, saved_model_path, log_path)

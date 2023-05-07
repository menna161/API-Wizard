import code
import datetime
import json
import os
import io
import contextlib
import tensorflow as tf
from tqdm import tqdm
import matplotlib.pyplot as plt
from ccn.cfg import get_config
from ccn.graph_match import minimum_loss_permutation
from ccn.vision import Perceptor, perceptual_loss, make_symbol_data, color_composite
from ccn.graph_data import get_dataset
from ccn.ml_utils import dense_regularization, update_data_dict, normalize_data_dict
from ccn.models import get_model, get_optim, get_spy_optim, run_dummy_batch, load_weights, save_weights
from ccn.upload import gs_upload_blob_from_memory, gs_upload_blob_from_string


def get_visual_samples(test_ds, model, test_num_samples, difficulty):
    sample_idxs = tf.random.uniform([CFG['batch_size']], 0, test_num_samples, tf.int32)
    spy_imgs = None
    if CFG['JUST_VISION']:
        vis_batch = tf.gather(test_ds, sample_idxs)
        (_, sample_imgs, aug_imgs) = model(vis_batch, difficulty)
        if CFG['use_spy']:
            (_, spy_imgs, _) = model(vis_batch, difficulty, spy_turn=True)
    else:
        vis_batch = {'adj': tf.gather(test_ds['adj'], sample_idxs), 'node_features': {name: tf.gather(tensor, sample_idxs) for (name, tensor) in test_ds['node_features'].items()}, 'adj_labels': tf.gather(test_ds['adj_labels'], sample_idxs), 'nf_labels': {name: tf.gather(tensor, sample_idxs) for (name, tensor) in test_ds['nf_labels'].items()}, 'num_nodes': tf.gather(test_ds['num_nodes'], sample_idxs)}
        (_, _, sample_imgs, aug_imgs, _, _) = model(vis_batch, difficulty)
        if CFG['use_spy']:
            (_, _, spy_imgs, _, _, _) = model(vis_batch, difficulty, spy_turn=True)
    sample_imgs = ((sample_imgs + 1) / 2)
    aug_imgs = ((aug_imgs + 1) / 2)
    if CFG['use_spy']:
        spy_imgs = ((spy_imgs + 1) / 2)
    return (sample_imgs, aug_imgs, spy_imgs)

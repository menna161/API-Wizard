import os
import code
import math
from typing import List
import tensorflow as tf
import numpy as np
import imageio
from tqdm import tqdm
from ccn.cfg import read_config, read_config_from_string, set_config
from ccn.upload import gs_download_blob_as_string
from ccn.vision import color_composite
from ccn.models import get_model, get_optim, run_dummy_batch, load_weights, save_weights
from ccn.ml_utils import gaussian_k
from ccn.graph_data import TensorGraph, label_data
from PIL import Image, ImageDraw, ImageFont


def write_mosaic(imgs, spy_imgs):
    imgs = tf.concat(imgs, axis=0)
    spy_imgs = tf.concat(spy_imgs, axis=0)
    out = tf.concat([imgs, spy_imgs], axis=1)
    imageio.imwrite(f"gallery/{CFG['load_name']}_mosaic.png", out)

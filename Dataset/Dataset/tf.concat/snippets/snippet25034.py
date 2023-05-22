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


def write_interpolation(imgs, scale_down=1, circle_crop=False, do_blur=True, texts: str=None, spy_imgs=None):
    'Texts is a list of strings equal to the number of imgs\n  '
    assert (len(texts) == len(imgs))
    writer = imageio.get_writer(f"gallery/{CFG['load_name']}_animation.mp4", format='FFMPEG', fps=20)
    for (i, img) in tqdm(enumerate(imgs)):

        def process_img(img):
            img = tf.cast((img * 255), tf.uint8)
            img = tf.image.resize(img, [int((img.shape[0] / scale_down)), int((img.shape[1] / scale_down))], 'lanczos3', antialias=True)
            if circle_crop:
                img = circle_crop(img)
            if do_blur:
                img = blur(img)[0]
            if (texts is not None):
                img = annotate_image(img, texts[i])
            return img
        img = process_img(img)
        if CFG['use_spy']:
            spy_img = process_img(spy_imgs[i])
            img = tf.concat([img, spy_img], axis=1)
        writer.append_data(np.array(img))
    writer.close()

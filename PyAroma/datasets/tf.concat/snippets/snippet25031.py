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


def annotate_image(img, text, side_width=64):
    'Annotate an image with the given text\n  '
    from PIL import Image, ImageDraw, ImageFont
    orig_width = img.shape[1]
    fs = 16
    zeros = tf.zeros((img.shape[0], side_width, img.shape[2]))
    img = tf.concat([img, zeros], axis=1)
    img = np.array(img).astype(np.uint8)
    image = Image.fromarray(img)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('OpenSans.ttf', fs)
    max_height = ((img.shape[0] // 4) - (fs // 2))
    min_height = (((3 * img.shape[0]) // 4) - (fs // 2))
    dist = ((min_height - max_height) // 2)

    def get_height(ratio, path='top'):
        'sinusoidal interpolation\n\n    1 returns center\n    top 0 returns top\n    bot 0 returns bot\n    '
        shift = int((dist * math.sin(((ratio / 2) * math.pi))))
        if (path == 'top'):
            return (max_height + shift)
        else:
            return (min_height - shift)
    top_text = text['top']['text']
    top_color = int((text['top']['amount'] * 255))
    top_color = f'rgb({top_color},{top_color},{top_color})'
    top_height = get_height(text['top']['amount'], path='top')
    draw.text(((orig_width + 8), top_height), top_text, fill=top_color, font=font)
    bot_text = text['bottom']['text']
    bot_color = int((text['bottom']['amount'] * 255))
    bot_color = f'rgb({bot_color},{bot_color},{bot_color})'
    bot_height = get_height(text['bottom']['amount'], path='bot')
    draw.text(((orig_width + 8), bot_height), bot_text, fill=bot_color, font=font)
    return np.array(image)

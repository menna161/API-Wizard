import random
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket, timeout
import cv2
import numpy as np
import pandas as pd
from PIL import Image


def path_to_filename(seq, orig_path):
    'Convert an image path to a CheXpeditor format filename.\n\n    Args:\n        seq (int): the sequence number of the file\n        orig_path (Path): the original image path listed in the CSV\n\n    Returns:\n        (str): a CheXpeditor format filename, under which the file will be\n            saved on the Android device\n\n    '
    nonce = random.randint(0, MAX_NONCE)
    return '__'.join(([str(seq), str(nonce)] + list(orig_path.parts)))

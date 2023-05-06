import tensorflow as tf
import numpy as np
import os
import pickle
import gzip
import urllib.request
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.contrib.keras.api.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.contrib.keras.api.keras.layers import Conv2D, MaxPooling2D
from tensorflow.contrib.keras.api.keras.models import load_model


def extract_labels(filename, num_images):
    with gzip.open(filename) as bytestream:
        bytestream.read(8)
        buf = bytestream.read((1 * num_images))
        labels = np.frombuffer(buf, dtype=np.uint8)
    return (np.arange(10) == labels[(:, None)]).astype(np.float32)

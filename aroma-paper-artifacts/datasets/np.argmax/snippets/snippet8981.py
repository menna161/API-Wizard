from tensorflow.contrib.keras.api.keras.models import Model, model_from_json, Sequential
from PIL import Image
import tensorflow as tf
import os
import numpy as np


def model_prediction(model, inputs):
    prob = model.model.predict(inputs)
    predicted_class = np.argmax(prob)
    prob_str = np.array2string(prob).replace('\n', '')
    return (prob, predicted_class, prob_str)

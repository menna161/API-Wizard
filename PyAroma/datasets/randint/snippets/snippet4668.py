import cv2
import numpy as np
import random
from lib.utils.funtions import image_enhance
from PIL import Image, ImageEnhance
from albumentations import Compose, OneOf, Flip, PadIfNeeded, IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, OpticalDistortion, RandomSizedCrop, HorizontalFlip, VerticalFlip, RandomRotate90, ShiftScaleRotate, CenterCrop, Transpose, GridDistortion, ElasticTransform, RandomGamma, RandomBrightnessContrast, RandomContrast, RandomBrightness, CLAHE, HueSaturationValue, Blur, MedianBlur, ChannelShuffle


def get_random_pos(img, window_shape):
    ' Extract of 2D random patch of shape window_shape in the image '
    (w, h) = window_shape
    (W, H) = img.shape[(- 2):]
    x1 = random.randint(0, ((W - w) - 1))
    x2 = (x1 + w)
    y1 = random.randint(0, ((H - h) - 1))
    y2 = (y1 + h)
    return (x1, x2, y1, y2)

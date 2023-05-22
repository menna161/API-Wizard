import cv2
import numpy as np
import random
from lib.utils.funtions import image_enhance
from PIL import Image, ImageEnhance
from albumentations import Compose, OneOf, Flip, PadIfNeeded, IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, OpticalDistortion, RandomSizedCrop, HorizontalFlip, VerticalFlip, RandomRotate90, ShiftScaleRotate, CenterCrop, Transpose, GridDistortion, ElasticTransform, RandomGamma, RandomBrightnessContrast, RandomContrast, RandomBrightness, CLAHE, HueSaturationValue, Blur, MedianBlur, ChannelShuffle


def imload(filename, gray=False, scale_rate=1.0, enhance=False):
    if (not gray):
        image = cv2.imread(filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if (scale_rate != 1.0):
            image = scale(image, scale_rate)
        if enhance:
            image = Image.fromarray(np.asarray(image, dtype='uint8'))
            contrast = ImageEnhance.Contrast(image)
            image = contrast.enhance(1.55)
    else:
        image = cv2.imread(filename, (- 1))
        if (scale_rate != 1.0):
            image = scale(image, scale_rate, interpolation=cv2.INTER_NEAREST)
        image = np.asarray(image, dtype='uint8')
    return image

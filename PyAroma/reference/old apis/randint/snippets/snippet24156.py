import cv2
import numpy as np


def photometric_distortion(image, brightness_delta=32, contrast_range=(0.5, 1.5), saturation_range=(0.5, 1.5), hue_delta=18, rng=None):
    '\n    Apply photometric distortion to image sequentially. Each transformation\n    is applied with a probability of 0.5.\n    1. random brightness\n    2. random contrast (mode 0)\n    3. convert color from BGR to HSV\n    4. random saturation\n    5. random hue\n    6. convert color from HSV to BGR\n    7. random contrast (mode 1)\n    '

    def convert(image, alpha=1, beta=0):
        '\n        Multiple with alpha and add beat with clip.\n        '
        image = ((image.astype(np.float32) * alpha) + beta)
        image = np.clip(image, 0, 255)
        return image.astype(np.uint8)

    def contrast(image):
        '\n        Contrast distortion.\n        '
        (contrast_lower, contrast_upper) = contrast_range
        if rng.randint(2):
            return convert(image, alpha=rng.uniform(contrast_lower, contrast_upper))
        return image
    if rng.randint(2):
        image = convert(image, beta=rng.uniform((- brightness_delta), brightness_delta))
    mode = rng.randint(2)
    if (mode == 1):
        image = contrast(image)
    (saturation_lower, saturation_upper) = saturation_range
    if rng.randint(2):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image[:, :, 1] = convert(image[:, :, 1], alpha=rng.uniform(saturation_lower, saturation_upper))
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    if rng.randint(2):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image[:, :, 0] = ((image[:, :, 0].astype(int) + rng.randint((- hue_delta), hue_delta)) % 180)
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    if (mode == 0):
        image = contrast(image)
    return image

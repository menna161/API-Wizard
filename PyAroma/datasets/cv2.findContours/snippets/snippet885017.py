import cv2
import math
import numpy as np
import rasterio
import rasterio.features


def get_rectangle(buildings):
    (contours, _) = cv2.findContours(buildings, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0):
        rectangle = cv2.minAreaRect(contours[0])
        return rectangle
    else:
        return None

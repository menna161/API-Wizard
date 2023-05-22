import cv2
import numpy as np


def find_biggest_contour(self, image):
    image = image.copy()
    (s, contours, hierarchy) = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    biggest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], (- 1), 255, (- 1))
    return (biggest_contour, mask)

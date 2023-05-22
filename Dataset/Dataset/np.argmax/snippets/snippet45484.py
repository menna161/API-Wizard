import numpy as np
import cv2


def contract(im_bw, box):
    rows_with_pixels = np.any(im_bw[(box[1]:box[3], box[0]:box[2])], axis=1)
    cols_with_pixels = np.any(im_bw[(box[1]:box[3], box[0]:box[2])], axis=0)
    if ((len((rows_with_pixels == True)) == 0) or (len((cols_with_pixels == True)) == 0)):
        box = [0, 0, 0, 0]
        return box
    left = (box[0] + np.argmax((cols_with_pixels == True)))
    top = (box[1] + np.argmax((rows_with_pixels == True)))
    right = (((box[0] + len(cols_with_pixels)) - np.argmax((cols_with_pixels[::(- 1)] == True))) - 1)
    bottom = (((box[1] + len(rows_with_pixels)) - np.argmax((rows_with_pixels[::(- 1)] == True))) - 1)
    box[0] = left
    box[1] = top
    box[2] = right
    box[3] = bottom
    return box

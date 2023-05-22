import os
import cv2
import numpy as np
import torchvision.transforms as transforms


def show_frame(pred, image=None, out_file='', vis=False):
    if vis:
        result = np.dstack((colors[(pred, 0)], colors[(pred, 1)], colors[(pred, 2)])).astype(np.uint8)
    if (out_file != ''):
        if (not os.path.exists(os.path.split(out_file)[0])):
            os.makedirs(os.path.split(out_file)[0])
        if vis:
            cv2.imwrite(out_file, result)
        else:
            cv2.imwrite(out_file, pred)
    if (vis and (image is not None)):
        temp = ((image.astype(float) * 0.4) + (result.astype(float) * 0.6))
        cv2.imshow('Result', temp.astype(np.uint8))
        cv2.waitKey()

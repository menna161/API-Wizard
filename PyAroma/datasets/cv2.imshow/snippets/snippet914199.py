from collections import deque
import random
import atari_py
import cv2
import torch


def render(self):
    cv2.imshow('screen', self.ale.getScreenRGB()[(:, :, ::(- 1))])
    cv2.waitKey(1)

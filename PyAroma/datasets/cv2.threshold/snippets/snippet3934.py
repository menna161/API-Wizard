import cv2
import sys
import numpy as np


def extract_color(src, h_th_low, h_th_up, s_th, v_th):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(hsv)
    if (h_th_low > h_th_up):
        (ret, h_dst_1) = cv2.threshold(h, h_th_low, 255, cv2.THRESH_BINARY)
        (ret, h_dst_2) = cv2.threshold(h, h_th_up, 255, cv2.THRESH_BINARY_INV)
        dst = cv2.bitwise_or(h_dst_1, h_dst_2)
    else:
        (ret, dst) = cv2.threshold(h, h_th_low, 255, cv2.THRESH_TOZERO)
        (ret, dst) = cv2.threshold(dst, h_th_up, 255, cv2.THRESH_TOZERO_INV)
        (ret, dst) = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)
    (ret, s_dst) = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
    (ret, v_dst) = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_and(dst, s_dst)
    dst = cv2.bitwise_and(dst, v_dst)
    return dst

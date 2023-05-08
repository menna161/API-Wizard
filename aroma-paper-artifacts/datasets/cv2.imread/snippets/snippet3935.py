import cv2
import sys
import numpy as np

if (__name__ == '__main__'):
    param = sys.argv
    if (len(param) != 6):
        print((('Usage: $ python ' + param[0]) + ' sample.jpg h_min, h_max, s_th, v_th'))
        quit()
    try:
        input_img = cv2.imread(param[1])
    except:
        print(('faild to load %s' % param[1]))
        quit()
    if (input_img is None):
        print(('faild to load %s' % param[1]))
        quit()
    h_min = int(param[2])
    h_max = int(param[3])
    s_th = int(param[4])
    v_th = int(param[5])
    msk_img = extract_color(input_img, h_min, h_max, s_th, v_th)
    output_img = cv2.bitwise_and(input_img, input_img, mask=msk_img)
    cv2.imwrite(('extract_' + param[1]), output_img)

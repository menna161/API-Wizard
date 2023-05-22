import cv2
import sys
import numpy as np

if (__name__ == '__main__'):
    param = sys.argv
    if (len(param) != 2):
        print((('Usage: $ python ' + param[0]) + ' sample.jpg'))
        quit()
    try:
        input_img = cv2.imread(param[1])
    except:
        print(('faild to load %s' % param[1]))
        quit()
    if (input_img is None):
        print(('faild to load %s' % param[1]))
        quit()
    (markers, img) = watershed(input_img)
    cv2.imwrite(('watershed_markers_' + param[1]), markers)
    cv2.imwrite(('watershed_image_' + param[1]), img)

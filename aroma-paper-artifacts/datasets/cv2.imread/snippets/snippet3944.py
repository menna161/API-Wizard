import cv2
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS, GPSTAGS

if (__name__ == '__main__'):
    param = sys.argv
    if (len(param) != 2):
        print((('Usage: $ python ' + param[0]) + ' sample.jpg'))
        quit()
    try:
        date = get_date_of_image(param[1])
        output_img = put_date(param[1], date)
        cv2.imwrite(((date.replace(':', '_').replace(' ', '_') + '_') + param[1]), output_img)
    except:
        base_img_cv2 = cv2.imread(param[1])
        cv2.imwrite(('nodate_' + param[1]), base_img_cv2)

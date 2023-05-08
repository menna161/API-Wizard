import cv2
import sys

if (__name__ == '__main__'):
    param = sys.argv
    if (len(param) != 4):
        print((('Usage: $ python ' + param[0]) + ' sample.jpg wide_ratio height_ratio'))
        quit()
    try:
        input_img = cv2.imread(param[1])
    except Exception as e:
        print(e)
        quit()
    if (input_img is None):
        print(('faild to load %s' % param[1]))
        quit()
    w_ratio = int(param[2])
    h_ratio = int(param[3])
    output_img = resize(input_img, w_ratio, h_ratio)
    cv2.imwrite(param[1], output_img)

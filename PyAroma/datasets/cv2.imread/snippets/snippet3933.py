import cv2
import sys

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
    output_img = color_swap(input_img)
    cv2.imwrite(('swap_' + param[1]), output_img)

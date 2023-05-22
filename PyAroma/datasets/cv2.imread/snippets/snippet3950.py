import cv2
import sys
import numpy as np

if (__name__ == '__main__'):
    param = sys.argv
    if (len(param) != 3):
        print((('Usage: $ python ' + param[0]) + ' sample1.jpg sample2.jgp'))
        quit()
    try:
        input_img1 = cv2.imread(param[1])
    except:
        print(('faild to load %s' % param[1]))
        quit()
    if (input_img1 is None):
        print(('faild to load %s' % param[1]))
        quit()
    try:
        input_img2 = cv2.imread(param[2])
    except:
        print(('faild to load %s' % param[2]))
        quit()
    if (input_img2 is None):
        print(('faild to load %s' % param[1]))
        quit()
    gray = cv2.cvtColor(input_img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(input_img2, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT()
    (kp, des) = sift.detectAndCompute(gray, None)
    (kp2, des2) = sift.detectAndCompute(gray2, None)
    matcher = cv2.DescriptorMatcher_create('FlannBased')
    matches = matcher.match(des, des2)
    output_img = drawMatches(gray, kp, gray2, kp2, matches[:100])

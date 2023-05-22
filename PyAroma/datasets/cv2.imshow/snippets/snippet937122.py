import argparse
import tensorflow as tf
import cv2


def main(args):
    mtcnn = MTCNN('./mtcnn.pb')
    img = cv2.imread(args.image)
    (bbox, scores, landmarks) = mtcnn.detect(img)
    print('total box:', len(bbox))
    for (box, pts) in zip(bbox, landmarks):
        box = box.astype('int32')
        img = cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 3)
        pts = pts.astype('int32')
        for i in range(5):
            img = cv2.circle(img, (pts[(i + 5)], pts[i]), 1, (0, 255, 0), 2)
    cv2.imshow('image', img)
    cv2.waitKey(0)

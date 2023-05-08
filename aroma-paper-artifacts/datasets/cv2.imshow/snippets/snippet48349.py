from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pycocotools.coco as COCO
import cv2
import numpy as np
from pycocotools import mask as maskUtils


def count_iou(split):
    coco = COCO.COCO((ANN_PATH + ANN_FILES[split]))
    images = coco.getImgIds()
    cnt = 0
    obj = 0
    for img_id in images:
        ann_ids = coco.getAnnIds(imgIds=[img_id])
        anns = coco.loadAnns(ids=ann_ids)
        bboxes = []
        obj += len(anns)
        for ann in anns:
            if (ann['iscrowd'] > 0):
                continue
            bbox = (_coco_box_to_bbox(ann['bbox']).tolist() + [ann['category_id']])
            for b in bboxes:
                if ((iou(b, bbox) > 0.5) and (b[4] == bbox[4])):
                    cnt += 1
                    if DEBUG:
                        file_name = coco.loadImgs(ids=[img_id])[0]['file_name']
                        img = cv2.imread('{}/{}2017/{}'.format(IMG_PATH, split, file_name))
                        (x1, y1) = (int(b[0]), int(b[1]))
                        (x2, y2) = (int(b[2]), int(b[3]))
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2, cv2.LINE_AA)
                        (x1, y1) = (int(bbox[0]), int(bbox[1]))
                        (x2, y2) = (int(bbox[2]), int(bbox[3]))
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.imshow('img', img)
                        print('cats', class_name[b[4]], class_name[bbox[4]])
                        cv2.waitKey()
            bboxes.append(bbox)
    print('find {} collisions of {} objects!'.format(cnt, obj))

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pycocotools.coco as COCO
import cv2
import numpy as np
from pycocotools import mask as maskUtils


def count(split):
    coco = COCO.COCO((ANN_PATH + ANN_FILES[split]))
    images = coco.getImgIds()
    cnt = 0
    obj = 0
    for img_id in images:
        ann_ids = coco.getAnnIds(imgIds=[img_id])
        anns = coco.loadAnns(ids=ann_ids)
        centers = []
        obj += len(anns)
        for ann in anns:
            if (ann['iscrowd'] > 0):
                continue
            bbox = ann['bbox']
            center = (((bbox[0] + (bbox[2] / 2)) // 4), ((bbox[1] + (bbox[3] / 2)) // 4), ann['category_id'], bbox)
            for c in centers:
                if ((center[0] == c[0]) and (center[1] == c[1]) and (center[2] == c[2]) and (iou(_coco_box_to_bbox(bbox), _coco_box_to_bbox(c[3])) < 2)):
                    cnt += 1
                    if DEBUG:
                        file_name = coco.loadImgs(ids=[img_id])[0]['file_name']
                        img = cv2.imread('{}/{}2017/{}'.format(IMG_PATH, split, file_name))
                        (x1, y1) = (int(c[3][0]), int(c[3][1]))
                        (x2, y2) = (int((c[3][0] + c[3][2])), int((c[3][1] + c[3][3])))
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2, cv2.LINE_AA)
                        (x1, y1) = (int(center[3][0]), int(center[3][1]))
                        (x2, y2) = (int((center[3][0] + center[3][2])), int((center[3][1] + center[3][3])))
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)
                        cv2.imshow('img', img)
                        cv2.waitKey()
            centers.append(center)
    print('find {} collisions of {} objects!'.format(cnt, obj))

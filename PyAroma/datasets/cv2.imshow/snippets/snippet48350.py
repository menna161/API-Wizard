from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pycocotools.coco as COCO
import cv2
import numpy as np
from pycocotools import mask as maskUtils


def count_anchor(split):
    coco = COCO.COCO((ANN_PATH + ANN_FILES[split]))
    images = coco.getImgIds()
    cnt = 0
    obj = 0
    stride = 16
    anchor = generate_anchors().reshape(15, 2, 2)
    (miss_s, miss_m, miss_l) = (0, 0, 0)
    N = len(images)
    print(N, 'images')
    for (ind, img_id) in enumerate(images):
        if ((ind % 1000) == 0):
            print(ind, N)
        anchors = []
        ann_ids = coco.getAnnIds(imgIds=[img_id])
        anns = coco.loadAnns(ids=ann_ids)
        obj += len(anns)
        img_info = coco.loadImgs(ids=[img_id])[0]
        (h, w) = (img_info['height'], img_info['width'])
        if RESIZE:
            if (h > w):
                for i in range(len(anns)):
                    anns[i]['bbox'][0] *= (800 / w)
                    anns[i]['bbox'][1] *= (800 / w)
                    anns[i]['bbox'][2] *= (800 / w)
                    anns[i]['bbox'][3] *= (800 / w)
                h = ((h * 800) // w)
                w = 800
            else:
                for i in range(len(anns)):
                    anns[i]['bbox'][0] *= (800 / h)
                    anns[i]['bbox'][1] *= (800 / h)
                    anns[i]['bbox'][2] *= (800 / h)
                    anns[i]['bbox'][3] *= (800 / h)
                w = ((w * 800) // h)
                h = 800
        for i in range((w // stride)):
            for j in range((h // stride)):
                ct = np.array([(i * stride), (j * stride)], dtype=np.float32).reshape(1, 1, 2)
                anchors.append((anchor + ct))
        anchors = np.concatenate(anchors, axis=0).reshape((- 1), 4)
        anchors[(:, 2:4)] = (anchors[(:, 2:4)] - anchors[(:, 0:2)])
        anchors = anchors.tolist()
        g = [g['bbox'] for g in anns]
        iscrowd = [int(o['iscrowd']) for o in anns]
        ious = maskUtils.iou(anchors, g, iscrowd)
        for t in range(len(g)):
            if (ious[(:, t)].max() < 0.5):
                s = anns[t]['area']
                if (s < (32 ** 2)):
                    miss_s += 1
                elif (s < (96 ** 2)):
                    miss_m += 1
                else:
                    miss_l += 1
        if DEBUG:
            file_name = coco.loadImgs(ids=[img_id])[0]['file_name']
            img = cv2.imread('{}/{}2017/{}'.format(IMG_PATH, split, file_name))
            if RESIZE:
                img = cv2.resize(img, (w, h))
            for (t, gt) in enumerate(g):
                if (anns[t]['iscrowd'] > 0):
                    continue
                (x1, y1, x2, y2) = _coco_box_to_bbox(gt)
                cl = ((0, 0, 255) if (ious[(:, t)].max() < 0.5) else (0, 255, 0))
                cv2.rectangle(img, (x1, y1), (x2, y2), cl, 2, cv2.LINE_AA)
                for k in range(len(anchors)):
                    if (ious[(k, t)] > 0.5):
                        (x1, y1, x2, y2) = _coco_box_to_bbox(anchors[k])
                        cl = (np.array([255, 0, 0]) * ious[(k, t)]).astype(np.int32).tolist()
                        cv2.rectangle(img, (x1, y1), (x2, y2), cl, 1, cv2.LINE_AA)
            cv2.imshow('img', img)
            cv2.waitKey()
        miss = 0
        if (len(ious) > 0):
            miss = (ious.max(axis=0) < 0.5).sum()
        cnt += miss
    print('cnt, obj, ratio ', cnt, obj, (cnt / obj))
    print('s, m, l ', miss_s, miss_m, miss_l)

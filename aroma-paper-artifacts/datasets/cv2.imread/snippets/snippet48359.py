import pycocotools.coco as coco
from pycocotools.cocoeval import COCOeval
import sys
import cv2
import numpy as np
import pickle

if (__name__ == '__main__'):
    dets = []
    img_ids = coco.getImgIds()
    num_images = len(img_ids)
    for k in range(1, len(sys.argv)):
        pred_path = sys.argv[k]
        dets.append(coco.loadRes(pred_path))
    for (i, img_id) in enumerate(img_ids):
        img_info = coco.loadImgs(ids=[img_id])[0]
        img_path = (IMG_PATH + img_info['file_name'])
        img = cv2.imread(img_path)
        gt_ids = coco.getAnnIds(imgIds=[img_id])
        gts = coco.loadAnns(gt_ids)
        gt_img = img.copy()
        for (j, pred) in enumerate(gts):
            bbox = _coco_box_to_bbox(pred['bbox'])
            cat_id = pred['category_id']
            gt_img = add_box(gt_img, bbox, 0, cat_id)
        for k in range(len(dets)):
            pred_ids = dets[k].getAnnIds(imgIds=[img_id])
            preds = dets[k].loadAnns(pred_ids)
            pred_img = img.copy()
            for (j, pred) in enumerate(preds):
                bbox = _coco_box_to_bbox(pred['bbox'])
                sc = pred['score']
                cat_id = pred['category_id']
                if (sc > 0.2):
                    pred_img = add_box(pred_img, bbox, sc, cat_id)
            cv2.imshow('pred{}'.format(k), pred_img)
        cv2.imshow('gt', gt_img)
        cv2.waitKey()

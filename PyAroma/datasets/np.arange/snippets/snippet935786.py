import mmcv
import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from .recall import eval_recalls


def fast_eval_recall(results, coco, max_dets, iou_thrs=np.arange(0.5, 0.96, 0.05)):
    if mmcv.is_str(results):
        assert results.endswith('.pkl')
        results = mmcv.load(results)
    elif (not isinstance(results, list)):
        raise TypeError('results must be a list of numpy arrays or a filename, not {}'.format(type(results)))
    gt_bboxes = []
    img_ids = coco.getImgIds()
    for i in range(len(img_ids)):
        ann_ids = coco.getAnnIds(imgIds=img_ids[i])
        ann_info = coco.loadAnns(ann_ids)
        if (len(ann_info) == 0):
            gt_bboxes.append(np.zeros((0, 4)))
            continue
        bboxes = []
        for ann in ann_info:
            if (ann.get('ignore', False) or ann['iscrowd']):
                continue
            (x1, y1, w, h) = ann['bbox']
            bboxes.append([x1, y1, ((x1 + w) - 1), ((y1 + h) - 1)])
        bboxes = np.array(bboxes, dtype=np.float32)
        if (bboxes.shape[0] == 0):
            bboxes = np.zeros((0, 4))
        gt_bboxes.append(bboxes)
    recalls = eval_recalls(gt_bboxes, results, max_dets, iou_thrs, print_summary=False)
    ar = recalls.mean(axis=1)
    return ar

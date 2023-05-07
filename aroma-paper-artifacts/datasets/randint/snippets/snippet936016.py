import logging
from abc import ABCMeta, abstractmethod
import mmcv
import numpy as np
import torch.nn as nn
import pycocotools.mask as maskUtils
from mmdet.core import tensor2imgs, get_classes, auto_fp16


def show_result(self, data, result, img_norm_cfg, dataset=None, score_thr=0.3, out_file=None):
    if isinstance(result, tuple):
        (bbox_result, segm_result) = result
    else:
        (bbox_result, segm_result) = (result, None)
    img_tensor = data['img'][0]
    img_metas = data['img_meta'][0].data[0]
    imgs = tensor2imgs(img_tensor, **img_norm_cfg)
    assert (len(imgs) == len(img_metas))
    if (dataset is None):
        class_names = self.CLASSES
    elif isinstance(dataset, str):
        class_names = get_classes(dataset)
    elif isinstance(dataset, (list, tuple)):
        class_names = dataset
    else:
        raise TypeError('dataset must be a valid dataset name or a sequence of class names, not {}'.format(type(dataset)))
    for (img, img_meta) in zip(imgs, img_metas):
        (h, w, _) = img_meta['img_shape']
        img_show = img[(:h, :w, :)]
        bboxes = np.vstack(bbox_result)
        if (segm_result is not None):
            segms = mmcv.concat_list(segm_result)
            inds = np.where((bboxes[(:, (- 1))] > score_thr))[0]
            for i in inds:
                color_mask = np.random.randint(0, 256, (1, 3), dtype=np.uint8)
                mask = maskUtils.decode(segms[i]).astype(np.bool)
                img_show[mask] = ((img_show[mask] * 0.5) + (color_mask * 0.5))
        labels = [np.full(bbox.shape[0], i, dtype=np.int32) for (i, bbox) in enumerate(bbox_result)]
        labels = np.concatenate(labels)
        mmcv.imshow_det_bboxes(img_show, bboxes, labels, class_names=class_names, score_thr=score_thr, show=False, out_file=out_file)

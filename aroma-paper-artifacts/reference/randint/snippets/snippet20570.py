import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.utils import _pair
from mmdet.core import auto_fp16, bbox_target, delta2bbox, force_fp32, multiclass_nms
from ..builder import build_loss
from ..losses import accuracy
from ..registry import HEADS


@force_fp32(apply_to=('bbox_preds',))
def refine_bboxes(self, rois, labels, bbox_preds, pos_is_gts, img_metas):
    "Refine bboxes during training.\n\n        Args:\n            rois (Tensor): Shape (n*bs, 5), where n is image number per GPU,\n                and bs is the sampled RoIs per image. The first column is\n                the image id and the next 4 columns are x1, y1, x2, y2.\n            labels (Tensor): Shape (n*bs, ).\n            bbox_preds (Tensor): Shape (n*bs, 4) or (n*bs, 4*#class).\n            pos_is_gts (list[Tensor]): Flags indicating if each positive bbox\n                is a gt bbox.\n            img_metas (list[dict]): Meta info of each image.\n\n        Returns:\n            list[Tensor]: Refined bboxes of each image in a mini-batch.\n\n        Example:\n            >>> # xdoctest: +REQUIRES(module:kwarray)\n            >>> import kwarray\n            >>> import numpy as np\n            >>> from mmdet.core.bbox.demodata import random_boxes\n            >>> self = BBoxHead(reg_class_agnostic=True)\n            >>> n_roi = 2\n            >>> n_img = 4\n            >>> scale = 512\n            >>> rng = np.random.RandomState(0)\n            >>> img_metas = [{'img_shape': (scale, scale)}\n            ...              for _ in range(n_img)]\n            >>> # Create rois in the expected format\n            >>> roi_boxes = random_boxes(n_roi, scale=scale, rng=rng)\n            >>> img_ids = torch.randint(0, n_img, (n_roi,))\n            >>> img_ids = img_ids.float()\n            >>> rois = torch.cat([img_ids[:, None], roi_boxes], dim=1)\n            >>> # Create other args\n            >>> labels = torch.randint(0, 2, (n_roi,)).long()\n            >>> bbox_preds = random_boxes(n_roi, scale=scale, rng=rng)\n            >>> # For each image, pretend random positive boxes are gts\n            >>> is_label_pos = (labels.numpy() > 0).astype(np.int)\n            >>> lbl_per_img = kwarray.group_items(is_label_pos,\n            ...                                   img_ids.numpy())\n            >>> pos_per_img = [sum(lbl_per_img.get(gid, []))\n            ...                for gid in range(n_img)]\n            >>> pos_is_gts = [\n            >>>     torch.randint(0, 2, (npos,)).byte().sort(\n            >>>         descending=True)[0]\n            >>>     for npos in pos_per_img\n            >>> ]\n            >>> bboxes_list = self.refine_bboxes(rois, labels, bbox_preds,\n            >>>                    pos_is_gts, img_metas)\n            >>> print(bboxes_list)\n        "
    img_ids = rois[:, 0].long().unique(sorted=True)
    assert (img_ids.numel() <= len(img_metas))
    bboxes_list = []
    for i in range(len(img_metas)):
        inds = torch.nonzero((rois[:, 0] == i)).squeeze(dim=1)
        num_rois = inds.numel()
        bboxes_ = rois[inds, 1:]
        label_ = labels[inds]
        bbox_pred_ = bbox_preds[inds]
        img_meta_ = img_metas[i]
        pos_is_gts_ = pos_is_gts[i]
        bboxes = self.regress_by_class(bboxes_, label_, bbox_pred_, img_meta_)
        pos_keep = (1 - pos_is_gts_)
        keep_inds = pos_is_gts_.new_ones(num_rois)
        keep_inds[:len(pos_is_gts_)] = pos_keep
        bboxes_list.append(bboxes[keep_inds])
    return bboxes_list

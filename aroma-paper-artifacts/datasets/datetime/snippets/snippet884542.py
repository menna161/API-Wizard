from __future__ import division
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from utils.parse_config import *
from utils.utils import build_targets, to_cpu, non_max_suppression
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import datetime
from torch2trt import torch2trt


def forward(self, x, targets=None, img_dim=None, Half=False):
    FloatTensor = (torch.cuda.FloatTensor if x.is_cuda else torch.FloatTensor)
    FloatTensor = (torch.cuda.HalfTensor if (x.type() == 'torch.cuda.HalfTensor') else torch.cuda.FloatTensor)
    self.img_dim = img_dim
    num_samples = x.size(0)
    grid_size = x.size(2)
    prediction = x.view(num_samples, self.num_anchors, (self.num_classes + 5), grid_size, grid_size).permute(0, 1, 3, 4, 2).contiguous()
    x = torch.sigmoid(prediction[(..., 0)])
    y = torch.sigmoid(prediction[(..., 1)])
    w = prediction[(..., 2)]
    h = prediction[(..., 3)]
    pred_conf = torch.sigmoid(prediction[(..., 4)])
    pred_cls = torch.sigmoid(prediction[(..., 5:)])
    if (grid_size != self.grid_size):
        self.compute_grid_offsets(grid_size, img_dim, cuda=x.is_cuda, Half=Half)
    pred_boxes = FloatTensor(prediction[(..., :4)].shape)
    pred_boxes[(..., 0)] = (x.data + self.grid_x)
    pred_boxes[(..., 1)] = (y.data + self.grid_y)
    pred_boxes[(..., 2)] = (torch.exp(w.data) * self.anchor_w)
    pred_boxes[(..., 3)] = (torch.exp(h.data) * self.anchor_h)
    output = torch.cat(((pred_boxes.view(num_samples, (- 1), 4) * self.stride), pred_conf.view(num_samples, (- 1), 1), pred_cls.view(num_samples, (- 1), self.num_classes)), (- 1))
    if (targets is None):
        return (output, 0)
    else:
        (iou_scores, class_mask, obj_mask, noobj_mask, tx, ty, tw, th, tcls, tconf) = build_targets(pred_boxes=pred_boxes, pred_cls=pred_cls, target=targets, anchors=self.scaled_anchors, ignore_thres=self.ignore_thres)
        loss_x = self.mse_loss(x[obj_mask], tx[obj_mask])
        loss_y = self.mse_loss(y[obj_mask], ty[obj_mask])
        loss_w = self.mse_loss(w[obj_mask], tw[obj_mask])
        loss_h = self.mse_loss(h[obj_mask], th[obj_mask])
        loss_conf_obj = self.bce_loss(pred_conf[obj_mask], tconf[obj_mask])
        loss_conf_noobj = self.bce_loss(pred_conf[noobj_mask], tconf[noobj_mask])
        loss_conf = ((self.obj_scale * loss_conf_obj) + (self.noobj_scale * loss_conf_noobj))
        loss_cls = self.bce_loss(pred_cls[obj_mask], tcls[obj_mask])
        total_loss = (((((loss_x + loss_y) + loss_w) + loss_h) + loss_conf) + loss_cls)
        cls_acc = (100 * class_mask[obj_mask].mean())
        conf_obj = pred_conf[obj_mask].mean()
        conf_noobj = pred_conf[noobj_mask].mean()
        conf50 = (pred_conf > 0.5).float()
        iou50 = (iou_scores > 0.5).float()
        iou75 = (iou_scores > 0.75).float()
        detected_mask = ((conf50 * class_mask) * tconf)
        precision = (torch.sum((iou50 * detected_mask)) / (conf50.sum() + 1e-16))
        recall50 = (torch.sum((iou50 * detected_mask)) / (obj_mask.sum() + 1e-16))
        recall75 = (torch.sum((iou75 * detected_mask)) / (obj_mask.sum() + 1e-16))
        self.metrics = {'loss': to_cpu(total_loss).item(), 'x': to_cpu(loss_x).item(), 'y': to_cpu(loss_y).item(), 'w': to_cpu(loss_w).item(), 'h': to_cpu(loss_h).item(), 'conf': to_cpu(loss_conf).item(), 'cls': to_cpu(loss_cls).item(), 'cls_acc': to_cpu(cls_acc).item(), 'recall50': to_cpu(recall50).item(), 'recall75': to_cpu(recall75).item(), 'precision': to_cpu(precision).item(), 'conf_obj': to_cpu(conf_obj).item(), 'conf_noobj': to_cpu(conf_noobj).item(), 'grid_size': grid_size}
        return (output, total_loss)

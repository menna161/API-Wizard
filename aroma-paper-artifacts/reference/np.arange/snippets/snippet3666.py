from functools import wraps
import importlib
import logging
import numpy as np
import copy
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from core.config import cfg
from model.roi_pooling.functions.roi_pool import RoIPoolFunction
from model.roi_crop.functions.roi_crop import RoICropFunction
from modeling.roi_xfrom.roi_align.functions.roi_align import RoIAlignFunction
import modeling.rpn_heads as rpn_heads
import modeling_rel.fast_rcnn_heads as fast_rcnn_heads
import modeling_rel.relpn_heads as relpn_heads
import modeling_rel.reldn_heads as reldn_heads
import modeling_rel.rel_pyramid_module as rel_pyramid_module
import utils_rel.boxes_rel as box_utils_rel
import utils.boxes as box_utils
import utils.blob as blob_utils
import utils_rel.net_rel as net_utils_rel
from utils.timer import Timer
import utils.resnet_weights_helper as resnet_utils
import utils.fpn as fpn_utils
from modeling_rel.refine_obj_feats import Merge_OBJ_Feats, Message_Passing4OBJ
from modeling_rel.sparse_targets_rel import FrequencyBias, FrequencyBias_Fix
from modeling_rel import refine_obj_feats
from math import pi


def _forward(self, data, im_info, do_vis=False, dataset_name=None, roidb=None, use_gt_labels=False, **rpn_kwargs):
    im_data = data
    if self.training:
        roidb = list(map((lambda x: blob_utils.deserialize(x)[0]), roidb))
    if (dataset_name is not None):
        dataset_name = blob_utils.deserialize(dataset_name)
    else:
        dataset_name = (cfg.TRAIN.DATASETS[0] if self.training else cfg.TEST.DATASETS[0])
    device_id = im_data.get_device()
    return_dict = {}
    blob_conv = self.Conv_Body(im_data)
    if self.training:
        gt_rois = (roidb[0]['boxes'] * im_info[(0, 2)].data.cpu().numpy())
        gt_classes = roidb[0]['gt_classes']
        sbj_gt_boxes = roidb[0]['sbj_gt_boxes']
        obj_gt_boxes = roidb[0]['obj_gt_boxes']
    rpn_ret = self.RPN(blob_conv, im_info, roidb)
    if cfg.FPN.FPN_ON:
        blob_conv = blob_conv[(- self.num_roi_levels):]
    if (cfg.MODEL.SHARE_RES5 and self.training):
        (box_feat, res5_feat) = self.Box_Head(blob_conv, rpn_ret, use_relu=True)
    else:
        box_feat = self.Box_Head(blob_conv, rpn_ret, use_relu=True)
    (cls_score, bbox_pred) = self.Box_Outs(box_feat)
    use_relu = (False if cfg.MODEL.NO_FC7_RELU else True)
    if self.training:
        fg_inds = np.where((rpn_ret['labels_int32'] > 0))[0]
        det_rois = rpn_ret['rois'][fg_inds]
        det_labels = rpn_ret['labels_int32'][fg_inds]
        det_scores = F.softmax(cls_score[fg_inds], dim=1)
        rel_ret = self.RelPN(det_rois, det_labels, det_scores, im_info, dataset_name, roidb)
        select_inds = np.array([])
        repeated_batch_idx = (0 * blob_utils.ones((gt_rois.shape[0], 1)))
        select_rois = np.hstack((repeated_batch_idx, gt_rois))
        select_feat = self.detector_feature_map(blob_conv, select_rois, use_relu=True)
        (select_dists, _) = self.Box_Outs(select_feat)
        select_dists = F.softmax(select_dists, (- 1))
        select_labels = (select_dists[(:, 1:)].max((- 1))[1].data.cpu().numpy() + 1)
        select_gt_labels = gt_classes
        sbj_feat = self.Box_Head_sg(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=True)
        obj_feat = self.Box_Head_sg(blob_conv, rel_ret, rois_name='obj_rois', use_relu=True)
    elif (roidb is not None):
        im_scale = im_info.data.numpy()[(:, 2)][0]
        im_w = im_info.data.numpy()[(:, 1)][0]
        im_h = im_info.data.numpy()[(:, 0)][0]
        gt_rois = (roidb['boxes'] * im_scale)
        sbj_boxes = roidb['sbj_gt_boxes']
        obj_boxes = roidb['obj_gt_boxes']
        sbj_rois = (sbj_boxes * im_scale)
        obj_rois = (obj_boxes * im_scale)
        repeated_batch_idx = (0 * blob_utils.ones((sbj_rois.shape[0], 1)))
        sbj_rois = np.hstack((repeated_batch_idx, sbj_rois))
        obj_rois = np.hstack((repeated_batch_idx, obj_rois))
        if (gt_rois.size > 0):
            repeated_batch_idx = (0 * blob_utils.ones((gt_rois.shape[0], 1)))
            select_rois = np.hstack((repeated_batch_idx, gt_rois))
            select_feat = self.detector_feature_map(blob_conv, select_rois, use_relu=True)
            (select_dists, _) = self.Box_Outs(select_feat)
            select_labels = self.get_nms_preds(select_dists, select_rois, softmax=False)
            select_inds = np.arange(0, select_labels.shape[0]).astype(np.int64)
            rel_ret = self.EdgePN(select_rois, select_labels, select_dists, im_info, dataset_name, None)
            det_feat_sg = self.Box_Head_sg(blob_conv, rel_ret, rois_name='det_rois', use_relu=True)
            det_labels = select_labels.copy()
            det_scores = select_dists[(:, 1:)].max((- 1))[0].data.cpu().numpy()
            min_ious = np.minimum(box_utils.bbox_overlaps(select_rois[(:, 1:)][rel_ret['sbj_inds']], sbj_rois[(:, 1:)]), box_utils.bbox_overlaps(select_rois[(:, 1:)][rel_ret['obj_inds']], obj_rois[(:, 1:)]))
            match_indices = np.where((min_ious.max((- 1)) >= 0.5))[0]
            (rel_ret['sbj_inds'], rel_ret['obj_inds'], rel_ret['sbj_rois'], rel_ret['obj_rois'], rel_ret['rel_rois'], rel_ret['sbj_labels'], rel_ret['obj_labels'], rel_ret['sbj_scores'], rel_ret['obj_scores']) = (rel_ret['sbj_inds'][match_indices], rel_ret['obj_inds'][match_indices], rel_ret['sbj_rois'][match_indices], rel_ret['obj_rois'][match_indices], rel_ret['rel_rois'][match_indices], rel_ret['sbj_labels'][match_indices], rel_ret['obj_labels'][match_indices], rel_ret['sbj_scores'][match_indices], rel_ret['obj_scores'][match_indices])
            sbj_feat = det_feat_sg[rel_ret['sbj_inds']]
            obj_feat = det_feat_sg[rel_ret['obj_inds']]
        else:
            score_thresh = cfg.TEST.SCORE_THRESH
            while (score_thresh >= (- 1e-06)):
                (det_rois, det_labels, det_scores) = self.prepare_det_rois(rpn_ret['rois'], cls_score, bbox_pred, im_info, score_thresh)
                rel_ret = self.RelPN(det_rois, det_labels, det_scores, im_info, dataset_name, None)
                valid_len = len(rel_ret['rel_rois'])
                if (valid_len > 0):
                    break
                logger.info('Got {} rel_rois when score_thresh={}, changing to {}'.format(valid_len, score_thresh, (score_thresh - 0.01)))
                score_thresh -= 0.01
            det_feat = None
            vaild_inds = np.unique(np.concatenate((rel_ret['sbj_inds'], rel_ret['obj_inds']), 0))
            vaild_sort_inds = vaild_inds[np.argsort((- det_scores[vaild_inds]))]
            select_inds = vaild_sort_inds[:10]
            select_rois = det_rois[select_inds]
            det_feat = self.Box_Head(blob_conv, rel_ret, rois_name='det_rois', use_relu=True)
            (det_dists, _) = self.Box_Outs(det_feat)
            select_dists = det_dists[select_inds]
            select_labels = det_labels[select_inds].copy()
    else:
        score_thresh = cfg.TEST.SCORE_THRESH
        while (score_thresh >= (- 1e-06)):
            (det_rois, det_labels, det_scores) = self.prepare_det_rois(rpn_ret['rois'], cls_score, bbox_pred, im_info, score_thresh)
            rel_ret = self.RelPN(det_rois, det_labels, det_scores, im_info, dataset_name, roidb)
            valid_len = len(rel_ret['rel_rois'])
            if (valid_len > 0):
                break
            logger.info('Got {} rel_rois when score_thresh={}, changing to {}'.format(valid_len, score_thresh, (score_thresh - 0.01)))
            score_thresh -= 0.01
        det_feat = None
        vaild_inds = np.unique(np.concatenate((rel_ret['sbj_inds'], rel_ret['obj_inds']), 0))
        vaild_sort_inds = vaild_inds[np.argsort((- det_scores[vaild_inds]))]
        select_inds = vaild_sort_inds
        select_rois = det_rois[select_inds]
        det_feat_sg = self.Box_Head_sg(blob_conv, rel_ret, rois_name='det_rois', use_relu=True)
        sbj_feat = det_feat_sg[rel_ret['sbj_inds']]
        obj_feat = det_feat_sg[rel_ret['obj_inds']]
        if (det_feat is None):
            det_feat = self.Box_Head(blob_conv, rel_ret, rois_name='det_rois', use_relu=True)
        (det_dists, _) = self.Box_Outs(det_feat)
        select_dists = det_dists[select_inds]
        select_labels = det_labels[select_inds].copy()
    if ((select_inds.size > 2) or self.training):
        entity_fmap = self.obj_feature_map(blob_conv.detach(), select_rois, use_relu=True)
        entity_feat0 = self.merge_obj_feats(entity_fmap, select_rois, select_dists.detach(), im_info)
        edge_ret = self.EdgePN(select_rois, select_labels, select_dists, im_info, dataset_name, None)
        edge_feat = self.get_phr_feats(self.visual_rep(blob_conv, edge_ret, device_id, use_relu=use_relu))
        edge_inds = np.stack((edge_ret['sbj_rois'][(:, 0)].astype(edge_ret['sbj_inds'].dtype), edge_ret['sbj_inds'], edge_ret['obj_inds']), (- 1))
        im_inds = select_rois[(:, 0)].astype(edge_inds.dtype)
        entity_feat = self.obj_mps1(entity_feat0, edge_feat, im_inds, edge_inds)
        entity_feat = self.obj_mps2(entity_feat, edge_feat, im_inds, edge_inds)
        entity_cls_score = self.ObjClassifier(entity_feat)
        if (not self.training):
            select_labels_pred = self.get_nms_preds(entity_cls_score, select_rois)
            det_labels[select_inds] = select_labels_pred
            if use_gt_labels:
                det_labels[select_inds] = roidb['gt_classes']
            select_twod_inds = ((np.arange(0, select_labels_pred.shape[0]) * cfg.MODEL.NUM_CLASSES) + select_labels_pred)
            select_scores = F.softmax(entity_cls_score, (- 1)).view((- 1))[select_twod_inds].data.cpu().numpy()
            det_scores[select_inds] = select_scores
            if use_gt_labels:
                det_scores[select_inds] = np.ones_like(select_scores)
    rel_feat = self.visual_rep(blob_conv, rel_ret, device_id, use_relu=use_relu)
    if (not self.training):
        sbj_labels = det_labels[rel_ret['sbj_inds']]
        obj_labels = det_labels[rel_ret['obj_inds']]
        rel_ret['sbj_labels'] = det_labels[rel_ret['sbj_inds']]
        rel_ret['obj_labels'] = det_labels[rel_ret['obj_inds']]
        rel_ret['sbj_scores'] = det_scores[rel_ret['sbj_inds']]
        rel_ret['obj_scores'] = det_scores[rel_ret['obj_inds']]
    else:
        sbj_labels = (rel_ret['all_sbj_labels_int32'] + 1)
        obj_labels = (rel_ret['all_obj_labels_int32'] + 1)
    sbj_embed = self.ori_embed[sbj_labels].clone().cuda(device_id)
    obj_embed = self.ori_embed[obj_labels].clone().cuda(device_id)
    sbj_pos = torch.from_numpy(self.get_obj_pos(rel_ret['sbj_rois'], im_info)).float().cuda(device_id)
    obj_pos = torch.from_numpy(self.get_obj_pos(rel_ret['obj_rois'], im_info)).float().cuda(device_id)
    prod = (self.sbj_map(torch.cat((sbj_feat, sbj_embed, sbj_pos), (- 1))) * self.obj_map(torch.cat((obj_feat, obj_embed, obj_pos), (- 1))))
    prd_scores = self.rel_compress((rel_feat * prod))
    if cfg.MODEL.USE_FREQ_BIAS:
        sbj_labels = torch.from_numpy(sbj_labels).long().cuda(device_id)
        obj_labels = torch.from_numpy(obj_labels).long().cuda(device_id)
        prd_bias_scores = self.freq_bias.rel_index_with_labels(torch.stack(((sbj_labels - 1), (obj_labels - 1)), 1))
        prd_scores += prd_bias_scores
    if (not self.training):
        prd_scores = F.softmax(prd_scores, (- 1))
    if self.training:
        return_dict['losses'] = {}
        return_dict['metrics'] = {}
        imp_gamma = get_importance_factor(select_rois, sbj_gt_boxes, obj_gt_boxes, im_info)
        rpn_kwargs.update(dict(((k, rpn_ret[k]) for k in rpn_ret.keys() if (k.startswith('rpn_cls_logits') or k.startswith('rpn_bbox_pred')))))
        (loss_rpn_cls, loss_rpn_bbox) = rpn_heads.generic_rpn_losses(**rpn_kwargs)
        if cfg.FPN.FPN_ON:
            for (i, lvl) in enumerate(range(cfg.FPN.RPN_MIN_LEVEL, (cfg.FPN.RPN_MAX_LEVEL + 1))):
                return_dict['losses'][('loss_rpn_cls_fpn%d' % lvl)] = loss_rpn_cls[i]
                return_dict['losses'][('loss_rpn_bbox_fpn%d' % lvl)] = loss_rpn_bbox[i]
        else:
            return_dict['losses']['loss_rpn_cls'] = loss_rpn_cls
            return_dict['losses']['loss_rpn_bbox'] = loss_rpn_bbox
        (loss_cls, loss_bbox, accuracy_cls) = fast_rcnn_heads.fast_rcnn_losses(cls_score, bbox_pred, rpn_ret['labels_int32'], rpn_ret['bbox_targets'], rpn_ret['bbox_inside_weights'], rpn_ret['bbox_outside_weights'])
        return_dict['losses']['loss_cls'] = loss_cls
        return_dict['losses']['loss_bbox'] = loss_bbox
        return_dict['metrics']['accuracy_cls'] = accuracy_cls
        (loss_cls_prd, accuracy_cls_prd) = reldn_heads.reldn_losses(prd_scores, rel_ret['all_prd_labels_int32'])
        return_dict['losses']['loss_cls_prd'] = loss_cls_prd
        return_dict['metrics']['accuracy_cls_prd'] = accuracy_cls_prd
        (loss_cls_entity, accuracy_cls_entity) = refine_obj_feats.entity_losses_imp(entity_cls_score, select_gt_labels, imp_gamma)
        return_dict['losses']['loss_cls_entity'] = loss_cls_entity
        return_dict['metrics']['accuracy_cls_entity'] = accuracy_cls_entity
        for (k, v) in return_dict['losses'].items():
            return_dict['losses'][k] = v.unsqueeze(0)
        for (k, v) in return_dict['metrics'].items():
            return_dict['metrics'][k] = v.unsqueeze(0)
    else:
        return_dict['sbj_rois'] = rel_ret['sbj_rois']
        return_dict['obj_rois'] = rel_ret['obj_rois']
        return_dict['sbj_labels'] = rel_ret['sbj_labels']
        return_dict['obj_labels'] = rel_ret['obj_labels']
        return_dict['sbj_scores'] = rel_ret['sbj_scores']
        return_dict['obj_scores'] = rel_ret['obj_scores']
        return_dict['prd_scores'] = prd_scores
        if do_vis:
            return_dict['blob_conv'] = blob_conv
    return return_dict

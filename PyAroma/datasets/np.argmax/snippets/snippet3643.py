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
    if (not cfg.MODEL.USE_REL_PYRAMID):
        blob_conv_prd = self.Prd_RCNN.Conv_Body(im_data)
    rpn_ret = self.RPN(blob_conv, im_info, roidb)
    if cfg.FPN.FPN_ON:
        blob_conv = blob_conv[(- self.num_roi_levels):]
        if (not cfg.MODEL.USE_REL_PYRAMID):
            blob_conv_prd = blob_conv_prd[(- self.num_roi_levels):]
        else:
            blob_conv_prd = self.RelPyramid(blob_conv)
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
        if cfg.MODEL.ADD_SO_SCORES:
            sbj_feat = self.S_Head(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=use_relu)
            obj_feat = self.O_Head(blob_conv, rel_ret, rois_name='obj_rois', use_relu=use_relu)
        else:
            sbj_feat = self.Box_Head(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=use_relu)
            obj_feat = self.Box_Head(blob_conv, rel_ret, rois_name='obj_rois', use_relu=use_relu)
        if (cfg.MODEL.USE_NODE_CONTRASTIVE_LOSS or cfg.MODEL.USE_NODE_CONTRASTIVE_SO_AWARE_LOSS or cfg.MODEL.USE_NODE_CONTRASTIVE_P_AWARE_LOSS):
            if cfg.MODEL.ADD_SO_SCORES:
                sbj_feat_sbj_pos = self.S_Head(blob_conv, rel_ret, rois_name='sbj_rois_sbj_pos', use_relu=use_relu)
                obj_feat_sbj_pos = self.O_Head(blob_conv, rel_ret, rois_name='obj_rois_sbj_pos', use_relu=use_relu)
                sbj_feat_obj_pos = self.S_Head(blob_conv, rel_ret, rois_name='sbj_rois_obj_pos', use_relu=use_relu)
                obj_feat_obj_pos = self.O_Head(blob_conv, rel_ret, rois_name='obj_rois_obj_pos', use_relu=use_relu)
            else:
                sbj_feat_sbj_pos = self.Box_Head(blob_conv, rel_ret, rois_name='sbj_rois_sbj_pos', use_relu=use_relu)
                obj_feat_sbj_pos = self.Box_Head(blob_conv, rel_ret, rois_name='obj_rois_sbj_pos', use_relu=use_relu)
                sbj_feat_obj_pos = self.Box_Head(blob_conv, rel_ret, rois_name='sbj_rois_obj_pos', use_relu=use_relu)
                obj_feat_obj_pos = self.Box_Head(blob_conv, rel_ret, rois_name='obj_rois_obj_pos', use_relu=use_relu)
    elif (roidb is not None):
        im_scale = im_info.data.numpy()[(:, 2)][0]
        im_w = im_info.data.numpy()[(:, 1)][0]
        im_h = im_info.data.numpy()[(:, 0)][0]
        sbj_boxes = roidb['sbj_gt_boxes']
        obj_boxes = roidb['obj_gt_boxes']
        sbj_rois = (sbj_boxes * im_scale)
        obj_rois = (obj_boxes * im_scale)
        repeated_batch_idx = (0 * blob_utils.ones((sbj_rois.shape[0], 1)))
        sbj_rois = np.hstack((repeated_batch_idx, sbj_rois))
        obj_rois = np.hstack((repeated_batch_idx, obj_rois))
        rel_rois = box_utils_rel.rois_union(sbj_rois, obj_rois)
        rel_ret = {}
        rel_ret['sbj_rois'] = sbj_rois
        rel_ret['obj_rois'] = obj_rois
        rel_ret['rel_rois'] = rel_rois
        if (cfg.FPN.FPN_ON and cfg.FPN.MULTILEVEL_ROIS):
            lvl_min = cfg.FPN.ROI_MIN_LEVEL
            lvl_max = cfg.FPN.ROI_MAX_LEVEL
            rois_blob_names = ['sbj_rois', 'obj_rois', 'rel_rois']
            for rois_blob_name in rois_blob_names:
                target_lvls = fpn_utils.map_rois_to_fpn_levels(rel_ret[rois_blob_name][(:, 1:5)], lvl_min, lvl_max)
                fpn_utils.add_multilevel_roi_blobs(rel_ret, rois_blob_name, rel_ret[rois_blob_name], target_lvls, lvl_min, lvl_max)
        sbj_det_feat = self.Box_Head(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=True)
        (sbj_cls_scores, _) = self.Box_Outs(sbj_det_feat)
        sbj_cls_scores = sbj_cls_scores.data.cpu().numpy()
        obj_det_feat = self.Box_Head(blob_conv, rel_ret, rois_name='obj_rois', use_relu=True)
        (obj_cls_scores, _) = self.Box_Outs(obj_det_feat)
        obj_cls_scores = obj_cls_scores.data.cpu().numpy()
        if use_gt_labels:
            sbj_labels = roidb['sbj_gt_classes']
            obj_labels = roidb['obj_gt_classes']
            sbj_scores = np.ones_like(sbj_labels, dtype=np.float32)
            obj_scores = np.ones_like(obj_labels, dtype=np.float32)
        else:
            sbj_labels = np.argmax(sbj_cls_scores[(:, 1:)], axis=1)
            obj_labels = np.argmax(obj_cls_scores[(:, 1:)], axis=1)
            sbj_scores = np.amax(sbj_cls_scores[(:, 1:)], axis=1)
            obj_scores = np.amax(obj_cls_scores[(:, 1:)], axis=1)
        rel_ret['sbj_scores'] = sbj_scores.astype(np.float32, copy=False)
        rel_ret['obj_scores'] = obj_scores.astype(np.float32, copy=False)
        rel_ret['sbj_labels'] = (sbj_labels.astype(np.int32, copy=False) + 1)
        rel_ret['obj_labels'] = (obj_labels.astype(np.int32, copy=False) + 1)
        rel_ret['all_sbj_labels_int32'] = sbj_labels.astype(np.int32, copy=False)
        rel_ret['all_obj_labels_int32'] = obj_labels.astype(np.int32, copy=False)
        if cfg.MODEL.USE_SPATIAL_FEAT:
            spt_feat = box_utils_rel.get_spt_features(sbj_boxes, obj_boxes, im_w, im_h)
            rel_ret['spt_feat'] = spt_feat
        if cfg.MODEL.ADD_SO_SCORES:
            sbj_feat = self.S_Head(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=use_relu)
            obj_feat = self.O_Head(blob_conv, rel_ret, rois_name='obj_rois', use_relu=use_relu)
        else:
            sbj_feat = self.Box_Head(blob_conv, rel_ret, rois_name='sbj_rois', use_relu=use_relu)
            obj_feat = self.Box_Head(blob_conv, rel_ret, rois_name='obj_rois', use_relu=use_relu)
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
        if cfg.MODEL.ADD_SO_SCORES:
            det_s_feat = self.S_Head(blob_conv, rel_ret, rois_name='det_rois', use_relu=use_relu)
            det_o_feat = self.O_Head(blob_conv, rel_ret, rois_name='det_rois', use_relu=use_relu)
            sbj_feat = det_s_feat[rel_ret['sbj_inds']]
            obj_feat = det_o_feat[rel_ret['obj_inds']]
        else:
            det_feat = self.Box_Head(blob_conv, rel_ret, rois_name='det_rois', use_relu=use_relu)
            sbj_feat = det_feat[rel_ret['sbj_inds']]
            obj_feat = det_feat[rel_ret['obj_inds']]
    rel_feat = self.Prd_RCNN.Box_Head(blob_conv_prd, rel_ret, rois_name='rel_rois', use_relu=use_relu)
    spo_feat = torch.cat((sbj_feat, rel_feat, obj_feat), dim=1)
    if cfg.MODEL.USE_SPATIAL_FEAT:
        spt_feat = rel_ret['spt_feat']
    else:
        spt_feat = None
    if (cfg.MODEL.USE_FREQ_BIAS or cfg.MODEL.RUN_BASELINE):
        sbj_labels = rel_ret['all_sbj_labels_int32']
        obj_labels = rel_ret['all_obj_labels_int32']
    else:
        sbj_labels = None
        obj_labels = None
    (prd_scores, prd_bias_scores, prd_spt_scores, ttl_cls_scores, sbj_cls_scores, obj_cls_scores) = self.RelDN(spo_feat, spt_feat, sbj_labels, obj_labels, sbj_feat, obj_feat)
    if self.training:
        return_dict['losses'] = {}
        return_dict['metrics'] = {}
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
        if (cfg.MODEL.USE_FREQ_BIAS and (not cfg.MODEL.ADD_SCORES_ALL)):
            (loss_cls_bias, accuracy_cls_bias) = reldn_heads.reldn_losses(prd_bias_scores, rel_ret['all_prd_labels_int32'])
            return_dict['losses']['loss_cls_bias'] = loss_cls_bias
            return_dict['metrics']['accuracy_cls_bias'] = accuracy_cls_bias
        if (cfg.MODEL.USE_SPATIAL_FEAT and (not cfg.MODEL.ADD_SCORES_ALL)):
            (loss_cls_spt, accuracy_cls_spt) = reldn_heads.reldn_losses(prd_spt_scores, rel_ret['all_prd_labels_int32'])
            return_dict['losses']['loss_cls_spt'] = loss_cls_spt
            return_dict['metrics']['accuracy_cls_spt'] = accuracy_cls_spt
        if cfg.MODEL.ADD_SCORES_ALL:
            (loss_cls_ttl, accuracy_cls_ttl) = reldn_heads.reldn_losses(ttl_cls_scores, rel_ret['all_prd_labels_int32'])
            return_dict['losses']['loss_cls_ttl'] = loss_cls_ttl
            return_dict['metrics']['accuracy_cls_ttl'] = accuracy_cls_ttl
        else:
            (loss_cls_prd, accuracy_cls_prd) = reldn_heads.reldn_losses(prd_scores, rel_ret['all_prd_labels_int32'])
            return_dict['losses']['loss_cls_prd'] = loss_cls_prd
            return_dict['metrics']['accuracy_cls_prd'] = accuracy_cls_prd
        if (cfg.MODEL.USE_NODE_CONTRASTIVE_LOSS or cfg.MODEL.USE_NODE_CONTRASTIVE_SO_AWARE_LOSS or cfg.MODEL.USE_NODE_CONTRASTIVE_P_AWARE_LOSS):
            rel_feat_sbj_pos = self.Prd_RCNN.Box_Head(blob_conv_prd, rel_ret, rois_name='rel_rois_sbj_pos', use_relu=use_relu)
            spo_feat_sbj_pos = torch.cat((sbj_feat_sbj_pos, rel_feat_sbj_pos, obj_feat_sbj_pos), dim=1)
            if cfg.MODEL.USE_SPATIAL_FEAT:
                spt_feat_sbj_pos = rel_ret['spt_feat_sbj_pos']
            else:
                spt_feat_sbj_pos = None
            if (cfg.MODEL.USE_FREQ_BIAS or cfg.MODEL.RUN_BASELINE):
                sbj_labels_sbj_pos_fg = rel_ret['sbj_labels_sbj_pos_fg_int32']
                obj_labels_sbj_pos_fg = rel_ret['obj_labels_sbj_pos_fg_int32']
            else:
                sbj_labels_sbj_pos_fg = None
                obj_labels_sbj_pos_fg = None
            (_, prd_bias_scores_sbj_pos, _, ttl_cls_scores_sbj_pos, _, _) = self.RelDN(spo_feat_sbj_pos, spt_feat_sbj_pos, sbj_labels_sbj_pos_fg, obj_labels_sbj_pos_fg, sbj_feat_sbj_pos, obj_feat_sbj_pos)
            rel_feat_obj_pos = self.Prd_RCNN.Box_Head(blob_conv_prd, rel_ret, rois_name='rel_rois_obj_pos', use_relu=use_relu)
            spo_feat_obj_pos = torch.cat((sbj_feat_obj_pos, rel_feat_obj_pos, obj_feat_obj_pos), dim=1)
            if cfg.MODEL.USE_SPATIAL_FEAT:
                spt_feat_obj_pos = rel_ret['spt_feat_obj_pos']
            else:
                spt_feat_obj_pos = None
            if (cfg.MODEL.USE_FREQ_BIAS or cfg.MODEL.RUN_BASELINE):
                sbj_labels_obj_pos_fg = rel_ret['sbj_labels_obj_pos_fg_int32']
                obj_labels_obj_pos_fg = rel_ret['obj_labels_obj_pos_fg_int32']
            else:
                sbj_labels_obj_pos_fg = None
                obj_labels_obj_pos_fg = None
            (_, prd_bias_scores_obj_pos, _, ttl_cls_scores_obj_pos, _, _) = self.RelDN(spo_feat_obj_pos, spt_feat_obj_pos, sbj_labels_obj_pos_fg, obj_labels_obj_pos_fg, sbj_feat_obj_pos, obj_feat_obj_pos)
            if cfg.MODEL.USE_NODE_CONTRASTIVE_LOSS:
                (loss_contrastive_sbj, loss_contrastive_obj) = reldn_heads.reldn_contrastive_losses(ttl_cls_scores_sbj_pos, ttl_cls_scores_obj_pos, rel_ret)
                return_dict['losses']['loss_contrastive_sbj'] = (loss_contrastive_sbj * cfg.MODEL.NODE_CONTRASTIVE_WEIGHT)
                return_dict['losses']['loss_contrastive_obj'] = (loss_contrastive_obj * cfg.MODEL.NODE_CONTRASTIVE_WEIGHT)
            if cfg.MODEL.USE_NODE_CONTRASTIVE_SO_AWARE_LOSS:
                (loss_so_contrastive_sbj, loss_so_contrastive_obj) = reldn_heads.reldn_so_contrastive_losses(ttl_cls_scores_sbj_pos, ttl_cls_scores_obj_pos, rel_ret)
                return_dict['losses']['loss_so_contrastive_sbj'] = (loss_so_contrastive_sbj * cfg.MODEL.NODE_CONTRASTIVE_SO_AWARE_WEIGHT)
                return_dict['losses']['loss_so_contrastive_obj'] = (loss_so_contrastive_obj * cfg.MODEL.NODE_CONTRASTIVE_SO_AWARE_WEIGHT)
            if cfg.MODEL.USE_NODE_CONTRASTIVE_P_AWARE_LOSS:
                (loss_p_contrastive_sbj, loss_p_contrastive_obj) = reldn_heads.reldn_p_contrastive_losses(ttl_cls_scores_sbj_pos, ttl_cls_scores_obj_pos, prd_bias_scores_sbj_pos, prd_bias_scores_obj_pos, rel_ret)
                return_dict['losses']['loss_p_contrastive_sbj'] = (loss_p_contrastive_sbj * cfg.MODEL.NODE_CONTRASTIVE_P_AWARE_WEIGHT)
                return_dict['losses']['loss_p_contrastive_obj'] = (loss_p_contrastive_obj * cfg.MODEL.NODE_CONTRASTIVE_P_AWARE_WEIGHT)
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
        if cfg.MODEL.USE_FREQ_BIAS:
            return_dict['prd_scores_bias'] = prd_bias_scores
        if cfg.MODEL.USE_SPATIAL_FEAT:
            return_dict['prd_scores_spt'] = prd_spt_scores
        if cfg.MODEL.ADD_SCORES_ALL:
            return_dict['prd_ttl_scores'] = ttl_cls_scores
        if do_vis:
            return_dict['blob_conv'] = blob_conv
            return_dict['blob_conv_prd'] = blob_conv_prd
    return return_dict

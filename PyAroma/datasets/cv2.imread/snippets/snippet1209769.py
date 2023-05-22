from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import _init_paths
import os
import sys
import numpy as np
import argparse
import pprint
import pdb
import time
import cv2
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import pickle
from roi_data_layer.roidb import combined_roidb
from roi_data_layer.roibatchLoader import roibatchLoader
from model.utils.config import cfg, cfg_from_file, cfg_from_list, get_output_dir
from model.rpn.bbox_transform import clip_boxes
from model.nms.nms_wrapper import nms
from model.rpn.bbox_transform import bbox_transform_inv
from model.utils.net_utils import save_net, load_net, vis_detections
from model.faster_rcnn.vgg16 import vgg16
from model.faster_rcnn.resnet import resnet
import pdb

if (__name__ == '__main__'):
    args = parse_args()
    print('Called with args:')
    print(args)
    if (torch.cuda.is_available() and (not args.cuda)):
        print('WARNING: You have a CUDA device, so you should probably run with --cuda')
    np.random.seed(cfg.RNG_SEED)
    if (args.dataset == 'pascal_voc'):
        args.imdb_name = 'voc_2007_trainval'
        args.imdbval_name = 'voc_2007_test'
        args.set_cfgs = ['ANCHOR_SCALES', '[8, 16, 32]', 'ANCHOR_RATIOS', '[0.5,1,2]']
    if (args.dataset == 'uav'):
        args.imdb_name = 'uav_2017_trainval'
        args.imdbval_name = 'uav_2017_test'
        args.set_cfgs = ['ANCHOR_SCALES', '[1, 2, 4, 8, 16]', 'ANCHOR_RATIOS', '[0.5,1,2]', 'MAX_NUM_GT_BOXES', '20']
    elif (args.dataset == 'pascal_voc_0712'):
        args.imdb_name = 'voc_2007_trainval+voc_2012_trainval'
        args.imdbval_name = 'voc_2007_test'
        args.set_cfgs = ['ANCHOR_SCALES', '[8, 16, 32]', 'ANCHOR_RATIOS', '[0.5,1,2]']
    elif (args.dataset == 'coco'):
        args.imdb_name = 'coco_2014_train+coco_2014_valminusminival'
        args.imdbval_name = 'coco_2014_minival'
        args.set_cfgs = ['ANCHOR_SCALES', '[4, 8, 16, 32]', 'ANCHOR_RATIOS', '[0.5,1,2]']
    elif (args.dataset == 'imagenet'):
        args.imdb_name = 'imagenet_train'
        args.imdbval_name = 'imagenet_val'
        args.set_cfgs = ['ANCHOR_SCALES', '[8, 16, 32]', 'ANCHOR_RATIOS', '[0.5,1,2]']
    elif (args.dataset == 'vg'):
        args.imdb_name = 'vg_150-50-50_minitrain'
        args.imdbval_name = 'vg_150-50-50_minival'
        args.set_cfgs = ['ANCHOR_SCALES', '[4, 8, 16, 32]', 'ANCHOR_RATIOS', '[0.5,1,2]']
    args.cfg_file = ('cfgs/{}_ls.yml'.format(args.net) if args.large_scale else 'cfgs/{}.yml'.format(args.net))
    if (args.cfg_file is not None):
        cfg_from_file(args.cfg_file)
    if (args.set_cfgs is not None):
        cfg_from_list(args.set_cfgs)
    print('Using config:')
    pprint.pprint(cfg)
    cfg.TRAIN.USE_FLIPPED = False
    (imdb, roidb, ratio_list, ratio_index) = combined_roidb(args.imdbval_name, False)
    imdb.competition_mode(on=True)
    imdb.set_gamma_altitude(args.gamma_altitude)
    imdb.set_gamma_angle(args.gamma_angle)
    imdb.set_gamma_weather(args.gamma_weather)
    imdb.set_epoch(args.checkepoch)
    imdb.set_ckpt(args.checkpoint)
    print('{:d} roidb entries'.format(len(roidb)))
    if ((args.gamma_altitude > 1e-10) and (args.gamma_angle > 1e-10) and (args.gamma_weather > 1e-10)):
        nuisance_type = 'A+V+W'
    elif ((args.gamma_altitude > 1e-10) and (args.gamma_angle > 1e-10)):
        nuisance_type = 'A+V'
    elif ((args.gamma_altitude > 1e-10) and (args.gamma_weather > 1e-10)):
        nuisance_type = 'A+W'
    elif (args.gamma_altitude > 1e-10):
        nuisance_type = 'A'
    elif (args.gamma_angle > 1e-10):
        nuisance_type = 'V'
    elif (args.gamma_weather > 1e-10):
        nuisance_type = 'W'
    else:
        nuisance_type = 'Baseline'
    if args.overall_eval:
        nuisance_type = 'Overall'
    model_dir = os.path.join(args.model_dir, nuisance_type, 'altitude={}_angle={}_weather={}'.format(str(args.gamma_altitude), str(args.gamma_angle), str(args.gamma_weather)))
    if (not os.path.exists(model_dir)):
        raise Exception(('There is no input directory for loading network from ' + model_dir))
    if (nuisance_type == 'Baseline'):
        load_name = os.path.join(model_dir, 'faster_rcnn_{}_{}_{}.pth'.format(args.checksession, args.checkepoch, args.checkpoint))
    else:
        load_name = os.path.join(model_dir, 'faster_rcnn_{}_{}_{}.pth'.format(args.checksession, args.checkepoch, args.checkpoint))
    if (args.net == 'vgg16'):
        fasterRCNN = vgg16(imdb.classes, pretrained=False, class_agnostic=args.class_agnostic)
    elif (args.net == 'res101'):
        fasterRCNN = resnet(imdb.classes, 101, pretrained=False, class_agnostic=args.class_agnostic)
    elif (args.net == 'res50'):
        fasterRCNN = resnet(imdb.classes, 50, pretrained=False, class_agnostic=args.class_agnostic)
    elif (args.net == 'res152'):
        fasterRCNN = resnet(imdb.classes, 152, pretrained=False, class_agnostic=args.class_agnostic)
    else:
        print('network is not defined')
        pdb.set_trace()
    fasterRCNN.create_architecture()
    print(('load checkpoint %s' % load_name))
    checkpoint = torch.load(load_name)
    for key in ['RCNN_angle_score.weight', 'RCNN_angle_score.bias', 'RCNN_altitude_score.weight', 'RCNN_altitude_score.bias', 'RCNN_weather_score.weight', 'RCNN_weather_score.bias']:
        if (key in checkpoint['model'].keys()):
            del checkpoint['model'][key]
    model_dict = fasterRCNN.state_dict()
    model_dict.update(checkpoint['model'])
    fasterRCNN.load_state_dict(model_dict)
    if ('pooling_mode' in checkpoint.keys()):
        cfg.POOLING_MODE = checkpoint['pooling_mode']
    print('load model successfully!')
    im_data = torch.FloatTensor(1)
    im_info = torch.FloatTensor(1)
    meta_data = torch.FloatTensor(1)
    num_boxes = torch.LongTensor(1)
    gt_boxes = torch.FloatTensor(1)
    if args.cuda:
        im_data = im_data.cuda()
        im_info = im_info.cuda()
        meta_data = meta_data.cuda()
        num_boxes = num_boxes.cuda()
        gt_boxes = gt_boxes.cuda()
    im_data = Variable(im_data)
    im_info = Variable(im_info)
    meta_data = Variable(meta_data)
    num_boxes = Variable(num_boxes)
    gt_boxes = Variable(gt_boxes)
    if args.cuda:
        cfg.CUDA = True
    if args.cuda:
        fasterRCNN.cuda()
    start = time.time()
    max_per_image = 100
    vis = args.vis
    if vis:
        thresh = 0.05
    else:
        thresh = 0.0
    save_name = 'faster_rcnn_10'
    num_images = len(imdb.image_index)
    all_boxes = [[[] for _ in xrange(num_images)] for _ in xrange(imdb.num_classes)]
    output_dir = get_output_dir(imdb, save_name)
    dataset = roibatchLoader(roidb, ratio_list, ratio_index, 1, imdb.num_classes, training=False, normalize=False)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=4, pin_memory=True)
    data_iter = iter(dataloader)
    _t = {'im_detect': time.time(), 'misc': time.time()}
    det_file = os.path.join(output_dir, 'detections.pkl')
    fasterRCNN.eval()
    empty_array = np.transpose(np.array([[], [], [], [], []]), (1, 0))
    for i in range(num_images):
        data = next(data_iter)
        im_data.data.resize_(data[0].size()).copy_(data[0])
        im_info.data.resize_(data[1].size()).copy_(data[1])
        meta_data.data.resize_(data[2].size()).copy_(data[2])
        gt_boxes.data.resize_(data[3].size()).copy_(data[3])
        num_boxes.data.resize_(data[4].size()).copy_(data[4])
        det_tic = time.time()
        (rois, cls_prob, bbox_pred, _, _, _) = fasterRCNN(im_data, im_info, meta_data, gt_boxes, num_boxes)
        scores = cls_prob.data
        boxes = rois.data[(:, :, 1:5)]
        if cfg.TEST.BBOX_REG:
            box_deltas = bbox_pred.data
            if cfg.TRAIN.BBOX_NORMALIZE_TARGETS_PRECOMPUTED:
                if args.class_agnostic:
                    box_deltas = ((box_deltas.view((- 1), 4) * torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_STDS).cuda()) + torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_MEANS).cuda())
                    box_deltas = box_deltas.view(1, (- 1), 4)
                else:
                    box_deltas = ((box_deltas.view((- 1), 4) * torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_STDS).cuda()) + torch.FloatTensor(cfg.TRAIN.BBOX_NORMALIZE_MEANS).cuda())
                    box_deltas = box_deltas.view(1, (- 1), (4 * len(imdb.classes)))
            pred_boxes = bbox_transform_inv(boxes, box_deltas, 1)
            pred_boxes = clip_boxes(pred_boxes, im_info.data, 1)
        else:
            pred_boxes = np.tile(boxes, (1, scores.shape[1]))
        pred_boxes /= data[1][0][2].item()
        scores = scores.squeeze()
        pred_boxes = pred_boxes.squeeze()
        det_toc = time.time()
        detect_time = (det_toc - det_tic)
        misc_tic = time.time()
        if vis:
            im = cv2.imread(imdb.image_path_at(i))
            im2show = np.copy(im)
        for j in xrange(1, imdb.num_classes):
            inds = torch.nonzero((scores[(:, j)] > thresh)).view((- 1))
            if (inds.numel() > 0):
                cls_scores = scores[(:, j)][inds]
                (_, order) = torch.sort(cls_scores, 0, True)
                if args.class_agnostic:
                    cls_boxes = pred_boxes[(inds, :)]
                else:
                    cls_boxes = pred_boxes[inds][(:, (j * 4):((j + 1) * 4))]
                cls_dets = torch.cat((cls_boxes, cls_scores.unsqueeze(1)), 1)
                cls_dets = cls_dets[order]
                keep = nms(cls_dets, cfg.TEST.NMS)
                cls_dets = cls_dets[keep.view((- 1)).long()]
                if vis:
                    im2show = vis_detections(im2show, imdb.classes[j], cls_dets.cpu().numpy(), 0.3)
                all_boxes[j][i] = cls_dets.cpu().numpy()
            else:
                all_boxes[j][i] = empty_array
        if (max_per_image > 0):
            image_scores = np.hstack([all_boxes[j][i][(:, (- 1))] for j in xrange(1, imdb.num_classes)])
            all_boxes[j][i] = np.concatenate((all_boxes[j][i], np.tile(meta_data.cpu().numpy(), (len(image_scores), 1))), axis=1)
            if (len(image_scores) > max_per_image):
                image_thresh = np.sort(image_scores)[(- max_per_image)]
                for j in xrange(1, imdb.num_classes):
                    keep = np.where((all_boxes[j][i][(:, (- 1))] >= image_thresh))[0]
                    all_boxes[j][i] = all_boxes[j][i][(keep, :)]
        misc_toc = time.time()
        nms_time = (misc_toc - misc_tic)
        sys.stdout.write('im_detect: {:d}/{:d} {:.3f}s {:.3f}s   \r'.format((i + 1), num_images, detect_time, nms_time))
        sys.stdout.flush()
        if vis:
            cv2.imwrite('result.png', im2show)
            pdb.set_trace()
    with open(det_file, 'wb') as f:
        pickle.dump(all_boxes, f, pickle.HIGHEST_PROTOCOL)
    print('Evaluating detections')
    imdb.evaluate_detections(all_boxes, output_dir, nuisance_type=nuisance_type, baseline_method=args.is_baseline_method, ovthresh=args.ovthresh)
    end = time.time()
    print(('test time: %0.4fs' % (end - start)))
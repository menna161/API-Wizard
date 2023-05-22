import sys
import json
import time
import datetime
import os
import random
import pickle
import numpy as np
import torch
from torch.autograd import Variable
import torch.optim as optim
from torch import nn
from sklearn.cluster import AffinityPropagation
from layers.modules import MultiBoxLoss
from layers import box_utils
from . import helpers
from data import VOCAnnotationTransform, VOCDetection, BaseTransform, VOC_CLASSES, detection_collate
from utils import augmentations
from . import uncertainty_helpers
import hdbscan


def bsas(args, all_detections, unlabeled_imgset, num_unlabeled_images, priors, iou_tresh=0.5):
    '\n    I find the best explanation of the algorithm to be equation 2 in:\n    Miller, Nicholson, Dayoub, Sunderhauf- Dropout Sampling for Robust Object Detection in Open-Set Conditions\n    Another noteworthy paper is:\n    Miller, Dayoub, Milford, Sunderhauf - Evaluating Merging Strategies for Sampling-based Uncertainty Techniques in Object Detection\n\n    :param args:\n    :param all_detections:\n    :param unlabeled_imgset:\n    :param num_unlabeled_images:\n    :param priors:\n    :param iou_tresh:\n    :return:\n    '
    print('Starting BSAS merging local time: ', datetime.datetime.now())
    if args.debug:
        iou_tresh = 0.5
    clusters = {}
    observations_means = {}
    observations_cov_0 = {}
    observations_cov_1 = {}
    observations_dist = {}
    detections_per_observation = {}
    total_num_observations = {}
    for (i, img) in enumerate(unlabeled_imgset):
        if (((i % 10) == 0) and (i != 0)):
            print('Merged image {:d}/{:d} trough {:d}/{:d}....'.format((i - 9), num_unlabeled_images, (i + 1), num_unlabeled_images))
            print('Local time: ', datetime.datetime.now())
        dets = [all_detections['detections'][ens, i, cl, :int(all_detections['num_boxes_per_class'][(ens, i)][cl].item()), :] for cl in range(1, args.num_classes) for ens in range(args.ensemble_size)]
        nonzero_dets = [det for det in dets if (det.ge(0.0).sum() > 0)]
        img_detections = torch.cat(nonzero_dets)
        observations_cov_0[img] = []
        observations_cov_1[img] = []
        observations_means[img] = []
        observations_dist[img] = []
        detections_per_observation[img] = []
        im_clusters = []
        first_cluster = True
        for (d, detection) in enumerate(img_detections):
            if first_cluster:
                im_clusters.append(detection.unsqueeze(dim=0).unsqueeze(dim=0).unsqueeze(dim=0))
                first_cluster = False
                continue
            for (j, cluster) in enumerate(im_clusters):
                iou_overlaps = box_utils.jaccard(detection[args.cfg['num_classes']:].unsqueeze(dim=0), cluster[:, :, :, args.cfg['num_classes']:].squeeze(dim=0).squeeze(dim=0))
                detection_fits_cluster = False
                if (iou_overlaps.ge(iou_tresh).sum() == cluster.shape[2]):
                    detection_fits_cluster = True
                    break
            if detection_fits_cluster:
                im_clusters[j] = torch.cat((im_clusters[j], detection.unsqueeze(dim=0).unsqueeze(dim=0).unsqueeze(dim=0)), dim=2)
            else:
                im_clusters.append(detection.unsqueeze(dim=0).unsqueeze(dim=0).unsqueeze(dim=0))
        num_obs = 0
        for cluster in im_clusters:
            if (cluster.shape[2] > 1):
                num_obs += 1
                (averaged_bounding_boxes, cov_0, cov_1) = uncertainty_helpers.means_covs_observation(cluster[:, :, :, (- 4):])
                observations_cov_0[img].append(cov_0)
                observations_cov_1[img].append(cov_1)
                observations_means[img].append(averaged_bounding_boxes)
                observations_dist[img].append(cluster[:, :, :, :args.cfg['num_classes']].mean(dim=2))
                detections_per_observation[img].append(cluster.shape[2])
        total_num_observations[img] = num_obs
    print('Finished BSAS merging, local time: ', datetime.datetime.now())
    return (observations_means, observations_cov_0, observations_cov_1, observations_dist, total_num_observations, detections_per_observation)

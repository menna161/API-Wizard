import warnings
import numpy as np, os, sys, pandas as pd, csv, random, datetime
import torch, torch.nn as nn
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle as pkl
from sklearn import metrics
from sklearn.cluster import KMeans
from scipy.spatial.distance import squareform, pdist, cdist
import losses as losses
from scipy.special import comb
from graphviz import Digraph


def f1_score(model_generated_cluster_labels, target_labels, feature_coll, computed_centroids):
    '\n    NOTE: MOSTLY ADAPTED FROM https://github.com/wzzheng/HDML on Hardness-Aware Deep Metric Learning.\n\n    Args:\n        model_generated_cluster_labels: np.ndarray [n_samples x 1], Cluster labels computed on top of data embeddings.\n        target_labels:                  np.ndarray [n_samples x 1], ground truth labels for each data sample.\n        feature_coll:                   np.ndarray [n_samples x embed_dim], total data embedding made by network.\n        computed_centroids:             np.ndarray [num_cluster=num_classes x embed_dim], cluster coordinates\n    Returns:\n        float, F1-score\n    '
    from scipy.special import comb
    d = np.zeros(len(feature_coll))
    for i in range(len(feature_coll)):
        d[i] = np.linalg.norm((feature_coll[(i, :)] - computed_centroids[(model_generated_cluster_labels[i], :)]))
    labels_pred = np.zeros(len(feature_coll))
    for i in np.unique(model_generated_cluster_labels):
        index = np.where((model_generated_cluster_labels == i))[0]
        ind = np.argmin(d[index])
        cid = index[ind]
        labels_pred[index] = cid
    N = len(target_labels)
    avail_labels = np.unique(target_labels)
    n_labels = len(avail_labels)
    count_cluster = np.zeros(n_labels)
    for i in range(n_labels):
        count_cluster[i] = len(np.where((target_labels == avail_labels[i]))[0])
    keys = np.unique(labels_pred)
    num_item = len(keys)
    values = range(num_item)
    item_map = dict()
    for i in range(len(keys)):
        item_map.update([(keys[i], values[i])])
    count_item = np.zeros(num_item)
    for i in range(N):
        index = item_map[labels_pred[i]]
        count_item[index] = (count_item[index] + 1)
    tp_fp = 0
    for k in range(n_labels):
        if (count_cluster[k] > 1):
            tp_fp = (tp_fp + comb(count_cluster[k], 2))
    tp = 0
    for k in range(n_labels):
        member = np.where((target_labels == avail_labels[k]))[0]
        member_ids = labels_pred[member]
        count = np.zeros(num_item)
        for j in range(len(member)):
            index = item_map[member_ids[j]]
            count[index] = (count[index] + 1)
        for i in range(num_item):
            if (count[i] > 1):
                tp = (tp + comb(count[i], 2))
    fp = (tp_fp - tp)
    count = 0
    for j in range(num_item):
        if (count_item[j] > 1):
            count = (count + comb(count_item[j], 2))
    fn = (count - tp)
    beta = 1
    P = (tp / (tp + fp))
    R = (tp / (tp + fn))
    F1 = (((((beta * beta) + 1) * P) * R) / (((beta * beta) * P) + R))
    return F1

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


def eval_metrics_one_dataset(model, test_dataloader, device, k_vals, opt):
    '\n    Compute evaluation metrics on test-dataset, e.g. NMI, F1 and Recall @ k.\n\n    Args:\n        model:              PyTorch network, network to compute evaluation metrics for.\n        test_dataloader:    PyTorch Dataloader, dataloader for test dataset, should have no shuffling and correct processing.\n        device:             torch.device, Device to run inference on.\n        k_vals:             list of int, Recall values to compute\n        opt:                argparse.Namespace, contains all training-specific parameters.\n    Returns:\n        F1 score (float), NMI score (float), recall_at_k (list of float), data embedding (np.ndarray)\n    '
    torch.cuda.empty_cache()
    _ = model.eval()
    n_classes = len(test_dataloader.dataset.avail_classes)
    with torch.no_grad():
        (target_labels, feature_coll) = ([], [])
        final_iter = tqdm(test_dataloader, desc='Computing Evaluation Metrics...')
        image_paths = [x[0] for x in test_dataloader.dataset.image_list]
        for (idx, inp) in enumerate(final_iter):
            (input_img, target) = (inp[(- 1)], inp[0])
            target_labels.extend(target.numpy().tolist())
            out = model(input_img.to(device))
            feature_coll.extend(out.cpu().detach().numpy().tolist())
        target_labels = np.hstack(target_labels).reshape((- 1), 1)
        feature_coll = np.vstack(feature_coll).astype('float32')
        torch.cuda.empty_cache()
        kmeans = KMeans(n_clusters=n_classes, random_state=0).fit(feature_coll)
        model_generated_cluster_labels = kmeans.labels_
        computed_centroids = kmeans.cluster_centers_
        NMI = metrics.cluster.normalized_mutual_info_score(model_generated_cluster_labels.reshape((- 1)), target_labels.reshape((- 1)))
        k_closest_points = squareform(pdist(feature_coll)).argsort(1)[(:, :int((np.max(k_vals) + 1)))]
        k_closest_classes = target_labels.reshape((- 1))[k_closest_points[(:, 1:)]]
        recall_all_k = []
        for k in k_vals:
            recall_at_k = (np.sum([1 for (target, recalled_predictions) in zip(target_labels, k_closest_classes) if (target in recalled_predictions[:k])]) / len(target_labels))
            recall_all_k.append(recall_at_k)
        F1 = f1_score(model_generated_cluster_labels, target_labels, feature_coll, computed_centroids)
    return (F1, NMI, recall_all_k, feature_coll)

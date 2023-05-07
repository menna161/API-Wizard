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
from sklearn import cluster
import faiss
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
        cpu_cluster_index = faiss.IndexFlatL2(feature_coll.shape[(- 1)])
        kmeans = faiss.Clustering(feature_coll.shape[(- 1)], n_classes)
        kmeans.niter = 20
        kmeans.min_points_per_centroid = 1
        kmeans.max_points_per_centroid = 1000000000
        kmeans.train(feature_coll, cpu_cluster_index)
        computed_centroids = faiss.vector_float_to_array(kmeans.centroids).reshape(n_classes, feature_coll.shape[(- 1)])
        faiss_search_index = faiss.IndexFlatL2(computed_centroids.shape[(- 1)])
        faiss_search_index.add(computed_centroids)
        (_, model_generated_cluster_labels) = faiss_search_index.search(feature_coll, 1)
        NMI = metrics.cluster.normalized_mutual_info_score(model_generated_cluster_labels.reshape((- 1)), target_labels.reshape((- 1)))
        faiss_search_index = faiss.IndexFlatL2(feature_coll.shape[(- 1)])
        faiss_search_index.add(feature_coll)
        (_, k_closest_points) = faiss_search_index.search(feature_coll, int((np.max(k_vals) + 1)))
        k_closest_classes = target_labels.reshape((- 1))[k_closest_points[(:, 1:)]]
        recall_all_k = []
        for k in k_vals:
            recall_at_k = (np.sum([1 for (target, recalled_predictions) in zip(target_labels, k_closest_classes) if (target in recalled_predictions[:k])]) / len(target_labels))
            recall_all_k.append(recall_at_k)
        F1 = f1_score(model_generated_cluster_labels, target_labels, feature_coll, computed_centroids)
    return (F1, NMI, recall_all_k, feature_coll)

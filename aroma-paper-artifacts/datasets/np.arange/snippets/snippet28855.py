import warnings
import torch, random, itertools as it, numpy as np, faiss, random
from tqdm import tqdm
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from PIL import Image


def npairsampling(self, batch, labels):
    "\n        This methods finds N-Pairs in a batch given by the classes provided in labels in the\n        creation fashion proposed in 'Improved Deep Metric Learning with Multi-class N-pair Loss Objective'.\n\n        Args:\n            batch:  np.ndarray or torch.Tensor, batch-wise embedded training samples.\n            labels: np.ndarray or torch.Tensor, ground truth labels corresponding to batch.\n        Returns:\n            list of sampled data tuples containing reference indices to the position IN THE BATCH.\n        "
    if isinstance(labels, torch.Tensor):
        labels = labels.detach().cpu().numpy()
    (label_set, count) = np.unique(labels, return_counts=True)
    label_set = label_set[(count >= 2)]
    pos_pairs = np.array([np.random.choice(np.where((labels == x))[0], 2, replace=False) for x in label_set])
    neg_tuples = []
    for idx in range(len(pos_pairs)):
        neg_tuples.append(pos_pairs[(np.delete(np.arange(len(pos_pairs)), idx), 1)])
    neg_tuples = np.array(neg_tuples)
    sampled_npairs = [[a, p, *list(neg)] for ((a, p), neg) in zip(pos_pairs, neg_tuples)]
    return sampled_npairs

import warnings
import torch, random, itertools as it, numpy as np, faiss, random
from tqdm import tqdm
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from PIL import Image


def randomsampling(self, batch, labels):
    '\n        This methods finds all available triplets in a batch given by the classes provided in labels, and randomly\n        selects <len(batch)> triplets.\n\n        Args:\n            batch:  np.ndarray or torch.Tensor, batch-wise embedded training samples.\n            labels: np.ndarray or torch.Tensor, ground truth labels corresponding to batch.\n        Returns:\n            list of sampled data tuples containing reference indices to the position IN THE BATCH.\n        '
    if isinstance(labels, torch.Tensor):
        labels = labels.detach().numpy()
    unique_classes = np.unique(labels)
    indices = np.arange(len(batch))
    class_dict = {i: indices[(labels == i)] for i in unique_classes}
    sampled_triplets = [list(it.product([x], [x], [y for y in unique_classes if (x != y)])) for x in unique_classes]
    sampled_triplets = [x for y in sampled_triplets for x in y]
    sampled_triplets = [[x for x in list(it.product(*[class_dict[j] for j in i])) if (x[0] != x[1])] for i in sampled_triplets]
    sampled_triplets = [x for y in sampled_triplets for x in y]
    sampled_triplets = random.sample(sampled_triplets, batch.shape[0])
    return sampled_triplets

import warnings
import torch, random, itertools as it, numpy as np, faiss, random
from tqdm import tqdm
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from PIL import Image


def __init__(self, inp_dim, n_classes):
    '\n        Basic Cross Entropy Loss for reference. Can be useful.\n        Contains its own mapping network, so the actual network can remain untouched.\n\n        Args:\n            inp_dim:   int, embedding dimension of network.\n            n_classes: int, number of target classes.\n        Returns:\n            Nothing!\n        '
    super(CEClassLoss, self).__init__()
    self.mapper = torch.nn.Sequential(torch.nn.Linear(inp_dim, n_classes))
    self.ce_loss = torch.nn.CrossEntropyLoss()

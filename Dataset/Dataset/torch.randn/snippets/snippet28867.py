import warnings
import torch, random, itertools as it, numpy as np, faiss, random
from tqdm import tqdm
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from PIL import Image


def __init__(self, num_proxies, embedding_dim):
    "\n        Basic ProxyNCA Loss as proposed in 'No Fuss Distance Metric Learning using Proxies'.\n\n        Args:\n            num_proxies:     int, number of proxies to use to estimate data groups. Usually set to number of classes.\n            embedding_dim:   int, Required to generate initial proxies which are the same size as the actual data embeddings.\n        Returns:\n            Nothing!\n        "
    super(ProxyNCALoss, self).__init__()
    self.num_proxies = num_proxies
    self.embedding_dim = embedding_dim
    self.PROXIES = torch.nn.Parameter((torch.randn(num_proxies, self.embedding_dim) / 8))
    self.all_classes = torch.arange(num_proxies)

from pathlib import Path
from argparse import ArgumentParser
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import umap
from tsne import bh_sne
from sklearn.decomposition import IncrementalPCA


def plot_umap(generator):
    X = next(generator(return_full=True))
    X_2d = umap.UMAP().fit_transform(X)
    plt.scatter(X_2d[(:, 0)], X_2d[(:, 1)])
    plt.show()
    return X_2d

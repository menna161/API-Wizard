import argparse
from glob import glob
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from data_gen import CHAR_IDX
from utils import LogicSeq
from models import build_model
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from mpl_toolkits.mplot3d import Axes3D


def get_pca(context, model, dims=2):
    'Plot the PCA of predicate embeddings.'
    dgen = LogicSeq([[(context, 'z(z).', 0)]], 1, train=False, shuffle=False, zeropad=False)
    embds = model.predict_generator(dgen)
    embds = embds.squeeze()
    pca = PCA(dims)
    embds = pca.fit_transform(embds)
    print('TRANSFORMED:', embds)
    print('VAR:', pca.explained_variance_ratio_)
    return embds

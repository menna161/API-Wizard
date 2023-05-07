from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np


def visualize_distribution(X, prediction, score, path=None):
    '\n    Visualize the original density distribution of the data in 2-dimension space.\n\n    Parameters\n    ----------\n    X: numpy array of shape (n_test, n_features)\n        Test data.\n    prediction: numpy array of shape (n_test, )\n        The prediction result of the test data.\n    score: numpy array of shape (n_test, )\n        The outlier score of the test data.\n    path: string\n        The saving path for result figures.\n    '
    sns.set(style='ticks')
    X = X.to_numpy()
    X_embedding = TSNE(n_components=2).fit_transform(X)
    sns_plot = sns.jointplot(X_embedding[(:, 1)], X_embedding[(:, 0)], kind='kde', space=0, color='#4CB391')
    if path:
        sns_plot.savefig((path + '/distribution.png'))
    plt.show()

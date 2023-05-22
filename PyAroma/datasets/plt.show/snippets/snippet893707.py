from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np


def visualize_distribution_static(X, prediction, score, path=None):
    '\n    Visualize the original distribution of the data in 2-dimension space, which outliers/inliers are colored as differnet scatter plot.\n\n    Parameters\n    ----------\n    X: numpy array of shape (n_test, n_features)\n        Test data.\n    prediction: numpy array of shape (n_test, )\n        The prediction result of the test data.\n    score: umpy array of shape (n_test, )\n        The outlier score of the test data.\n    path: string\n        The saving path for result figures.\n    '
    sns.set(style='darkgrid')
    X = X.to_numpy()
    X_embedding = TSNE(n_components=2).fit_transform(X)
    outlier_label = []
    for i in range(len(X_embedding)):
        if (prediction[i] == 1):
            outlier_label.append('inlier')
        else:
            outlier_label.append('outlier')
    X_outlier = pd.DataFrame({'x_emb': X_embedding[(:, 0)], 'y_emb': X_embedding[(:, 1)], 'outlier_label': np.array(outlier_label), 'score': np.array(score)})
    new_sns = sns.scatterplot(x='x_emb', y='y_emb', hue='score', sizes=20, palette='BuGn_r', legend=False, data=X_outlier)
    if path:
        new_sns.get_figure().savefig((path + '/distribution_withoutlier.png'))
    plt.show()

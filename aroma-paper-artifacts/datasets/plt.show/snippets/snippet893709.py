from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np


def visualize_outlierscore(value, label, contamination, path=None):
    '\n    Visualize the predicted outlier score.\n\n    Parameters\n    ----------\n    value: numpy array of shape (n_test, )\n        The outlier score of the test data.\n    label: numpy array of shape (n_test, )\n        The label of test data produced by the algorithm.\n    contamination : float in (0., 0.5), optional (default=0.1)\n        The amount of contamination of the data set,\n        i.e. the proportion of outliers in the data set. Used when fitting to\n        define the threshold on the decision function.\n    path: string\n        The saving path for result figures.\n    '
    sns.set(style='darkgrid')
    ts = np.arange(len(value))
    outlier_label = []
    for i in range(len(ts)):
        if (label[i] == 1):
            outlier_label.append('inlier')
        else:
            outlier_label.append('outlier')
    X_outlier = pd.DataFrame({'ts': ts, 'Outlier_score': value, 'outlier_label': np.array(outlier_label)})
    pal = dict(inlier='#4CB391', outlier='gray')
    g = sns.FacetGrid(X_outlier, hue='outlier_label', palette=pal, height=5)
    g.map(plt.scatter, 'ts', 'Outlier_score', s=30, alpha=0.7, linewidth=0.5, edgecolor='white')
    ranking = np.sort(value)
    threshold = ranking[int(((1 - contamination) * len(ranking)))]
    plt.hlines(threshold, xmin=0, xmax=(len(X_outlier) - 1), colors='g', zorder=100, label='Threshold')
    threshold = ranking[int((contamination * len(ranking)))]
    plt.hlines(threshold, xmin=0, xmax=(len(X_outlier) - 1), colors='g', zorder=100, label='Threshold2')
    if path:
        plt.savefig((path + '/visualize_outlierscore.png'))
    plt.show()

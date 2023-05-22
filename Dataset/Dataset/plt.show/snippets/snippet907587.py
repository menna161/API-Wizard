import itertools
import scipy.spatial.distance as distance
import numpy as np
import copy
import pickle
from scipy.special import xlogy
import seaborn as sns
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import pandas as pd
import matplotlib.pyplot as plt


def plot_distance_matrix(embeddings, labels=None, distance='cosine'):
    import seaborn as sns
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import squareform
    import pandas as pd
    import matplotlib.pyplot as plt
    distance_matrix = pdist(embeddings, distance=distance)
    cond_distance_matrix = squareform(distance_matrix, checks=False)
    linkage_matrix = linkage(cond_distance_matrix, method='complete', optimal_ordering=True)
    if (labels is not None):
        distance_matrix = pd.DataFrame(distance_matrix, index=labels, columns=labels)
    sns.clustermap(distance_matrix, row_linkage=linkage_matrix, col_linkage=linkage_matrix, cmap='viridis_r')
    plt.show()

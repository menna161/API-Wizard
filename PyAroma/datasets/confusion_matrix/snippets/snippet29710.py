import numpy as np


def compute_confusion_matrix(num_clusters, clustered_points_algo, sorted_indices_algo):
    '\n    computes a confusion matrix and returns it\n    '
    seg_len = 400
    true_confusion_matrix = np.zeros([num_clusters, num_clusters])
    for point in range(len(clustered_points_algo)):
        cluster = clustered_points_algo[point]
        num = (int((sorted_indices_algo[point] / seg_len)) % num_clusters)
        true_confusion_matrix[(int(num), int(cluster))] += 1
    return true_confusion_matrix

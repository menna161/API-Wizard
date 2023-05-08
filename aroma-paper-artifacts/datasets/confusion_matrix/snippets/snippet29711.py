import numpy as np


def computeF1_macro(confusion_matrix, matching, num_clusters):
    '\n    computes the macro F1 score\n    confusion matrix : requres permutation\n    matching according to which matrix must be permuted\n    '
    permuted_confusion_matrix = np.zeros([num_clusters, num_clusters])
    for cluster in range(num_clusters):
        matched_cluster = matching[cluster]
        permuted_confusion_matrix[(:, cluster)] = confusion_matrix[(:, matched_cluster)]
    F1_score = 0
    for cluster in range(num_clusters):
        TP = permuted_confusion_matrix[(cluster, cluster)]
        FP = (np.sum(permuted_confusion_matrix[(:, cluster)]) - TP)
        FN = (np.sum(permuted_confusion_matrix[(cluster, :)]) - TP)
        precision = (TP / (TP + FP))
        recall = (TP / (TP + FN))
        f1 = stats.hmean([precision, recall])
        F1_score += f1
    F1_score /= num_clusters
    return F1_score

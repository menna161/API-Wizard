import numpy as np
import math, time, collections, os, errno, sys, code, random
import matplotlib
import matplotlib.pyplot as plt
from sklearn import mixture
from sklearn.cluster import KMeans
import pandas as pd
from multiprocessing import Pool
from src.TICC_helper import *
from src.admm_solver import ADMMSolver


def compute_matches(self, train_confusion_matrix_EM, train_confusion_matrix_GMM, train_confusion_matrix_kmeans):
    matching_Kmeans = find_matching(train_confusion_matrix_kmeans)
    matching_GMM = find_matching(train_confusion_matrix_GMM)
    matching_EM = find_matching(train_confusion_matrix_EM)
    correct_e_m = 0
    correct_g_m_m = 0
    correct_k_means = 0
    for cluster in range(self.number_of_clusters):
        matched_cluster_e_m = matching_EM[cluster]
        matched_cluster_g_m_m = matching_GMM[cluster]
        matched_cluster_k_means = matching_Kmeans[cluster]
        correct_e_m += train_confusion_matrix_EM[(cluster, matched_cluster_e_m)]
        correct_g_m_m += train_confusion_matrix_GMM[(cluster, matched_cluster_g_m_m)]
        correct_k_means += train_confusion_matrix_kmeans[(cluster, matched_cluster_k_means)]
    return (matching_EM, matching_GMM, matching_Kmeans)

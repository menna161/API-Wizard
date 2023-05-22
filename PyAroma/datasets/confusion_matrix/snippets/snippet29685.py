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


def fit(self, input_file):
    '\n        Main method for TICC solver.\n        Parameters:\n            - input_file: location of the data file\n        '
    assert (self.maxIters > 0)
    self.log_parameters()
    (times_series_arr, time_series_rows_size, time_series_col_size) = self.load_data(input_file)
    str_NULL = self.prepare_out_directory()
    training_indices = getTrainTestSplit(time_series_rows_size, self.num_blocks, self.window_size)
    num_train_points = len(training_indices)
    complete_D_train = self.stack_training_data(times_series_arr, time_series_col_size, num_train_points, training_indices)
    gmm = mixture.GaussianMixture(n_components=self.number_of_clusters, covariance_type='full')
    gmm.fit(complete_D_train)
    clustered_points = gmm.predict(complete_D_train)
    gmm_clustered_pts = (clustered_points + 0)
    kmeans = KMeans(n_clusters=self.number_of_clusters, random_state=0).fit(complete_D_train)
    clustered_points_kmeans = kmeans.labels_
    kmeans_clustered_pts = kmeans.labels_
    train_cluster_inverse = {}
    log_det_values = {}
    computed_covariance = {}
    cluster_mean_info = {}
    cluster_mean_stacked_info = {}
    old_clustered_points = None
    empirical_covariances = {}
    pool = Pool(processes=self.num_proc)
    for iters in range(self.maxIters):
        print('\n\n\nITERATION ###', iters)
        train_clusters_arr = collections.defaultdict(list)
        for (point, cluster_num) in enumerate(clustered_points):
            train_clusters_arr[cluster_num].append(point)
        len_train_clusters = {k: len(train_clusters_arr[k]) for k in range(self.number_of_clusters)}
        opt_res = self.train_clusters(cluster_mean_info, cluster_mean_stacked_info, complete_D_train, empirical_covariances, len_train_clusters, time_series_col_size, pool, train_clusters_arr)
        self.optimize_clusters(computed_covariance, len_train_clusters, log_det_values, opt_res, train_cluster_inverse)
        old_computed_covariance = computed_covariance
        print('UPDATED THE OLD COVARIANCE')
        self.trained_model = {'cluster_mean_info': cluster_mean_info, 'computed_covariance': computed_covariance, 'cluster_mean_stacked_info': cluster_mean_stacked_info, 'complete_D_train': complete_D_train, 'time_series_col_size': time_series_col_size}
        clustered_points = self.predict_clusters()
        new_train_clusters = collections.defaultdict(list)
        for (point, cluster) in enumerate(clustered_points):
            new_train_clusters[cluster].append(point)
        len_new_train_clusters = {k: len(new_train_clusters[k]) for k in range(self.number_of_clusters)}
        before_empty_cluster_assign = clustered_points.copy()
        if (iters != 0):
            cluster_norms = [(np.linalg.norm(old_computed_covariance[(self.number_of_clusters, i)]), i) for i in range(self.number_of_clusters)]
            norms_sorted = sorted(cluster_norms, reverse=True)
            valid_clusters = [cp[1] for cp in norms_sorted if (len_new_train_clusters[cp[1]] != 0)]
            counter = 0
            for cluster_num in range(self.number_of_clusters):
                if (len_new_train_clusters[cluster_num] == 0):
                    cluster_selected = valid_clusters[counter]
                    counter = ((counter + 1) % len(valid_clusters))
                    print('cluster that is zero is:', cluster_num, 'selected cluster instead is:', cluster_selected)
                    start_point = np.random.choice(new_train_clusters[cluster_selected])
                    for i in range(0, self.cluster_reassignment):
                        point_to_move = (start_point + i)
                        if (point_to_move >= len(clustered_points)):
                            break
                        clustered_points[point_to_move] = cluster_num
                        computed_covariance[(self.number_of_clusters, cluster_num)] = old_computed_covariance[(self.number_of_clusters, cluster_selected)]
                        cluster_mean_stacked_info[(self.number_of_clusters, cluster_num)] = complete_D_train[(point_to_move, :)]
                        cluster_mean_info[(self.number_of_clusters, cluster_num)] = complete_D_train[(point_to_move, :)][((self.window_size - 1) * time_series_col_size):(self.window_size * time_series_col_size)]
        for cluster_num in range(self.number_of_clusters):
            print('length of cluster #', cluster_num, '-------->', sum([(x == cluster_num) for x in clustered_points]))
        self.write_plot(clustered_points, str_NULL, training_indices)
        train_confusion_matrix_EM = compute_confusion_matrix(self.number_of_clusters, clustered_points, training_indices)
        train_confusion_matrix_GMM = compute_confusion_matrix(self.number_of_clusters, gmm_clustered_pts, training_indices)
        train_confusion_matrix_kmeans = compute_confusion_matrix(self.number_of_clusters, kmeans_clustered_pts, training_indices)
        (matching_EM, matching_GMM, matching_Kmeans) = self.compute_matches(train_confusion_matrix_EM, train_confusion_matrix_GMM, train_confusion_matrix_kmeans)
        print('\n\n\n')
        if np.array_equal(old_clustered_points, clustered_points):
            print('\n\n\n\nCONVERGED!!! BREAKING EARLY!!!')
            break
        old_clustered_points = before_empty_cluster_assign
    if (pool is not None):
        pool.close()
        pool.join()
    train_confusion_matrix_EM = compute_confusion_matrix(self.number_of_clusters, clustered_points, training_indices)
    train_confusion_matrix_GMM = compute_confusion_matrix(self.number_of_clusters, gmm_clustered_pts, training_indices)
    train_confusion_matrix_kmeans = compute_confusion_matrix(self.number_of_clusters, clustered_points_kmeans, training_indices)
    self.compute_f_score(matching_EM, matching_GMM, matching_Kmeans, train_confusion_matrix_EM, train_confusion_matrix_GMM, train_confusion_matrix_kmeans)
    if self.compute_BIC:
        bic = computeBIC(self.number_of_clusters, time_series_rows_size, clustered_points, train_cluster_inverse, empirical_covariances)
        return (clustered_points, train_cluster_inverse, bic)
    return (clustered_points, train_cluster_inverse)

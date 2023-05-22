import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import numba as nb
import multiprocessing
import torch_scatter


@nb.jit('b1[:](f4[:,:],i4)', nopython=True, cache=True)
def nb_greedy_FPS(xyz, K):
    start_element = 0
    sample_num = xyz.shape[0]
    sum_vec = np.zeros((sample_num, 1), dtype=np.float32)
    xyz_sq = (xyz ** 2)
    for j in range(sample_num):
        sum_vec[(j, 0)] = np.sum(xyz_sq[(j, :)])
    pairwise_distance = ((sum_vec + np.transpose(sum_vec)) - (2 * np.dot(xyz, np.transpose(xyz))))
    candidates_ind = np.zeros((sample_num,), dtype=np.bool_)
    candidates_ind[start_element] = True
    remain_ind = np.ones((sample_num,), dtype=np.bool_)
    remain_ind[start_element] = False
    all_ind = np.arange(sample_num)
    for i in range(1, K):
        if (i == 1):
            min_remain_pt_dis = pairwise_distance[(:, start_element)]
            min_remain_pt_dis = min_remain_pt_dis[remain_ind]
        else:
            cur_dis = pairwise_distance[(remain_ind, :)]
            cur_dis = cur_dis[(:, candidates_ind)]
            min_remain_pt_dis = np.zeros((cur_dis.shape[0],), dtype=np.float32)
            for j in range(cur_dis.shape[0]):
                min_remain_pt_dis[j] = np.min(cur_dis[(j, :)])
        next_ind_in_remain = np.argmax(min_remain_pt_dis)
        next_ind = all_ind[remain_ind][next_ind_in_remain]
        candidates_ind[next_ind] = True
        remain_ind[next_ind] = False
    return candidates_ind

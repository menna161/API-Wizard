import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def test_forward(self, prob, embedding, param, mask_threshold):
    '\n        :param prob: probability of planar, tensor with size (1, h, w)\n        :param embedding: tensor with size (2, h, w)\n        :param mask_threshold: threshold of planar region\n        :return: clustering results: numpy array with shape (h, w),\n                 sampled segmentation results, tensor with size (N, K) where N is sample size, K is cluster number, row sum to 1\n                 sample_params, tensor with size (3, N), sampled params\n        '
    (c, h, w) = embedding.size()
    embedding = embedding.view(c, (h * w)).t()
    prob = prob.view((h * w), 1)
    param = param.view(3, (h * w))
    rand_index = np.random.choice(np.arange(0, (h * w))[(prob.cpu().numpy().reshape((- 1)) > mask_threshold)], self.sample_num)
    sample_embedding = embedding[rand_index]
    sample_prob = prob[rand_index]
    sample_param = param[(:, rand_index)]
    seed_point = self.generate_seed(sample_embedding, self.anchor_num)
    seed_point = self.filter_seed(sample_embedding, sample_prob, seed_point, bandwidth=self.bandwidth, min_count=3)
    with torch.no_grad():
        for iter in range(self.test_iter):
            seed_point = self.shift(sample_embedding, sample_prob, seed_point, self.bandwidth)
    seed_point = self.filter_seed(sample_embedding, sample_prob, seed_point, bandwidth=self.bandwidth, min_count=10)
    center = self.merge_center(seed_point, bandwidth=self.bandwidth)
    segmentation = self.cluster(embedding, center)
    sampled_segmentation = segmentation[rand_index]
    return (segmentation, sampled_segmentation, sample_param)

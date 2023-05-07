import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def bin_shift(self, prob, embedding, param, gt_seg, bandwidth):
    '\n        discrete seeding mean shift in training stage\n        :param prob: tensor with size (1, h, w) indicate probability of being plane\n        :param embedding: tensor with size (2, h, w)\n        :param param: tensor with size (3, h, w)\n        :param gt_seg: ground truth instance segmentation, used for sampling planar embeddings\n        :param bandwidth: float\n        :return: segmentation results, tensor with size (h*w, K), K is cluster number, row sum to 1\n                 sampled segmentation results, tensor with size (N, K) where N is sample size, K is cluster number, row sum to 1\n                center, tensor with size (K, 2) cluster center in embedding space\n                sample_prob, tensor with size (N, 1) sampled probability\n                sample_seg, tensor with size (N, 1) sampled ground truth instance segmentation\n                sample_params, tensor with size (3, N), sampled params\n        '
    (c, h, w) = embedding.size()
    embedding = embedding.view(c, (h * w)).t()
    param = param.view(3, (h * w))
    prob = prob.view((h * w), 1)
    seg = gt_seg.view((- 1))
    rand_index = np.random.choice(np.arange(0, (h * w))[(seg.cpu().numpy() != 20)], self.sample_num)
    sample_embedding = embedding[rand_index]
    sample_prob = prob[rand_index]
    sample_param = param[(:, rand_index)]
    seed_point = self.generate_seed(sample_embedding, self.anchor_num)
    seed_point = self.filter_seed(sample_embedding, sample_prob, seed_point, bandwidth=self.bandwidth, min_count=3)
    if (torch.numel(seed_point) <= 0):
        return (None, None, None, None, None, None)
    with torch.no_grad():
        for iter in range(self.train_iter):
            seed_point = self.shift(sample_embedding, sample_prob, seed_point, self.bandwidth)
    seed_point = self.filter_seed(sample_embedding, sample_prob, seed_point, bandwidth=self.bandwidth, min_count=10)
    if (torch.numel(seed_point) <= 0):
        return (None, None, None, None, None, None)
    center = self.merge_center(seed_point, bandwidth=self.bandwidth)
    segmentation = self.cluster(embedding, center)
    sampled_segmentation = segmentation[rand_index]
    return (segmentation, sampled_segmentation, center, sample_prob, seg[rand_index].view((- 1), 1), sample_param)

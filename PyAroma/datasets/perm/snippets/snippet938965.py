import torch
from extensions.gridding import Gridding, GriddingReverse
from extensions.cubic_feature_sampling import CubicFeatureSampling


def forward(self, pred_cloud, partial_cloud=None):
    if (partial_cloud is not None):
        pred_cloud = torch.cat([partial_cloud, pred_cloud], dim=1)
    _ptcloud = torch.split(pred_cloud, 1, dim=0)
    ptclouds = []
    for p in _ptcloud:
        non_zeros = torch.sum(p, dim=2).ne(0)
        p = p[non_zeros].unsqueeze(dim=0)
        n_pts = p.size(1)
        if (n_pts < self.n_points):
            rnd_idx = torch.cat([torch.randint(0, n_pts, (self.n_points,))])
        else:
            rnd_idx = torch.randperm(p.size(1))[:self.n_points]
        ptclouds.append(p[(:, rnd_idx, :)])
    return torch.cat(ptclouds, dim=0).contiguous()

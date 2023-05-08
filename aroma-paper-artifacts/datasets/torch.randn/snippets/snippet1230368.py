import torch
import torch.nn.functional as F
from data.base import sample_partitions
from data.mvn import MultivariateNormalDiag
import math


def sample_warped_mog(B, N, K, radial_std=0.4, tangential_std=0.1, alpha=5.0, onehot=True, rand_N=True, rand_K=True, device='cpu'):
    batch = sample_mog(B, N, K, mvn=MultivariateNormalDiag(1), alpha=alpha, onehot=False, rand_N=rand_N, rand_K=rand_K, device=device)
    (r, labels) = (batch['X'], batch['labels'])
    N = r.shape[1]
    r = (((2 * math.pi) * radial_std) * r)
    a = torch.gather((2 * torch.randn(B, K).to(device)), 1, labels).unsqueeze((- 1))
    b = torch.gather((2 * torch.randn(B, K).to(device)), 1, labels).unsqueeze((- 1))
    cos = r.cos()
    sin = r.sin()
    x = (a * cos)
    y = (b * sin)
    dx = (b * cos)
    dy = (a * sin)
    norm = (dx.pow(2) + dy.pow(2)).sqrt()
    t = (tangential_std * torch.randn(B, N, 1).to(device))
    dx = ((t * dx) / norm)
    dy = ((t * dy) / norm)
    x = (x + dx)
    y = (y + dy)
    E = torch.cat([x, y], (- 1))
    rho = torch.gather(((2 * math.pi) * torch.rand(B, K).to(device)), 1, labels)
    rot = torch.stack([rho.cos(), (- rho.sin()), rho.sin(), rho.cos()], (- 1))
    rot = rot.reshape(B, (- 1), 2, 2)
    X = torch.einsum('bni,bnij->bnj', E, rot)
    mu = torch.gather((min(K, 4.0) * torch.randn(B, K, 2).to(device)), 1, labels.unsqueeze((- 1)).repeat(1, 1, 2))
    X = (X + mu)
    batch['X'] = X
    if onehot:
        batch.pop('labels')
        batch['oh_labels'] = F.one_hot(labels, K)
    else:
        batch['labels'] = labels
    return batch

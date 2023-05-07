import numpy as np
import torch
from .base_sampler import BaseSampler


@staticmethod
def random_choice(gallery, num):
    "Random select some elements from the gallery.\n\n        It seems that Pytorch's implementation is slower than numpy so we use\n        numpy to randperm the indices.\n        "
    assert (len(gallery) >= num)
    if isinstance(gallery, list):
        gallery = np.array(gallery)
    cands = np.arange(len(gallery))
    np.random.shuffle(cands)
    rand_inds = cands[:num]
    if (not isinstance(gallery, np.ndarray)):
        rand_inds = torch.from_numpy(rand_inds).long().to(gallery.device)
    return gallery[rand_inds]

import torch
from .base_sampler import BaseSampler
from mmdet.core.bbox import demodata


def random_choice(self, gallery, num):
    'Random select some elements from the gallery.\n\n        If `gallery` is a Tensor, the returned indices will be a Tensor;\n        If `gallery` is a ndarray or list, the returned indices will be a\n        ndarray.\n\n        Args:\n            gallery (Tensor | ndarray | list): indices pool.\n            num (int): expected sample num.\n\n        Returns:\n            Tensor or ndarray: sampled indices.\n        '
    assert (len(gallery) >= num)
    is_tensor = isinstance(gallery, torch.Tensor)
    if (not is_tensor):
        gallery = torch.tensor(gallery, dtype=torch.long, device=torch.cuda.current_device())
    perm = torch.randperm(gallery.numel(), device=gallery.device)[:num]
    rand_inds = gallery[perm]
    if (not is_tensor):
        rand_inds = rand_inds.cpu().numpy()
    return rand_inds

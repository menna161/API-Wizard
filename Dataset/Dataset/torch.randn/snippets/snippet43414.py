import torch


def __call__(self, sample):
    m = (torch.eye(3) + (torch.randn(3, 3) * self._pertubation_factor))
    if self._flip:
        m[(0, 0)] *= (- 1)
    pos_idx = [a for a in dir(sample) if ('pos' in a)]
    for pos_id in pos_idx:
        sample[pos_id] = (sample[pos_id] @ m)
    return sample

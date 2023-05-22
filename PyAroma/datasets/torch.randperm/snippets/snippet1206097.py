import torch
import torch.nn.functional as F
import utils


def simba_single(self, x, y, num_iters=10000, epsilon=0.2, targeted=False):
    n_dims = x.view(1, (- 1)).size(1)
    perm = torch.randperm(n_dims)
    x = x.unsqueeze(0)
    last_prob = self.get_probs(x, y)
    for i in range(num_iters):
        diff = torch.zeros(n_dims)
        diff[perm[i]] = epsilon
        left_prob = self.get_probs((x - diff.view(x.size())).clamp(0, 1), y)
        if (targeted != (left_prob < last_prob)):
            x = (x - diff.view(x.size())).clamp(0, 1)
            last_prob = left_prob
        else:
            right_prob = self.get_probs((x + diff.view(x.size())).clamp(0, 1), y)
            if (targeted != (right_prob < last_prob)):
                x = (x + diff.view(x.size())).clamp(0, 1)
                last_prob = right_prob
        if ((i % 10) == 0):
            print(last_prob)
    return x.squeeze()

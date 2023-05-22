import math
import torch
import torch.nn as nn
from .prior.priors import *
import torch.nn.functional as F
from .variational_dist import Q_FCDenseNet103_FVI


def predict_runtime(self, x_t, S):
    self.q.eval()
    self.prior.cpu()
    (B, _, H, W) = x_t.size()
    assert (B == 1), 'Predict one image at a time'
    Z = torch.randn((S, B, self.num_classes, H, W)).to(self.device)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    with torch.no_grad():
        start.record()
        (q_mean, q_cov_out, q_cov_out_diag, q_logvar_aleatoric) = self.q(x_t)
        q_cov_out = q_cov_out.contiguous().view(B, self.L, (- 1), H, W)
        q_var = ((torch.einsum('ijklm,ijklm->iklm', q_cov_out, q_cov_out) / self.L) + q_cov_out_diag.exp())
        f_samples = (q_mean.unsqueeze(0).expand(S, B, (- 1), H, W) + torch.einsum('ijklm,jklm->ijklm', Z, q_var.sqrt()))
        f_samples = torch.einsum('ijklm,jklm->ijklm', f_samples, torch.exp((- q_logvar_aleatoric)))
        f_dist = F.softmax(f_samples, 2).mean(0)
        f_pred = f_dist.argmax(1)
        f_entropy = (- (torch.log((f_dist + 1e-12)) * f_dist).sum(1))
        end.record()
        torch.cuda.synchronize()
        time = start.elapsed_time(end)
        print('Inference time elapsed (ms): {}'.format(time))
    self.q.train()
    return time

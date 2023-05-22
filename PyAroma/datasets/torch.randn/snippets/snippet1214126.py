import math
import torch


def jit_sample_normal(num: int, mean: torch.Tensor, cholesky_precisions: torch.Tensor, covariance_type: str) -> torch.Tensor:
    samples = torch.randn(num, mean.size(0), dtype=mean.dtype, device=mean.device)
    chol_covariance = _cholesky_covariance(cholesky_precisions, covariance_type)
    if (covariance_type in ('tied', 'full')):
        scale = chol_covariance.matmul(samples.unsqueeze((- 1))).squeeze((- 1))
    else:
        scale = (chol_covariance * samples)
    return (mean + scale)

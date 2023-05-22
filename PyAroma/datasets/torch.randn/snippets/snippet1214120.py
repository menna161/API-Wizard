from typing import List
import torch


def sample_means(counts: List[int], dims: List[int]) -> List[torch.Tensor]:
    return [torch.randn(count, dim) for (count, dim) in zip(counts, dims)]

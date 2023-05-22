import torch


@staticmethod
def forward(ctx, A, b, alpha):
    initialx = torch.randn(b.shape[0], device=b.device, dtype=b.dtype)
    initialx = (initialx - (torch.matmul(alpha, initialx) * alpha))
    x = CG_torch(A, b, initialx)
    ctx.save_for_backward(A, alpha, x)
    return x

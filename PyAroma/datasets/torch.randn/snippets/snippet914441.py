import torch


@staticmethod
def forward(ctx, g, E0, b, alpha):
    Aprime = (lambda v: (A(v) - (E0 * v)))
    initialx = torch.randn(b.shape[0], device=b.device, dtype=b.dtype)
    initialx = (initialx - (torch.matmul(alpha, initialx) * alpha))
    x = CG_torch(Aprime, b, initialx, sparse=True)
    ctx.g = g
    ctx.save_for_backward(E0, alpha, x)
    return x

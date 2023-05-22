import torch


def setCGSubspaceSparse(A, Aadjoint_to_gadjoint):
    '\n        Function primitive of low-rank CG linear system solver, where the matrix is\n    "sparse" and represented as a function.\n\n        As a workaround of the fact that Pytorch doesn\'t support taking gradient of\n    objects of type other than torch.tensor, the computation graph of this primitive\n    is wrapped compared to CGSubspace, which the version in which the matrix A is\n    normally represented as a torch.Tensor. \n        In particular, this wrapped version is mainly used to make the back-propagation\n    of the dominant sparse eigensolver primitive -- i.e., DominantSparseSymeig -- work\n    properly. The computation graph is schematically shown below.\n            ----------------------\n    g     --|--> A               | \n            |     \\              | \n            |      A-E_0I --     |\n            |     /         \\    |\n    E_0   --|-->--          |||--|--> x  \n            |               / /  |\n    b     --|------->------- /   |\n    alpha --|------->--------    |\n            ----------------------\n    input: g -- The parameter(s) of interest of the matrix A, whose gradients are requested.\n                In current version, g must be a torch.Tensor of arbitrary shape.\n           E0, alpha are the smallest eigvalue and corresponding (non-degenerate)\n                eigenvector, respectively.\n    output: x.\n\n        The computation process involves using CG algorithm to solve a low-rank linear\n    system of the form (A - E_0I)x = b, alpha^T x = 0. For more details of this part, \n    c.f. https://buwantaiji.github.io/2019/10/CG-backward/\n\n    USER NOTE: The mechanism of wrapping relies on user\'s providing two quantities:\n        A -- The "sparse" representation of the matrix A as a function.\n        Aadjoint_to_gadjoint -- A function that receive the adjoint of the matrix A\n            as input, and return the adjoint of the pamameters(g) as output.\n\n            The input should be of the form of two vectors represented as torch.Tensor, \n        say, v1 and v2, and the adjoint of A = v1 * v2^T.(outer product)\n            User may do whatever he want to get the adjoint of g using these\n        two vectors.\n    '
    global CGSubspaceSparse

    @staticmethod
    def forward(ctx, g, E0, b, alpha):
        Aprime = (lambda v: (A(v) - (E0 * v)))
        initialx = torch.randn(b.shape[0], device=b.device, dtype=b.dtype)
        initialx = (initialx - (torch.matmul(alpha, initialx) * alpha))
        x = CG_torch(Aprime, b, initialx, sparse=True)
        ctx.g = g
        ctx.save_for_backward(E0, alpha, x)
        return x

    @staticmethod
    def backward(ctx, grad_x):
        g = ctx.g
        (E0, alpha, x) = ctx.saved_tensors
        CG = CGSubspaceSparse.apply
        b = (grad_x - (torch.matmul(alpha, grad_x) * alpha))
        grad_b = CG(g, E0, b, alpha)
        (v1, v2) = ((- grad_b), x)
        grad_alpha = ((- x) * torch.matmul(alpha, grad_x))
        grad_E0 = (- torch.matmul(v1, v2))
        grad_g = Aadjoint_to_gadjoint(v1, v2)
        return (grad_g, grad_E0, grad_b, grad_alpha)
    CGSubspaceSparse = type('CGSubspaceSparse', (torch.autograd.Function,), {'forward': forward, 'backward': backward})

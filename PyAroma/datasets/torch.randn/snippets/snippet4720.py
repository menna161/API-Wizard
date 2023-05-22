import torch
import torch.nn as nn


def forward(self, x):
    (B, C, H, W) = x.size()
    gx = self.pool(x)
    (mu, log_var) = (self.mu(gx), self.logvar(gx))
    if self.training:
        std = torch.exp(log_var.reshape(B, self.nodes, self.hidden))
        eps = torch.randn_like(std)
        z = (mu.reshape(B, self.nodes, self.hidden) + (std * eps))
    else:
        z = mu.reshape(B, self.nodes, self.hidden)
    A = torch.matmul(z, z.permute(0, 2, 1))
    A = torch.relu(A)
    Ad = torch.diagonal(A, dim1=1, dim2=2)
    mean = torch.mean(Ad, dim=1).clamp(min=0.001)
    gama = torch.sqrt((1 + (1.0 / mean))).unsqueeze((- 1)).unsqueeze((- 1))
    dl_loss = ((gama.mean() * torch.log((Ad[(Ad < 1)] + 1e-07)).sum()) / ((A.size(0) * A.size(1)) * A.size(2)))
    kl_loss = (((- 0.5) / self.nodes) * torch.mean(torch.sum((((1 + (2 * log_var)) - mu.pow(2)) - log_var.exp().pow(2)), 1)))
    loss = (kl_loss - dl_loss)
    if self.add_diag:
        diag = []
        for i in range(Ad.shape[0]):
            diag.append(torch.diag(Ad[(i, :)]).unsqueeze(0))
        A = (A + (gama * torch.cat(diag, 0)))
    A = self.laplacian_matrix(A, self_loop=True)
    z_hat = ((gama.mean() * mu.reshape(B, self.nodes, self.hidden)) * (1.0 - log_var.reshape(B, self.nodes, self.hidden)))
    return (A, gx, loss, z_hat)

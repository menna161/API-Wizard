import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.normal import Normal
from lib.utils.vis_logger import logger


def elbo(self, x, n_samples=1):
    '\n        Evaluates elbo for each sample (not averaged)\n        :param x: (B, 1, H, W)\n        :return:\n            elbo: (B, N)\n        '
    B = x.size(0)
    x = x.view(B, (- 1))
    org = x.clone()
    x = self.encoder(x)
    x = self.gaussian(x, n_samples)
    x = self.decoder(x)
    (x, org) = torch.broadcast_tensors(x, org[(:, None, :)])
    bce = self.bce(x, org)
    bce = bce.sum(dim=(- 1))
    kl = self.gaussian.kl_divergence()
    logger.update(image=org[(0, 0)].view(28, 28))
    logger.update(pred=x[(0, 0)].view(28, 28))
    logger.update(bce=bce.mean())
    logger.update(kl=kl.mean())
    z = torch.randn(1, self.dim_latent).to(x.device)
    gen = self.decoder(z)
    logger.update(gen=gen.view(1, 28, 28)[0])
    return ((- bce) - kl[(:, None)])

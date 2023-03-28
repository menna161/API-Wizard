import matplotlib
import matplotlib.pyplot as plt
import os
import tempfile
import torch
import glob
import numpy as np
from collections import OrderedDict
from itertools import product
from torch import nn
from torch import optim
from torchvision.utils import save_image
from tqdm import tqdm
from skimage.io import imread, imsave
from fid_score import calculate_fid_given_imgs
from sklearn.linear_model import LogisticRegression
from MulticoreTSNE import MulticoreTSNE as TSNE
from subprocess import check_output
import itertools
from sklearn.linear_model import LogisticRegression
from models import vae
from sklearn.linear_model import LogisticRegression
from torch.distributions.kl import kl_divergence
from torch import distributions as distns
from collections import Counter
from sklearn.cluster import KMeans


def dsprite_disentanglement_fv(gen, ds, is_vae=False, save_path=None, n_votes=800, L=800, cull_dimensions=False, verbose=False, **kwargs):
    '\n\n    Notes\n    ----- \n\n    Quoted from the FactorVAE paper: "So in our experiments, we use\n     L = 200 and 10000 iterations, with a batch size of 10 per\n     iteration of training the linear classifier, and use a batch of\n     size 800 to evaluate the metric at the end of training."\n     Based on this, `num_examples` should be 10000, `batch_size`\n     should be 200, and the validation set (is it really needed?)\n     consists of 800 examples.\n\n    '
    if (cull_dimensions and (not is_vae)):
        raise Exception('`cull_dimensions` only works when `is_vae` is True')
    from sklearn.linear_model import LogisticRegression
    from torch.distributions.kl import kl_divergence
    from torch import distributions as distns
    from collections import Counter
    gen.eval()
    if (save_path is not None):
        if (not os.path.exists(save_path)):
            os.makedirs(save_path)
    n_examples_per_vote = L
    n_factors = len(ds.metadata['latents_sizes'])
    n_votes_per_factor = (n_votes // (n_factors - 1))
    if verbose:
        pbar = tqdm(total=(n_votes_per_factor * (n_factors - 1)))
    (xs, ys) = ([], [])
    if is_vae:
        (mus, sigmas) = ([], [])
    for k_fixed in range(1, n_factors):
        for _ in range(n_votes_per_factor):
            rnd_val = np.random.randint(0, ds.metadata['latents_sizes'][k_fixed])
            samples = ds.sample_conditional(k_fixed, rnd_val, n_examples_per_vote)
            samples = samples.unsqueeze(1)
            samples = samples.cuda()
            with torch.no_grad():
                enc = gen.encode(samples)
                if is_vae:
                    mu = enc[:, 0:(enc.size(1) // 2)]
                    sigma = enc[:, (enc.size(1) // 2):]
                    mus.append(mu)
                    sigmas.append(sigma)
                    enc = mu
                xs.append(enc.cpu().numpy())
                ys.append(k_fixed)
            if verbose:
                pbar.update(1)
    xs = np.asarray(xs)
    ys = (np.asarray(ys) - 1)
    if is_vae:
        mus = torch.cat(mus, dim=0)
        sigmas = torch.cat(sigmas, dim=0)
        this_distn = distns.Normal(mus, sigmas)
        prior = distns.Normal(torch.zeros_like(mus), torch.ones_like(sigmas))
        this_kl = kl_divergence(this_distn, prior)
        if cull_dimensions:
            xs = xs[:, :, (this_kl.mean(dim=0) > 0.01).cpu().numpy().astype(np.bool)]
    xs /= xs.reshape((xs.shape[0] * xs.shape[1]), (- 1)).std(axis=0, keepdims=True)
    print('xs shape =', xs.shape)
    xs_new = []
    for i in range(len(xs)):
        xs_new.append(np.argmin(xs[i].var(axis=0)))
    xs_new = np.asarray(xs_new)
    n_corrects = []
    for j in range(ys.max()):
        n_corrects.append((Counter(xs_new[(ys == j)]).most_common()[0][1] * 1.0))
    n_correct = (np.sum(n_corrects) / len(xs_new))
    if (save_path is not None):
        with open(('%s/result.txt' % save_path), 'w') as f:
            f.write(('Train accuracy: %f\n' % n_correct))
    return {'dfv': n_correct}

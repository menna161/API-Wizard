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


def dsprite_disentanglement(gan, ds, save_path, batch_size=256, num_examples=50000):
    gan._eval()
    from sklearn.linear_model import LogisticRegression
    from models import vae
    is_vae = (True if (type(gan) == vae.VAE) else False)
    if (not os.path.exists(save_path)):
        os.makedirs(save_path)
    xs = []
    ys = []
    pbar = tqdm(total=num_examples)
    for iter in range(num_examples):
        rnd_latent_idx = np.random.randint(1, len(ds.metadata['latents_sizes']))
        rnd_val_in_idx = np.random.randint(0, ds.metadata['latents_sizes'][rnd_latent_idx])
        samples = ds.sample_conditional(rnd_latent_idx, rnd_val_in_idx, batch_size)
        idcs = np.arange(0, len(samples))
        (idcs_even, idcs_odd) = (idcs[0::2], idcs[1::2])
        samples_even = samples[idcs_even].unsqueeze(1)
        samples_odd = samples[idcs_odd].unsqueeze(1)
        if gan.use_cuda:
            samples_even = samples_even.cuda()
            samples_odd = samples_odd.cuda()
        with torch.no_grad():
            enc1 = gan.generator.encode(samples_even)
            enc2 = gan.generator.encode(samples_odd)
            if is_vae:
                enc1 = enc1[:, 0:(enc1.size(1) // 2)]
                enc2 = enc2[:, 0:(enc2.size(1) // 2)]
            diffs = torch.mean(torch.abs((enc1 - enc2)), dim=0).cpu().numpy()
            xs.append(diffs)
            ys.append(rnd_latent_idx)
        pbar.update(1)
    xs = np.asarray(xs)
    ys = (np.asarray(ys) - 1)
    print(xs.shape, ys.shape)
    lm = LogisticRegression(solver='lbfgs', multi_class='multinomial', verbose=1, max_iter=100000)
    lm.fit(xs, ys)
    score = lm.score(xs, ys)
    print(('Accuracy for %i: %f' % (num_examples, lm.score(xs, ys))))
    with open(('%s/result.txt' % save_path), 'w') as f:
        f.write(('Accuracy for %i: %f\n' % (num_examples, score)))

import os
import argparse
import warnings
import numpy as np
from functools import partial
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import chainer
from chainer import training
from chainer.training import extensions
from chainer.training import triggers
import chainer.functions as F
from chainerui.utils import save_args
from chainer_bcnn.datasets import ImageDataset
from chainer_bcnn.data.augmentor import DataAugmentor, Flip2D, Affine2D, Crop2D, ResizeCrop2D
from chainer_bcnn.data.normalizer import Normalizer, Clip2D, Subtract2D, Divide2D
from chainer_bcnn.models import BayesianUNet, UNet
from chainer_bcnn.links import Regressor
from chainer_bcnn.extensions import LogReport
from chainer_bcnn.extensions import PrintReport
from chainer_bcnn.extensions import Validator
from chainer_bcnn.visualizer import ImageVisualizer
from chainer_bcnn.links import MCSampler
from chainer_bcnn.inference import Inferencer
from chainer_bcnn.data import load_image, save_image
from chainer_bcnn.datasets import train_valid_split
from chainer_bcnn.utils import fixed_seed
from chainer_bcnn.utils import find_latest_snapshot
from chainer_bcnn.models import PatchDiscriminator
from chainer_bcnn.updaters import DCGANUpdater, LSGANUpdater


def test_phase(generator, test, args):
    print('# samples:')
    print('-- test:', len(test))
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    snapshot_file = find_latest_snapshot('generator_iter_{.updater.iteration:08}.npz', args.out)
    chainer.serializers.load_npz(snapshot_file, generator)
    print('Loaded a snapshot:', snapshot_file)
    model = MCSampler(generator, mc_iteration=args.mc_iteration, activation=F.tanh, reduce_mean=None, reduce_var=partial(F.mean, axis=1))
    if (args.gpu[0] >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu[0]).use()
        model.to_gpu()
    infer = Inferencer(test_iter, model, device=args.gpu[0])
    (pred, uncert) = infer.run()
    os.makedirs(os.path.join(args.out, 'test'), exist_ok=True)
    acc_values = []
    uncert_values = []
    uncert_clim = (0, np.percentile(uncert, 95))
    error_clim = (0, 1)
    files = test.files['image']
    if isinstance(files, np.ndarray):
        files = files.tolist()
    commonpath = os.path.commonpath(files)
    plt.rcParams['font.size'] = 14
    for (i, (p, u, imf, lbf)) in enumerate(zip(pred, uncert, test.files['image'], test.files['label'])):
        (im, _) = load_image(imf)
        (lb, _) = load_image(lbf)
        im = im.astype(np.float32)
        lb = lb.astype(np.float32)
        p = p.transpose(1, 2, 0)
        im = ((im[(:, :, ::(- 1))] + 1.0) / 2.0)
        lb = ((lb[(:, :, ::(- 1))] + 1.0) / 2.0)
        p = ((p[(:, :, ::(- 1))] + 1.0) / 2.0)
        error = np.mean(np.abs((p - lb)), axis=(- 1))
        acc_values.append(eval_metric(p, lb))
        uncert_values.append(np.mean(u))
        plt.figure(figsize=(20, 4))
        for (j, (pic, cmap, clim, title)) in enumerate(zip([im, p, lb, u, error], [None, None, None, 'jet', 'jet'], [None, None, None, uncert_clim, error_clim], [('Input image\n%s' % os.path.relpath(imf, commonpath)), ('Predicted label\n(MAE=%.3f)' % acc_values[(- 1)]), 'Ground-truth label', ('Predicted variance\n(PV=%.4f)' % uncert_values[(- 1)]), 'Error'])):
            plt.subplot(1, 5, (j + 1))
            plt.imshow(pic, cmap=cmap)
            plt.xticks([], [])
            plt.yticks([], [])
            plt.title(title)
            plt.clim(clim)
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, ('test/%03d.png' % i)))
        plt.close()

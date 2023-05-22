import os
import argparse
import random
import warnings
import numpy as np
import cupy as cp
from functools import partial
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import chainer
from chainer import training
from chainer.training import extensions
from chainer.training import triggers
import chainer.functions as F
from chainer.functions import softmax_cross_entropy
from chainerui.utils import save_args
from chainer_bcnn.datasets import ImageDataset
from chainer_bcnn.data.augmentor import DataAugmentor, Flip2D, Affine2D
from chainer_bcnn.data.normalizer import Normalizer, Clip2D, Subtract2D, Divide2D
from chainer_bcnn.models import BayesianUNet
from chainer_bcnn.links import Classifier
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
from scipy.stats import pearsonr


def train_phase(predictor, train, valid, args):
    print('# classes:', train.n_classes)
    print('# samples:')
    print('-- train:', len(train))
    print('-- valid:', len(valid))
    train_batchsize = min((args.batchsize * len(args.gpu)), len(train))
    valid_batchsize = args.batchsize
    train_iter = chainer.iterators.MultiprocessIterator(train, train_batchsize)
    valid_iter = chainer.iterators.SerialIterator(valid, valid_batchsize, repeat=False, shuffle=True)
    class_weight = None
    lossfun = partial(softmax_cross_entropy, normalize=False, class_weight=class_weight)
    model = Classifier(predictor, lossfun=lossfun)
    if (args.gpu[0] >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu[0]).use()
        if (len(args.gpu) == 1):
            model.to_gpu()
    optimizer = chainer.optimizers.Adam(alpha=args.lr, beta1=0.9, beta2=0.999, eps=1e-08, amsgrad=False)
    optimizer.setup(model)
    if (args.decay > 0):
        optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(args.decay))
    if (len(args.gpu) == 1):
        updater = training.updaters.StandardUpdater(train_iter, optimizer, device=args.gpu[0])
    else:
        devices = {'main': args.gpu[0]}
        for (idx, g) in enumerate(args.gpu[1:]):
            devices[('slave_%d' % idx)] = g
        updater = training.updaters.ParallelUpdater(train_iter, optimizer, devices=devices)
    frequency = (max((args.iteration // 20), 1) if (args.frequency == (- 1)) else max(1, args.frequency))
    stop_trigger = triggers.EarlyStoppingTrigger(monitor='validation/main/loss', max_trigger=(args.iteration, 'iteration'), check_trigger=(frequency, 'iteration'), patients=(np.inf if (args.pinfall == (- 1)) else max(1, args.pinfall)))
    trainer = training.Trainer(updater, stop_trigger, out=args.out)
    transforms = {'x': (lambda x: x), 'y': (lambda x: np.argmax(x, axis=0)), 't': (lambda x: x)}
    cmap = np.array([[0, 0, 0], [0, 0, 1]])
    cmaps = {'x': None, 'y': cmap, 't': cmap}
    clims = {'x': 'minmax', 'y': None, 't': None}
    visualizer = ImageVisualizer(transforms=transforms, cmaps=cmaps, clims=clims)
    valid_file = os.path.join('validation', 'iter_{.updater.iteration:08}.png')
    trainer.extend(Validator(valid_iter, model, valid_file, visualizer=visualizer, n_vis=20, device=args.gpu[0]), trigger=(frequency, 'iteration'))
    trainer.extend(extensions.dump_graph('main/loss'))
    trainer.extend(extensions.snapshot(filename='snapshot_iter_{.updater.iteration:08}.npz'), trigger=(frequency, 'iteration'))
    trainer.extend(extensions.snapshot_object(predictor, 'predictor_iter_{.updater.iteration:08}.npz'), trigger=(frequency, 'iteration'))
    log_keys = ['main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy']
    trainer.extend(LogReport(keys=log_keys))
    if extensions.PlotReport.available():
        for plot_key in ['loss', 'accuracy']:
            plot_keys = [key for key in log_keys if key.split('/')[(- 1)].startswith(plot_key)]
            trainer.extend(extensions.PlotReport(plot_keys, 'iteration', file_name=(plot_key + '.png'), trigger=(frequency, 'iteration')))
    trainer.extend(PrintReport(((['iteration'] + log_keys) + ['elapsed_time']), n_step=100))
    trainer.extend(extensions.ProgressBar())
    if args.resume:
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()

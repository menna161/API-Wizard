import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer import reporter
from chainer.training import extensions
from chainer_bcnn.functions import mc_dropout
from chainer_bcnn.functions.loss import noised_mean_squared_error
from chainer_bcnn.links import Regressor
from chainer_bcnn.links import MCSampler
from chainer_bcnn.inference import Inferencer
from chainer_bcnn.utils import fixed_seed


def train_phase(predictor, train, valid, args):
    plt.rcParams['font.size'] = 18
    plt.figure(figsize=(13, 5))
    ax = sns.scatterplot(x=train.x.ravel(), y=train.y.ravel(), color='blue', s=55, alpha=0.3)
    ax.plot(train.x.ravel(), train.t.ravel(), color='red', linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim((- 10), 10)
    ax.set_ylim((- 15), 15)
    plt.legend(['Ground-truth', 'Observation'])
    plt.title('Training data set')
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, 'train_dataset.png'))
    plt.close()
    train_iter = chainer.iterators.SerialIterator(train, args.batchsize, shuffle=True)
    valid_iter = chainer.iterators.SerialIterator(valid, args.batchsize, repeat=False, shuffle=False)
    lossfun = noised_mean_squared_error
    accfun = (lambda y, t: F.mean_absolute_error(y[0], t))
    model = Regressor(predictor, lossfun=lossfun, accfun=accfun)
    if (args.gpu >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu).use()
        model.to_gpu()
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    if (args.decay > 0):
        optimizer.add_hook(chainer.optimizer_hooks.WeightDecay(args.decay))
    updater = training.updaters.StandardUpdater(train_iter, optimizer, device=args.gpu)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), out=args.out)
    trainer.extend(extensions.Evaluator(valid_iter, model, device=args.gpu))
    trainer.extend(extensions.dump_graph('main/loss'))
    frequency = (args.epoch if (args.frequency == (- 1)) else max(1, args.frequency))
    trainer.extend(extensions.snapshot(), trigger=(frequency, 'epoch'))
    trainer.extend(extensions.LogReport())
    if (args.plot and extensions.PlotReport.available()):
        trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], 'epoch', file_name='loss.png'))
        trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'], 'epoch', file_name='accuracy.png'))
        trainer.extend(extensions.PlotReport(['main/predictor/sigma', 'validation/main/predictor/sigma'], 'epoch', file_name='sigma.png'))
    trainer.extend(extensions.PrintReport(['epoch', 'iteration', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy', 'main/predictor/sigma', 'validation/main/predictor/sigma', 'elapsed_time']))
    trainer.extend(extensions.ProgressBar())
    if args.resume:
        chainer.serializers.load_npz(args.resume, trainer)
    trainer.run()
    chainer.serializers.save_npz(os.path.join(args.out, 'predictor.npz'), predictor)

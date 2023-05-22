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
from chainer.training import extensions
from chainer_bcnn.functions import mc_dropout
from chainer_bcnn.links import Regressor
from chainer_bcnn.links import MCSampler
from chainer_bcnn.inference import Inferencer
from chainer_bcnn.utils import fixed_seed


def test_phase(predictor, test, args):
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    chainer.serializers.load_npz(os.path.join(args.out, 'predictor.npz'), predictor)
    model = MCSampler(predictor, mc_iteration=args.mc_iteration, activation=None, reduce_mean=None, reduce_var=None)
    if (args.gpu >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu).use()
        model.to_gpu()
    infer = Inferencer(test_iter, model, device=args.gpu)
    (pred, uncert) = infer.run()
    x = test.x.ravel()
    t = test.t.ravel()
    pred = pred.ravel()
    uncert = uncert.ravel()
    plt.rcParams['font.size'] = 18
    plt.figure(figsize=(13, 5))
    ax = sns.scatterplot(x=x, y=pred, color='blue', s=75)
    ax.errorbar(x, pred, yerr=uncert, fmt='none', capsize=10, ecolor='gray', linewidth=1.5)
    ax.plot(x, t, color='red', linewidth=1.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim((- 10), 10)
    ax.set_ylim((- 15), 15)
    plt.legend(['Ground-truth', 'Prediction', 'Predicted variance'])
    plt.title('Result on testing data set')
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, 'eval.png'))
    plt.close()

import os
import argparse
import numpy as np
from functools import partial
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from chainer.datasets import get_mnist
from chainer_bcnn.functions import mc_dropout
from chainer_bcnn.links import Classifier
from chainer_bcnn.links import MCSampler
from chainer_bcnn.inference import Inferencer
from chainer_bcnn.utils import fixed_seed


def test_phase(predictor, test, args):
    test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)
    chainer.serializers.load_npz(os.path.join(args.out, 'predictor.npz'), predictor)
    model = MCSampler(predictor, mc_iteration=args.mc_iteration, activation=partial(F.softmax, axis=1), reduce_mean=partial(F.argmax, axis=1), reduce_var=partial(F.mean, axis=1))
    if (args.gpu >= 0):
        chainer.backends.cuda.get_device_from_id(args.gpu).use()
        model.to_gpu()
    infer = Inferencer(test_iter, model, device=args.gpu)
    (pred, uncert) = infer.run()
    os.makedirs(args.out, exist_ok=True)
    match = (pred == test.labels)
    accuracy = (np.sum(match) / len(match))
    arr = [uncert[match], uncert[np.logical_not(match)]]
    plt.rcParams['font.size'] = 18
    plt.figure(figsize=(13, 5))
    ax = sns.violinplot(data=arr, inner='quartile', palette='Blues', orient='h', cut=0)
    ax.set_xlabel('Predicted variance')
    ax.set_yticklabels([('Correct prediction\n(n=%d)' % len(arr[0])), ('Wrong prediction\n(n=%d)' % len(arr[1]))])
    plt.title(('Accuracy=%.3f' % accuracy))
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, 'eval.png'))
    plt.close()

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


def main():
    parser = argparse.ArgumentParser(description='Example: Uncertainty estimates in classification')
    parser.add_argument('--batchsize', '-b', type=int, default=100, help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=300, help='Number of sweeps over the dataset to train')
    parser.add_argument('--frequency', '-f', type=int, default=(- 1), help='Frequency of taking a snapshot')
    parser.add_argument('--gpu', '-g', type=int, default=0, help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='logs', help='Directory to output the log files')
    parser.add_argument('--resume', '-r', default='', help='Resume the training from snapshot')
    parser.add_argument('--unit', '-u', type=int, default=20, help='Number of units')
    parser.add_argument('--noplot', dest='plot', action='store_false', help='Disable PlotReport extension')
    parser.add_argument('--test_on_test', action='store_true', help='Switch to the testing phase on test dataset')
    parser.add_argument('--test_on_valid', action='store_true', help='Switch to the testing phase on valid dataset')
    parser.add_argument('--mc_iteration', type=int, default=50, help='Number of iteration of MCMC')
    parser.add_argument('--decay', type=float, default=(- 1), help='Weight of L2 regularization')
    parser.add_argument('--seed', type=int, default=0, help='Fix the random seed')
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    with fixed_seed(args.seed, strict=False):
        predictor = BayesianConvNet(n_units=args.unit, n_out=10)
        train = Dataset(phase='train', indices=np.arange(0, 1000))
        valid = Dataset(phase='train', indices=np.arange(1000, 2000))
        test = Dataset(phase='test')
        if args.test_on_test:
            test_phase(predictor, test, args)
        elif args.test_on_valid:
            test_phase(predictor, valid, args)
        else:
            train_phase(predictor, train, valid, args)

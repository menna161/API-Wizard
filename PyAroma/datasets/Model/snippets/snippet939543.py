import argparse
import sys
import os
import socket
import numpy as np
import tensorflow as tf
from tensorpack import *
from tensorpack.tfutils import argscope, SmartInit
import horovod.tensorflow as hvd
from imagenet_utils import fbresnet_augmentor, get_val_dataflow, ImageNetModel, eval_classification
from resnet_model import resnet_group, resnet_bottleneck, resnet_backbone, Norm

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='ILSVRC dataset dir')
    parser.add_argument('--logdir', help='Directory for models and training stats.')
    parser.add_argument('--load', help='load model')
    parser.add_argument('--eval', action='store_true', help='run evaluation with --load instead of training.')
    parser.add_argument('--fake', help='use fakedata to test or benchmark this model', action='store_true')
    parser.add_argument('-d', '--depth', help='resnet depth', type=int, default=50, choices=[50, 101, 152])
    parser.add_argument('--norm', choices=['BN', 'GN'], default='BN')
    parser.add_argument('--accum-grad', type=int, default=1)
    parser.add_argument('--weight-decay-norm', action='store_true', help='apply weight decay on normalization layers (gamma & beta).This is used in torch/pytorch, and slightly improves validation accuracy of large models.')
    parser.add_argument('--validation', choices=['distributed', 'master'], help='Validation method. By default the script performs no validation.')
    parser.add_argument('--no-zmq-ops', help='use pure python to send/receive data', action='store_true')
    '\n    Sec 2.3: We keep the per-worker sample size n constant when we change the number of workers k.\n    In this work, we use n = 32 which has performed well for a wide range of datasets and networks.\n    '
    parser.add_argument('--batch', help='per-GPU batch size', default=32, type=int)
    args = parser.parse_args()
    model = Model(args.depth, args.norm)
    model.accum_grad = args.accum_grad
    if args.weight_decay_norm:
        model.weight_decay_pattern = '.*/W|.*/gamma|.*/beta'
    if args.eval:
        batch = 128
        ds = get_val_dataflow(args.data, batch, fbresnet_augmentor(False))
        eval_classification(model, SmartInit(args.load), ds)
        sys.exit()
    logger.info('Training on {}'.format(socket.gethostname()))
    os.system('nvidia-smi')
    assert (args.load is None)
    hvd.init()
    if (args.logdir is None):
        args.logdir = os.path.join('train_log', 'Horovod-{}GPUs-{}Batch'.format(hvd.size(), args.batch))
    if (hvd.rank() == 0):
        logger.set_logger_dir(args.logdir, 'd')
    logger.info('Rank={}, Local Rank={}, Size={}'.format(hvd.rank(), hvd.local_rank(), hvd.size()))
    '\n    Sec 3: Remark 3: Normalize the per-worker loss by\n    total minibatch size kn, not per-worker size n.\n    '
    model.loss_scale = (1.0 / hvd.size())
    config = get_config(model, fake=args.fake)
    '\n    Sec 3: standard communication primitives like\n    allreduce [11] perform summing, not averaging\n    '
    trainer = HorovodTrainer(average=False)
    launch_train_with_config(config, trainer)

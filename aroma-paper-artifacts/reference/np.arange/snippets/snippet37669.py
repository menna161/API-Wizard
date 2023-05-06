from __future__ import division
import argparse
import multiprocessing
import os
import cupy
import numpy as np
import chainer
from chainer import iterators
from chainer.links import Classifier
from chainer.optimizer import WeightDecay
from chainer.optimizers import CorrectedMomentumSGD
from chainer import training
from chainer.training import extensions
from chainercv.chainer_experimental.datasets.sliceable import TransformDataset
from chainercv.datasets import directory_parsing_label_names
from chainercv.datasets import DirectoryParsingLabelDataset
from chainercv.transforms import center_crop
from chainercv.transforms import random_flip
from chainercv.transforms import random_sized_crop
from chainercv.transforms import resize
from chainercv.transforms import scale
from chainercv.chainer_experimental.training.extensions import make_shift
from chainercv.links.model.resnet import Bottleneck
from chainercv.links import ResNet101
from chainercv.links import ResNet152
from chainercv.links import ResNet50
import chainermn
import chainer_compiler
from chainer_compiler.utils import input_rewriter
import cv2


def main():
    model_cfgs = {'resnet50': {'class': ResNet50, 'score_layer_name': 'fc6', 'kwargs': {'arch': 'fb'}}, 'resnet101': {'class': ResNet101, 'score_layer_name': 'fc6', 'kwargs': {'arch': 'fb'}}, 'resnet152': {'class': ResNet152, 'score_layer_name': 'fc6', 'kwargs': {'arch': 'fb'}}}
    parser = argparse.ArgumentParser(description='Learning convnet from ILSVRC2012 dataset')
    parser.add_argument('train', help='Path to root of the train dataset')
    parser.add_argument('val', help='Path to root of the validation dataset')
    parser.add_argument('--export', type=str, default=None, help='Export the model to ONNX')
    parser.add_argument('--compile', type=str, default=None, help='Compile the model')
    parser.add_argument('--computation_order', type=str, default=None, help='Computation order in backpropagation')
    parser.add_argument('--model', '-m', choices=model_cfgs.keys(), default='resnet50', help='Convnet models')
    parser.add_argument('--communicator', type=str, default='pure_nccl', help='Type of communicator')
    parser.add_argument('--loaderjob', type=int, default=4)
    parser.add_argument('--batchsize', type=int, default=32, help='Batch size for each worker')
    parser.add_argument('--lr', type=float)
    parser.add_argument('--momentum', type=float, default=0.9)
    parser.add_argument('--weight-decay', type=float, default=0.0001)
    parser.add_argument('--out', type=str, default='result')
    parser.add_argument('--epoch', type=int, default=90)
    parser.add_argument('--iterations', '-I', type=int, default=None, help='Number of iterations to train')
    parser.add_argument('--no_use_fixed_batch_dataset', dest='use_fixed_batch_dataset', action='store_false', help='Disable the use of FixedBatchDataset')
    parser.add_argument('--compiler-log', action='store_true', help='Enables compile-time logging')
    parser.add_argument('--trace', action='store_true', help='Enables runtime tracing')
    parser.add_argument('--verbose', action='store_true', help='Enables runtime verbose log')
    parser.add_argument('--skip_runtime_type_check', action='store_true', help='Skip runtime type check')
    parser.add_argument('--dump_memory_usage', type=int, default=0, help='Dump memory usage (0-2)')
    parser.add_argument('--quiet_period', type=int, default=0, help='Quiet period after runtime report')
    parser.add_argument('--overwrite_batchsize', action='store_true', help='Overwrite batch size')
    args = parser.parse_args()
    if hasattr(multiprocessing, 'set_start_method'):
        multiprocessing.set_start_method('forkserver')
        p = multiprocessing.Process()
        p.start()
        p.join()
    comm = chainermn.create_communicator(args.communicator)
    device = comm.intra_rank
    if (args.lr is not None):
        lr = args.lr
    else:
        lr = ((0.1 * (args.batchsize * comm.size)) / 256)
        if (comm.rank == 0):
            print('lr={}: lr is selected based on the linear scaling rule'.format(lr))
    label_names = directory_parsing_label_names(args.train)
    model_cfg = model_cfgs[args.model]
    extractor = model_cfg['class'](n_class=len(label_names), **model_cfg['kwargs'])
    extractor.pick = model_cfg['score_layer_name']
    for l in extractor.links():
        if isinstance(l, Bottleneck):
            l.conv3.bn.gamma.data[:] = 0
    if (args.export is not None):
        chainer_compiler.use_unified_memory_allocator()
        extractor.to_device(device)
        x = extractor.xp.zeros((args.batchsize, 3, 224, 224)).astype('f')
        chainer_compiler.export(extractor, [x], args.export)
        return
    if (args.compile is not None):
        print('run compiled model')
        chainer_compiler.use_chainerx_shared_allocator()
        extractor.to_device(device)
        with chainer.using_config('enable_backprop', False), chainer.using_config('train', False):
            x = extractor.xp.zeros((1, 3, 224, 224)).astype('f')
            extractor(x)
        compiler_kwargs = {}
        if args.compiler_log:
            compiler_kwargs['compiler_log'] = True
        runtime_kwargs = {}
        if args.trace:
            runtime_kwargs['trace'] = True
        if args.verbose:
            runtime_kwargs['verbose'] = True
        if args.skip_runtime_type_check:
            runtime_kwargs['check_types'] = False
        if (args.dump_memory_usage >= 1):
            runtime_kwargs['dump_memory_usage'] = args.dump_memory_usage
            (free, total) = cupy.cuda.runtime.memGetInfo()
            used = (total - free)
            runtime_kwargs['base_memory_usage'] = used
        onnx_filename = args.compile
        if args.overwrite_batchsize:
            new_onnx_filename = ('/tmp/overwrite_batchsize_' + os.path.basename(onnx_filename))
            new_input_types = [input_rewriter.Type(shape=(args.batchsize, 3, 224, 224))]
            input_rewriter.rewrite_onnx_file(onnx_filename, new_onnx_filename, new_input_types)
            onnx_filename = new_onnx_filename
        extractor_cc = chainer_compiler.compile_onnx(extractor, onnx_filename, 'onnx_chainer', computation_order=args.computation_order, compiler_kwargs=compiler_kwargs, runtime_kwargs=runtime_kwargs, quiet_period=args.quiet_period)
        model = Classifier(extractor_cc)
    else:
        print('run vanilla chainer model')
        model = Classifier(extractor)
    train_data = DirectoryParsingLabelDataset(args.train)
    val_data = DirectoryParsingLabelDataset(args.val)
    train_data = TransformDataset(train_data, ('img', 'label'), TrainTransform(extractor.mean))
    val_data = TransformDataset(val_data, ('img', 'label'), ValTransform(extractor.mean))
    print('finished loading dataset')
    if (comm.rank == 0):
        train_indices = np.arange(len(train_data))
        val_indices = np.arange(len(val_data))
    else:
        train_indices = None
        val_indices = None
    train_indices = chainermn.scatter_dataset(train_indices, comm, shuffle=True)
    val_indices = chainermn.scatter_dataset(val_indices, comm, shuffle=True)
    train_data = train_data.slice[train_indices]
    val_data = val_data.slice[val_indices]
    if args.use_fixed_batch_dataset:
        train_data = FixedBatchDataset(train_data, args.batchsize)
        val_data = FixedBatchDataset(val_data, args.batchsize)
    train_iter = chainer.iterators.MultiprocessIterator(train_data, args.batchsize, n_processes=args.loaderjob)
    val_iter = iterators.MultiprocessIterator(val_data, args.batchsize, repeat=False, shuffle=False, n_processes=args.loaderjob)
    optimizer = chainermn.create_multi_node_optimizer(CorrectedMomentumSGD(lr=lr, momentum=args.momentum), comm)
    optimizer.setup(model)
    for param in model.params():
        if (param.name not in ('beta', 'gamma')):
            param.update_rule.add_hook(WeightDecay(args.weight_decay))
    if (device >= 0):
        chainer.cuda.get_device(device).use()
        model.to_gpu()
    updater = chainer.training.StandardUpdater(train_iter, optimizer, device=device)
    if args.iterations:
        stop_trigger = (args.iterations, 'iteration')
    else:
        stop_trigger = (args.epoch, 'epoch')
    trainer = training.Trainer(updater, stop_trigger, out=args.out)

    @make_shift('lr')
    def warmup_and_exponential_shift(trainer):
        epoch = trainer.updater.epoch_detail
        warmup_epoch = 5
        if (epoch < warmup_epoch):
            if (lr > 0.1):
                warmup_rate = (0.1 / lr)
                rate = (warmup_rate + (((1 - warmup_rate) * epoch) / warmup_epoch))
            else:
                rate = 1
        elif (epoch < 30):
            rate = 1
        elif (epoch < 60):
            rate = 0.1
        elif (epoch < 80):
            rate = 0.01
        else:
            rate = 0.001
        return (rate * lr)
    trainer.extend(warmup_and_exponential_shift)
    evaluator = chainermn.create_multi_node_evaluator(extensions.Evaluator(val_iter, model, device=device), comm)
    trainer.extend(evaluator, trigger=(1, 'epoch'))
    log_interval = (0.1, 'epoch')
    print_interval = (0.1, 'epoch')
    if (comm.rank == 0):
        trainer.extend(chainer.training.extensions.observe_lr(), trigger=log_interval)
        trainer.extend(extensions.snapshot_object(extractor, 'snapshot_model_{.updater.epoch}.npz'), trigger=(args.epoch, 'epoch'))
        trainer.extend(extensions.LogReport(trigger=log_interval))
        trainer.extend(extensions.PrintReport(['iteration', 'epoch', 'elapsed_time', 'lr', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy']), trigger=print_interval)
        trainer.extend(extensions.ProgressBar(update_interval=10))
    trainer.run()

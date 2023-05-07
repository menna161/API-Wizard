from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import mxnet as mx
import numpy as np
import os
import sys
import random
import argparse
import dataset as D
import transforms as T
from model import Model
from loss import HPHNTripletLoss
from runner import Trainer, Evaluator
from util import SummaryWriter


def main():
    args = parser.parse_args()
    args.train_meta = './meta/CARS196/train.txt'
    args.test_meta = './meta/CARS196/test.txt'
    args.lr_decay_epochs = [int(epoch) for epoch in args.lr_decay_epochs.split(',')]
    args.recallk = [int(k) for k in args.recallk.split(',')]
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_idx)
    args.ctx = [mx.gpu(0)]
    print(args)
    mx.random.seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)
    (train_transform, test_transform) = T.get_transform(image_size=args.image_size)
    (train_loader, test_loader) = D.get_data_loader(args.data_dir, args.train_meta, args.test_meta, train_transform, test_transform, args.batch_size, args.num_instances, args.num_workers)
    model = Model(args.embed_dim, args.ctx)
    model.hybridize()
    loss = HPHNTripletLoss(margin=args.margin, soft_margin=False, num_instances=args.num_instances, n_inner_pts=args.n_inner_pts, l2_norm=args.ee_l2norm)
    summary_writer = SummaryWriter(os.path.join(args.save_dir, 'tensorboard_log'))
    print('steps in epoch:', args.lr_decay_epochs)
    steps = list(map((lambda x: (x * len(train_loader))), args.lr_decay_epochs))
    print('steps in iter:', steps)
    lr_schedule = mx.lr_scheduler.MultiFactorScheduler(step=steps, factor=args.lr_decay_factor)
    lr_schedule.base_lr = args.lr
    optimizer = mx.gluon.Trainer(model.collect_params(), 'adam', {'learning_rate': args.lr, 'wd': args.wd}, kvstore=args.kvstore)
    trainer = Trainer(model, loss, optimizer, train_loader, summary_writer, args.ctx, summary_step=args.summary_step, lr_schedule=lr_schedule)
    evaluator = Evaluator(model, test_loader, args.ctx)
    best_metrics = [0.0]
    global_step = (args.start_epoch * len(train_loader))
    print('base lr mult:', args.base_lr_mult)
    for epoch in range(args.start_epoch, args.epochs):
        model.backbone.collect_params().setattr('lr_mult', args.base_lr_mult)
        trainer.train(epoch)
        global_step = ((epoch + 1) * len(train_loader))
        if (((epoch + 1) % args.eval_epoch_term) == 0):
            old_best_metric = best_metrics[0]
            best_metrics = evaluate_and_log(summary_writer, evaluator, args.recallk, global_step, (epoch + 1), best_metrics=best_metrics)
            if (best_metrics[0] != old_best_metric):
                save_path = os.path.join(args.save_dir, ('model_epoch_%05d.params' % (epoch + 1)))
                model.save_parameters(save_path)
        sys.stdout.flush()

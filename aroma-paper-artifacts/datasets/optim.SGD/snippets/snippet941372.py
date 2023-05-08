import torch
import numpy as np
import argparse
import os
from tqdm import tqdm
from lib.fvi_seg import FVI_seg
from lib.utils.torch_utils import adjust_learning_rate
from lib.utils.fvi_seg_utils import test, numpy_metrics, run_runtime_seg
from lib.utils.camvid import get_camvid
from lib.elbo_seg import fELBO_seg as fELBO
from lib.priors import f_prior_BNN

if (__name__ == '__main__'):
    device = torch.device('cuda')
    keys = ('device', 'x_inducing_var', 'f_prior', 'n_inducing', 'add_cov_diag', 'standard_cross_entropy')
    values = (device, args.x_inducing_var, args.f_prior, args.n_inducing, args.add_cov_diag, args.standard_cross_entropy)
    fvi_args = dict(zip(keys, values))
    FVI = FVI_seg(x_size=(H_crop, W_crop), num_classes=num_classes, **fvi_args).to(device)
    optimizer = torch.optim.SGD(FVI.parameters(), lr=args.lr, momentum=0.9, weight_decay=0.0001)
    if args.load:
        model_load_dir = os.path.join(args.base_dir, 'FVI_CV/model_{}_{}.bin'.format(args.dataset, exp_name))
        optimizer_load_dir = os.path.join(args.base_dir, 'FVI_CV/optimizer_{}_{}.bin'.format(args.dataset, exp_name))
        FVI.load_state_dict(torch.load(model_load_dir))
        optimizer.load_state_dict(torch.load(optimizer_load_dir))
        print('Loading FVI segmentation model..')
    if args.training_mode:
        print('Training FVI segmentation for {} epochs'.format(args.n_epochs))
        train(args.n_epochs, train_loader, FVI)
    if args.test_mode:
        print('Evaluating FVI segmentation on test set')
        model_load_dir = os.path.join(args.base_dir, 'FVI_CV/models_test/model_{}_fvi_seg_test.bin'.format(args.dataset))
        FVI.load_state_dict(torch.load(model_load_dir))
        (error, mIOU) = test(FVI, test_loader, num_classes, args.dataset, exp_name, mkdir=True)
        print('Test Error: {:.5f} || Test Mean IOU: {:.5f}'.format(error, mIOU))
        np.savetxt('{}_{}_epoch_{}_test_error.txt'.format(args.dataset, exp_name, (- 1)), [error])
        np.savetxt('{}_{}_epoch_{}_test_mIOU.txt'.format(args.dataset, exp_name, (- 1)), [mIOU])
    if args.test_runtime_mode:
        model_load_dir = os.path.join(args.base_dir, 'FVI_CV/models_test/model_{}_fvi_seg_test.bin'.format(args.dataset))
        FVI.load_state_dict(torch.load(model_load_dir))
        run_runtime_seg(FVI, test_loader, exp_name, 50)

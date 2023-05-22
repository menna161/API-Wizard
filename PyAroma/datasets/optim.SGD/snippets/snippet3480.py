import argparse
import os
import sys
import pickle
import resource
import traceback
import logging
from collections import defaultdict
import numpy as np
import yaml
import torch
from torch.autograd import Variable
import torch.nn as nn
import cv2
import _init_paths
import nn as mynn
import utils_rel.net_rel as net_utils_rel
import utils.misc as misc_utils
from core.config import cfg, cfg_from_file, cfg_from_list, assert_and_infer_cfg
from datasets_rel.roidb_rel import combined_roidb_for_training
from roi_data_rel.loader_rel import RoiDataLoader, MinibatchSampler, BatchSampler, collate_minibatch
from utils.detectron_weight_helper import load_detectron_weight
from utils.logging import setup_logging
from utils.timer import Timer
from utils_rel.training_stats_rel import TrainingStats
from core.test_engine_rel_mps import get_metrics_det_boxes, get_metrics_gt_boxes
from tensorboardX import SummaryWriter


def main():
    'Main function'
    args = parse_args()
    print('Called with args:')
    print(args)
    if (not torch.cuda.is_available()):
        sys.exit('Need a CUDA device to run the code.')
    if (args.cuda or (cfg.NUM_GPUS > 0)):
        cfg.CUDA = True
    else:
        raise ValueError('Need Cuda device to run !')
    if (args.dataset == 'vrd'):
        cfg.TRAIN.DATASETS = ('vrd_train',)
        cfg.TEST.DATASETS = ('vrd_val',)
        cfg.MODEL.NUM_CLASSES = 101
        cfg.MODEL.NUM_PRD_CLASSES = 70
    elif (args.dataset == 'vg_mini'):
        cfg.TRAIN.DATASETS = ('vg_train_mini',)
        cfg.MODEL.NUM_CLASSES = 151
        cfg.MODEL.NUM_PRD_CLASSES = 50
    elif (args.dataset == 'vg'):
        cfg.TRAIN.DATASETS = ('vg_train',)
        cfg.MODEL.NUM_CLASSES = 151
        cfg.MODEL.NUM_PRD_CLASSES = 50
    elif (args.dataset == 'oi_rel'):
        cfg.TRAIN.DATASETS = ('oi_rel_train',)
        cfg.MODEL.NUM_CLASSES = 58
        cfg.MODEL.NUM_PRD_CLASSES = 9
    elif (args.dataset == 'oi_rel_mini'):
        cfg.TRAIN.DATASETS = ('oi_rel_train_mini',)
        cfg.MODEL.NUM_CLASSES = 58
        cfg.MODEL.NUM_PRD_CLASSES = 9
    else:
        raise ValueError('Unexpected args.dataset: {}'.format(args.dataset))
    cfg_from_file(args.cfg_file)
    if (args.set_cfgs is not None):
        cfg_from_list(args.set_cfgs)
    Generalized_RCNN = importlib.import_module(('modeling_rel.' + cfg.MODEL.TYPE)).Generalized_RCNN
    from core.test_engine_rel_mps import get_metrics_det_boxes, get_metrics_gt_boxes
    original_batch_size = (cfg.NUM_GPUS * cfg.TRAIN.IMS_PER_BATCH)
    original_num_gpus = cfg.NUM_GPUS
    original_ims_per_batch = cfg.TRAIN.IMS_PER_BATCH
    if (args.batch_size is None):
        args.batch_size = original_batch_size
    cfg.NUM_GPUS = torch.cuda.device_count()
    assert ((args.batch_size % cfg.NUM_GPUS) == 0), ('batch_size: %d, NUM_GPUS: %d' % (args.batch_size, cfg.NUM_GPUS))
    cfg.TRAIN.IMS_PER_BATCH = (args.batch_size // cfg.NUM_GPUS)
    effective_batch_size = (args.iter_size * args.batch_size)
    print(('effective_batch_size = batch_size * iter_size = %d * %d' % (args.batch_size, args.iter_size)))
    print('Adaptive config changes:')
    print(('    effective_batch_size: %d --> %d' % (original_batch_size, effective_batch_size)))
    print(('    NUM_GPUS:             %d --> %d' % (original_num_gpus, cfg.NUM_GPUS)))
    print(('    IMS_PER_BATCH:        %d --> %d' % (original_ims_per_batch, cfg.TRAIN.IMS_PER_BATCH)))
    old_base_lr = cfg.SOLVER.BASE_LR
    cfg.SOLVER.BASE_LR *= (args.batch_size / original_batch_size)
    print('Adjust BASE_LR linearly according to batch_size change:\n    BASE_LR: {} --> {}'.format(old_base_lr, cfg.SOLVER.BASE_LR))
    step_scale = (original_batch_size / effective_batch_size)
    old_solver_steps = cfg.SOLVER.STEPS
    old_max_iter = cfg.SOLVER.MAX_ITER
    cfg.SOLVER.STEPS = list(map((lambda x: int(((x * step_scale) + 0.5))), cfg.SOLVER.STEPS))
    cfg.SOLVER.MAX_ITER = int(((cfg.SOLVER.MAX_ITER * step_scale) + 0.5))
    print('Adjust SOLVER.STEPS and SOLVER.MAX_ITER linearly based on effective_batch_size change:\n    SOLVER.STEPS: {} --> {}\n    SOLVER.MAX_ITER: {} --> {}'.format(old_solver_steps, cfg.SOLVER.STEPS, old_max_iter, cfg.SOLVER.MAX_ITER))
    if (cfg.FPN.FPN_ON and cfg.MODEL.FASTER_RCNN):
        cfg.FPN.RPN_COLLECT_SCALE = (cfg.TRAIN.IMS_PER_BATCH / original_ims_per_batch)
        print('Scale FPN rpn_proposals collect size directly propotional to the change of IMS_PER_BATCH:\n    cfg.FPN.RPN_COLLECT_SCALE: {}'.format(cfg.FPN.RPN_COLLECT_SCALE))
    if (args.num_workers is not None):
        cfg.DATA_LOADER.NUM_THREADS = args.num_workers
    print(('Number of data loading threads: %d' % cfg.DATA_LOADER.NUM_THREADS))
    if (args.optimizer is not None):
        cfg.SOLVER.TYPE = args.optimizer
    if (args.lr is not None):
        cfg.SOLVER.BASE_LR = args.lr
    if (args.lr_decay_gamma is not None):
        cfg.SOLVER.GAMMA = args.lr_decay_gamma
    assert_and_infer_cfg()
    timers = defaultdict(Timer)
    timers['roidb'].tic()
    (roidb, ratio_list, ratio_index, ds) = combined_roidb_for_training(cfg.TRAIN.DATASETS, cfg.TRAIN.PROPOSAL_FILES)
    timers['roidb'].toc()
    roidb_size = len(roidb)
    logger.info('{:d} roidb entries'.format(roidb_size))
    logger.info('Takes %.2f sec(s) to construct roidb', timers['roidb'].average_time)
    train_size = ((roidb_size // args.batch_size) * args.batch_size)
    batchSampler = BatchSampler(sampler=MinibatchSampler(ratio_list, ratio_index), batch_size=args.batch_size, drop_last=True)
    dataset = RoiDataLoader(roidb, cfg.MODEL.NUM_CLASSES, training=True)
    dataloader = torch.utils.data.DataLoader(dataset, batch_sampler=batchSampler, num_workers=cfg.DATA_LOADER.NUM_THREADS, collate_fn=collate_minibatch)
    dataiterator = iter(dataloader)
    maskRCNN = Generalized_RCNN()
    if cfg.CUDA:
        maskRCNN.cuda()
    gn_params = []
    backbone_bias_params = []
    backbone_bias_param_names = []
    prd_branch_bias_params = []
    prd_branch_bias_param_names = []
    backbone_nonbias_params = []
    backbone_nonbias_param_names = []
    prd_branch_nonbias_params = []
    prd_branch_nonbias_param_names = []
    for (key, value) in dict(maskRCNN.named_parameters()).items():
        if value.requires_grad:
            if ('gn' in key):
                gn_params.append(value)
            elif (('Conv_Body' in key) or ('Box_Head' in key) or ('Box_Outs' in key) or ('RPN' in key)):
                if ('bias' in key):
                    backbone_bias_params.append(value)
                    backbone_bias_param_names.append(key)
                else:
                    backbone_nonbias_params.append(value)
                    backbone_nonbias_param_names.append(key)
            elif ('bias' in key):
                prd_branch_bias_params.append(value)
                prd_branch_bias_param_names.append(key)
            else:
                prd_branch_nonbias_params.append(value)
                prd_branch_nonbias_param_names.append(key)
    params = [{'params': backbone_nonbias_params, 'lr': 0, 'weight_decay': cfg.SOLVER.WEIGHT_DECAY}, {'params': backbone_bias_params, 'lr': (0 * (cfg.SOLVER.BIAS_DOUBLE_LR + 1)), 'weight_decay': (cfg.SOLVER.WEIGHT_DECAY if cfg.SOLVER.BIAS_WEIGHT_DECAY else 0)}, {'params': prd_branch_nonbias_params, 'lr': 0, 'weight_decay': cfg.SOLVER.WEIGHT_DECAY}, {'params': prd_branch_bias_params, 'lr': (0 * (cfg.SOLVER.BIAS_DOUBLE_LR + 1)), 'weight_decay': (cfg.SOLVER.WEIGHT_DECAY if cfg.SOLVER.BIAS_WEIGHT_DECAY else 0)}, {'params': gn_params, 'lr': 0, 'weight_decay': cfg.SOLVER.WEIGHT_DECAY_GN}]
    if (cfg.SOLVER.TYPE == 'SGD'):
        optimizer = torch.optim.SGD(params, momentum=cfg.SOLVER.MOMENTUM)
    elif (cfg.SOLVER.TYPE == 'Adam'):
        optimizer = torch.optim.Adam(params)
    if args.load_ckpt:
        load_name = args.load_ckpt
        logging.info('loading checkpoint %s', load_name)
        checkpoint = torch.load(load_name, map_location=(lambda storage, loc: storage))
        net_utils_rel.load_ckpt_rel(maskRCNN, checkpoint['model'])
        if args.resume:
            args.start_step = (checkpoint['step'] + 1)
            if ('train_size' in checkpoint):
                if (checkpoint['train_size'] != train_size):
                    print(('train_size value: %d different from the one in checkpoint: %d' % (train_size, checkpoint['train_size'])))
            optimizer.load_state_dict(checkpoint['optimizer'])
            misc_utils.load_optimizer_state_dict(optimizer, checkpoint['optimizer'])
        del checkpoint
        torch.cuda.empty_cache()
    if args.load_detectron:
        logging.info('loading Detectron weights %s', args.load_detectron)
        load_detectron_weight(maskRCNN, args.load_detectron)
    lr = optimizer.param_groups[2]['lr']
    backbone_lr = optimizer.param_groups[0]['lr']
    device_ids = list(range(torch.cuda.device_count()))
    maskRCNN_one_gpu = mynn.DataParallel(maskRCNN, cpu_keywords=['im_info', 'roidb'], minibatch=True, device_ids=[device_ids[0]])
    maskRCNN = mynn.DataParallel(maskRCNN, cpu_keywords=['im_info', 'roidb'], minibatch=True)
    args.run_name = (((((misc_utils.get_run_name() + '_') + args.exp) + '_') + '_step_with_prd_cls_v') + str(cfg.MODEL.SUBTYPE))
    output_dir = misc_utils.get_output_dir(args, args.run_name)
    args.cfg_filename = os.path.basename(args.cfg_file)
    if (not args.no_save):
        if (not os.path.exists(output_dir)):
            os.makedirs(output_dir)
        blob = {'cfg': yaml.dump(cfg), 'args': args}
        with open(os.path.join(output_dir, 'config_and_args.pkl'), 'wb') as f:
            pickle.dump(blob, f, pickle.HIGHEST_PROTOCOL)
        if args.use_tfboard:
            from tensorboardX import SummaryWriter
            tblogger = SummaryWriter(output_dir)
    maskRCNN.train()
    CHECKPOINT_PERIOD = (ds.len // effective_batch_size)
    decay_steps_ind = None
    for i in range(1, len(cfg.SOLVER.STEPS)):
        if (cfg.SOLVER.STEPS[i] >= args.start_step):
            decay_steps_ind = i
            break
    if (decay_steps_ind is None):
        decay_steps_ind = len(cfg.SOLVER.STEPS)
    training_stats = TrainingStats(args, args.disp_interval, (tblogger if (args.use_tfboard and (not args.no_save)) else None))
    try:
        logger.info('Training starts !')
        step = args.start_step
        for step in range(args.start_step, cfg.SOLVER.MAX_ITER):
            if (step < cfg.SOLVER.WARM_UP_ITERS):
                method = cfg.SOLVER.WARM_UP_METHOD
                if (method == 'constant'):
                    warmup_factor = cfg.SOLVER.WARM_UP_FACTOR
                elif (method == 'linear'):
                    alpha = (step / cfg.SOLVER.WARM_UP_ITERS)
                    warmup_factor = ((cfg.SOLVER.WARM_UP_FACTOR * (1 - alpha)) + alpha)
                else:
                    raise KeyError('Unknown SOLVER.WARM_UP_METHOD: {}'.format(method))
                lr_new = (cfg.SOLVER.BASE_LR * warmup_factor)
                net_utils_rel.update_learning_rate_rel(optimizer, lr, lr_new)
                lr = optimizer.param_groups[2]['lr']
                backbone_lr = optimizer.param_groups[0]['lr']
                assert (lr == lr_new)
            elif (step == cfg.SOLVER.WARM_UP_ITERS):
                net_utils_rel.update_learning_rate_rel(optimizer, lr, cfg.SOLVER.BASE_LR)
                lr = optimizer.param_groups[2]['lr']
                backbone_lr = optimizer.param_groups[0]['lr']
                assert (lr == cfg.SOLVER.BASE_LR)
            if ((decay_steps_ind < len(cfg.SOLVER.STEPS)) and (step == cfg.SOLVER.STEPS[decay_steps_ind])):
                logger.info('Decay the learning on step %d', step)
                lr_new = (lr * cfg.SOLVER.GAMMA)
                net_utils_rel.update_learning_rate_rel(optimizer, lr, lr_new)
                lr = optimizer.param_groups[2]['lr']
                backbone_lr = optimizer.param_groups[0]['lr']
                assert (lr == lr_new)
                decay_steps_ind += 1
            training_stats.IterTic()
            optimizer.zero_grad()
            for inner_iter in range(args.iter_size):
                try:
                    input_data = next(dataiterator)
                except StopIteration:
                    dataiterator = iter(dataloader)
                    input_data = next(dataiterator)
                for key in input_data:
                    if (key != 'roidb'):
                        input_data[key] = list(map(Variable, input_data[key]))
                net_outputs = maskRCNN(**input_data)
                training_stats.UpdateIterStats(net_outputs, inner_iter)
                loss = net_outputs['total_loss']
                loss.backward()
            optimizer.step()
            training_stats.IterToc()
            if (step == args.start_step):
                for (n, p) in maskRCNN.named_parameters():
                    if ((p.requires_grad == True) and (p.grad is None)):
                        logger.warning('The module was defined but no-use!')
                        logger.warning(n)
            training_stats.LogIterStats(step, lr, backbone_lr)
            if ((int((step + 1)) % CHECKPOINT_PERIOD) == 0):
                save_ckpt(output_dir, args, step, train_size, maskRCNN, optimizer)
                metrics = get_metrics_gt_boxes(maskRCNN_one_gpu, timers, cfg.TEST.DATASETS[0])
                maskRCNN.train()
                tblogger.add_scalar((args.dataset + '_metrics'), metrics, step)
        save_ckpt(output_dir, args, step, train_size, maskRCNN, optimizer)
    except (RuntimeError, KeyboardInterrupt):
        del dataiterator
        logger.info('Save ckpt on exception ...')
        save_ckpt(output_dir, args, step, train_size, maskRCNN, optimizer)
        logger.info('Save ckpt done.')
        stack_trace = traceback.format_exc()
        print(stack_trace)
    finally:
        if (args.use_tfboard and (not args.no_save)):
            tblogger.close()

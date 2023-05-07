from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import os
from absl import flags
from metric import ece_metric
from nets import hparams_config
from nets.optimizer_setting import *
from official.utils.flags import core as flags_core
from official.utils.logs import hooks_helper
from official.utils.logs import logger
from official.utils.misc import model_helpers
from utils import checkpoint_utils
from utils import data_util
from utils import export_utils
from utils.hook_utils import *
from utils import config_utils
from metric import recall_metric
from functions import data_config, model_fns, input_fns
from nets import blocks
from losses import cls_losses
from hyperdash import Experiment


def resnet_main(flags_obj, model_function, input_function, dataset_name, shape=None, num_images=None, zeroshot_eval=False):
    model_helpers.apply_clean(flags.FLAGS)
    os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
    session_config = config_utils.get_session_config(flags_obj)
    run_config = config_utils.get_run_config(flags_obj, flags_core, session_config, num_images['train'])

    def gen_estimator(period=None):
        resnet_size = int(flags_obj.resnet_size)
        data_format = flags_obj.data_format
        batch_size = flags_obj.batch_size
        resnet_version = int(flags_obj.resnet_version)
        loss_scale = flags_core.get_loss_scale(flags_obj)
        dtype_tf = flags_core.get_tf_dtype(flags_obj)
        num_epochs_per_decay = flags_obj.num_epochs_per_decay
        learning_rate_decay_factor = flags_obj.learning_rate_decay_factor
        end_learning_rate = flags_obj.end_learning_rate
        learning_rate_decay_type = flags_obj.learning_rate_decay_type
        weight_decay = flags_obj.weight_decay
        zero_gamma = flags_obj.zero_gamma
        lr_warmup_epochs = flags_obj.lr_warmup_epochs
        base_learning_rate = flags_obj.base_learning_rate
        use_resnet_d = flags_obj.use_resnet_d
        use_dropblock = flags_obj.use_dropblock
        dropblock_kp = [float(be) for be in flags_obj.dropblock_kp]
        label_smoothing = flags_obj.label_smoothing
        momentum = flags_obj.momentum
        bn_momentum = flags_obj.bn_momentum
        train_epochs = flags_obj.train_epochs
        piecewise_lr_boundary_epochs = [int(be) for be in flags_obj.piecewise_lr_boundary_epochs]
        piecewise_lr_decay_rates = [float(dr) for dr in flags_obj.piecewise_lr_decay_rates]
        use_ranking_loss = flags_obj.use_ranking_loss
        use_se_block = flags_obj.use_se_block
        use_sk_block = flags_obj.use_sk_block
        mixup_type = flags_obj.mixup_type
        dataset_name = flags_obj.dataset_name
        kd_temp = flags_obj.kd_temp
        no_downsample = flags_obj.no_downsample
        anti_alias_filter_size = flags_obj.anti_alias_filter_size
        anti_alias_type = flags_obj.anti_alias_type
        cls_loss_type = flags_obj.cls_loss_type
        logit_type = flags_obj.logit_type
        embedding_size = flags_obj.embedding_size
        pool_type = flags_obj.pool_type
        arc_s = flags_obj.arc_s
        arc_m = flags_obj.arc_m
        bl_alpha = flags_obj.bl_alpha
        bl_beta = flags_obj.bl_beta
        exp = None
        if (install_hyperdash and flags_obj.use_hyperdash):
            exp = Experiment(flags_obj.model_dir.split('/')[(- 1)])
            resnet_size = exp.param('resnet_size', int(flags_obj.resnet_size))
            batch_size = exp.param('batch_size', flags_obj.batch_size)
            exp.param('dtype', flags_obj.dtype)
            learning_rate_decay_type = exp.param('learning_rate_decay_type', flags_obj.learning_rate_decay_type)
            weight_decay = exp.param('weight_decay', flags_obj.weight_decay)
            zero_gamma = exp.param('zero_gamma', flags_obj.zero_gamma)
            lr_warmup_epochs = exp.param('lr_warmup_epochs', flags_obj.lr_warmup_epochs)
            base_learning_rate = exp.param('base_learning_rate', flags_obj.base_learning_rate)
            use_dropblock = exp.param('use_dropblock', flags_obj.use_dropblock)
            dropblock_kp = exp.param('dropblock_kp', [float(be) for be in flags_obj.dropblock_kp])
            piecewise_lr_boundary_epochs = exp.param('piecewise_lr_boundary_epochs', [int(be) for be in flags_obj.piecewise_lr_boundary_epochs])
            piecewise_lr_decay_rates = exp.param('piecewise_lr_decay_rates', [float(dr) for dr in flags_obj.piecewise_lr_decay_rates])
            mixup_type = exp.param('mixup_type', flags_obj.mixup_type)
            dataset_name = exp.param('dataset_name', flags_obj.dataset_name)
            exp.param('autoaugment_type', flags_obj.autoaugment_type)
        classifier = tf.estimator.Estimator(model_fn=model_function, model_dir=flags_obj.model_dir, config=run_config, params={'resnet_size': resnet_size, 'data_format': data_format, 'batch_size': batch_size, 'resnet_version': resnet_version, 'loss_scale': loss_scale, 'dtype': dtype_tf, 'num_epochs_per_decay': num_epochs_per_decay, 'learning_rate_decay_factor': learning_rate_decay_factor, 'end_learning_rate': end_learning_rate, 'learning_rate_decay_type': learning_rate_decay_type, 'weight_decay': weight_decay, 'zero_gamma': zero_gamma, 'lr_warmup_epochs': lr_warmup_epochs, 'base_learning_rate': base_learning_rate, 'use_resnet_d': use_resnet_d, 'use_dropblock': use_dropblock, 'dropblock_kp': dropblock_kp, 'label_smoothing': label_smoothing, 'momentum': momentum, 'bn_momentum': bn_momentum, 'embedding_size': embedding_size, 'train_epochs': train_epochs, 'piecewise_lr_boundary_epochs': piecewise_lr_boundary_epochs, 'piecewise_lr_decay_rates': piecewise_lr_decay_rates, 'with_drawing_bbox': flags_obj.with_drawing_bbox, 'use_ranking_loss': use_ranking_loss, 'use_se_block': use_se_block, 'use_sk_block': use_sk_block, 'mixup_type': mixup_type, 'kd_temp': kd_temp, 'no_downsample': no_downsample, 'dataset_name': dataset_name, 'anti_alias_filter_size': anti_alias_filter_size, 'anti_alias_type': anti_alias_type, 'cls_loss_type': cls_loss_type, 'logit_type': logit_type, 'arc_s': arc_s, 'arc_m': arc_m, 'pool_type': pool_type, 'bl_alpha': bl_alpha, 'bl_beta': bl_beta, 'train_steps': total_train_steps})
        return (classifier, exp)
    run_params = {'batch_size': flags_obj.batch_size, 'dtype': flags_core.get_tf_dtype(flags_obj), 'resnet_size': flags_obj.resnet_size, 'resnet_version': flags_obj.resnet_version, 'synthetic_data': flags_obj.use_synthetic_data, 'train_epochs': flags_obj.train_epochs}
    if flags_obj.use_synthetic_data:
        dataset_name = (dataset_name + '-synthetic')
    benchmark_logger = logger.get_benchmark_logger()
    benchmark_logger.log_run_info('resnet', dataset_name, run_params, test_id=flags_obj.benchmark_test_id)
    train_hooks = hooks_helper.get_train_hooks(flags_obj.hooks, model_dir=flags_obj.model_dir, batch_size=flags_obj.batch_size)

    def input_fn_train(num_epochs):
        return input_function(is_training=True, use_random_crop=flags_obj.training_random_crop, num_epochs=num_epochs, flags_obj=flags_obj)

    def input_fn_eval():
        return input_function(is_training=False, use_random_crop=False, num_epochs=1, flags_obj=flags_obj)
    ckpt_keeper = checkpoint_utils.CheckpointKeeper(save_dir=flags_obj.model_dir, num_to_keep=flags_obj.num_best_ckpt_to_keep, keep_epoch=flags_obj.keep_ckpt_every_eval, maximize=True)
    if zeroshot_eval:
        dataset = data_config.get_config(dataset_name)
        model = model_fns.Model(int(flags_obj.resnet_size), flags_obj.data_format, resnet_version=int(flags_obj.resnet_version), num_classes=dataset.num_classes, zero_gamma=flags_obj.zero_gamma, use_se_block=flags_obj.use_se_block, use_sk_block=flags_obj.use_sk_block, no_downsample=flags_obj.no_downsample, anti_alias_filter_size=flags_obj.anti_alias_filter_size, anti_alias_type=flags_obj.anti_alias_type, bn_momentum=flags_obj.bn_momentum, embedding_size=flags_obj.embedding_size, pool_type=flags_obj.pool_type, bl_alpha=flags_obj.bl_alpha, bl_beta=flags_obj.bl_beta, dtype=flags_core.get_tf_dtype(flags_obj), loss_type=flags_obj.cls_loss_type)

    def train_and_evaluate(hooks):
        tf.logging.info('Starting cycle: %d/%d', cycle_index, int(n_loops))
        if num_train_epochs:
            classifier.train(input_fn=(lambda : input_fn_train(num_train_epochs)), hooks=hooks, steps=flags_obj.max_train_steps)
        tf.logging.info('Starting to evaluate.')
        if zeroshot_eval:
            tf.reset_default_graph()
            eval_results = recall_metric.recall_at_k(flags_obj, flags_core, input_fns.input_fn_ir_eval, model, num_images['validation'], eval_similarity=flags_obj.eval_similarity, return_embedding=True)
        else:
            eval_results = classifier.evaluate(input_fn=input_fn_eval, steps=flags_obj.max_train_steps)
        return eval_results
    total_train_steps = (flags_obj.train_epochs * int((num_images['train'] / flags_obj.batch_size)))
    if (flags_obj.eval_only or (not flags_obj.train_epochs)):
        (schedule, n_loops) = ([0], 1)
    elif flags_obj.export_only:
        (schedule, n_loops) = ([], 0)
    else:
        n_loops = math.ceil((flags_obj.train_epochs / flags_obj.epochs_between_evals))
        schedule = [flags_obj.epochs_between_evals for _ in range(int(n_loops))]
        schedule[(- 1)] = (flags_obj.train_epochs - sum(schedule[:(- 1)]))
        schedule = config_utils.get_epoch_schedule(flags_obj, schedule, num_images)
        tf.logging.info('epoch schedule:')
        tf.logging.info(schedule)
    (classifier, exp) = gen_estimator()
    if flags_obj.pretrained_model_checkpoint_path:
        warm_start_hook = WarmStartHook(flags_obj.pretrained_model_checkpoint_path)
        train_hooks.append(warm_start_hook)
    for (cycle_index, num_train_epochs) in enumerate(schedule):
        eval_results = train_and_evaluate(train_hooks)
        if zeroshot_eval:
            metric = eval_results['recall_at_1']
        else:
            metric = eval_results['accuracy']
        ckpt_keeper.save(metric, flags_obj.model_dir)
        if exp:
            exp.metric('accuracy', metric)
        benchmark_logger.log_evaluation_result(eval_results)
        if model_helpers.past_stop_threshold(flags_obj.stop_threshold, metric):
            break
        if model_helpers.past_stop_threshold(total_train_steps, eval_results['global_step']):
            break
    if exp:
        exp.end()
    if (flags_obj.export_dir is not None):
        export_utils.export_pb(flags_core, flags_obj, shape, classifier)

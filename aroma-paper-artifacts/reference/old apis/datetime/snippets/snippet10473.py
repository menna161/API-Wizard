import datetime
import logging
import time
import torch
import torch.distributed as dist
from maskrcnn_benchmark.utils.comm import get_world_size
from maskrcnn_benchmark.utils.metric_logger import MetricLogger


def do_train(model, data_loader, optimizer, scheduler, checkpointer, device, checkpoint_period, arguments):
    logger = logging.getLogger('maskrcnn_benchmark.trainer')
    logger.info('Start training')
    meters = MetricLogger(delimiter='  ')
    max_iter = len(data_loader)
    start_iter = arguments['iteration']
    model.train()
    start_training_time = time.time()
    end = time.time()
    for (iteration, (images, targets, _)) in enumerate(data_loader, start_iter):
        data_time = (time.time() - end)
        iteration = (iteration + 1)
        arguments['iteration'] = iteration
        scheduler.step()
        images = images.to(device)
        targets = [target.to(device) for target in targets]
        loss_dict = model(images, targets)
        losses = sum((loss for loss in loss_dict.values()))
        loss_dict_reduced = reduce_loss_dict(loss_dict)
        losses_reduced = sum((loss for loss in loss_dict_reduced.values()))
        meters.update(loss=losses_reduced, **loss_dict_reduced)
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        batch_time = (time.time() - end)
        end = time.time()
        meters.update(time=batch_time, data=data_time)
        eta_seconds = (meters.time.global_avg * (max_iter - iteration))
        eta_string = str(datetime.timedelta(seconds=int(eta_seconds)))
        if (((iteration % 20) == 0) or (iteration == max_iter)):
            logger.info(meters.delimiter.join(['eta: {eta}', 'iter: {iter}', '{meters}', 'lr: {lr:.6f}', 'max mem: {memory:.0f}']).format(eta=eta_string, iter=iteration, meters=str(meters), lr=optimizer.param_groups[0]['lr'], memory=((torch.cuda.max_memory_allocated() / 1024.0) / 1024.0)))
        if ((iteration % checkpoint_period) == 0):
            checkpointer.save('model_{:07d}'.format(iteration), **arguments)
        if (iteration == max_iter):
            checkpointer.save('model_final', **arguments)
    total_training_time = (time.time() - start_training_time)
    total_time_str = str(datetime.timedelta(seconds=total_training_time))
    logger.info('Total training time: {} ({:.4f} s / it)'.format(total_time_str, (total_training_time / max_iter)))

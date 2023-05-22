import datetime
import json
import logging
import os
import torch
from machamp.model.machamp import MachampModel
from uniplot import plot_to_string


def report_scores(self, cur_epoch, best_epoch):
    info = {'epoch': ((str(cur_epoch) + '/') + str(self.num_epochs)), 'best_epoch': best_epoch}
    best_epoch -= 1
    cur_epoch -= 1
    if torch.cuda.is_available():
        info['max_gpu_mem'] = (torch.cuda.max_memory_allocated() * 1e-09)
    _proc_status = ('/proc/%d/status' % os.getpid())
    if os.path.isfile(_proc_status):
        data = open(_proc_status).read()
        i = data.index('VmRSS:')
        info['cur_ram'] = (int(data[i:].split(None, 3)[1]) * 1e-06)
    else:
        info['cur_ram'] = 0
    info['time_epoch'] = str((datetime.datetime.now() - self.epoch_start_time)).split('.')[0]
    info['time_total'] = str((datetime.datetime.now() - self.start_time)).split('.')[0]
    for key in info:
        if (type(info[key]) == float):
            info[key] = '{:.4f}'.format(info[key])
    longest_key = (max([len(key) for key in info]) + 1)
    for (key, value) in info.items():
        logger.info((((key + (' ' * (longest_key - len(key)))) + ': ') + str(value)))
    logger.info('')
    table = [['', 'train_loss', 'dev_loss', 'train_scores', 'dev_scores']]
    for (epoch_name, epoch) in zip([(('Best (' + str((best_epoch + 1))) + ')'), ('Epoch ' + str((cur_epoch + 1)))], [best_epoch, cur_epoch]):
        table.append([epoch_name, '', '', '', ''])
        for task_name in sorted(self.train_scores[0]):
            prefix = ('best_' if epoch_name.startswith('Best') else '')
            if (task_name == 'sum'):
                continue
            else:
                main_metric = self.train_scores[epoch][task_name]['optimization_metrics']
                if ('sum' in self.train_scores[epoch][task_name][main_metric]):
                    sum_metric = self.train_scores[epoch][task_name][main_metric]['sum']
                else:
                    if (len(self.train_scores[epoch][task_name][main_metric]) != 1):
                        logger.error('Not sure which metric to pick')
                        exit(1)
                    sum_metric = list(self.train_scores[epoch][task_name][main_metric].keys())[0]
                task_metrics = list(self.train_scores[epoch][task_name].keys())
                task_metrics.remove('optimization_metrics')
                for task_metric in task_metrics:
                    task_submetrics = list(self.train_scores[epoch][task_name][task_metric].keys())
                    if ('sum' in task_submetrics):
                        if (task_metric in task_submetrics):
                            task_submetrics.remove(task_metric)
                        task_submetrics.remove('sum')
                    if (len(task_submetrics) > 0):
                        for task_submetric in task_submetrics:
                            submetric_train_score = self.train_scores[epoch][task_name][task_metric][task_submetric]
                            info[((((prefix + 'train_') + task_name) + '_') + task_submetric)] = submetric_train_score
                train_score = self.train_scores[epoch][task_name][main_metric][sum_metric]
                info[((((prefix + 'train_') + task_name) + '_') + main_metric)] = train_score
                info[(((prefix + 'train_') + task_name) + '_loss')] = self.train_losses[epoch][task_name]
                if ((len(self.dev_scores) > 0) and (task_name in self.dev_scores[epoch])):
                    for task_metric in task_metrics:
                        task_submetrics = list(self.dev_scores[epoch][task_name][task_metric].keys())
                        if ('sum' in task_submetrics):
                            if (task_metric in task_submetrics):
                                task_submetrics.remove(task_metric)
                            task_submetrics.remove('sum')
                        if (len(task_submetrics) > 0):
                            for task_submetric in task_submetrics:
                                submetric_dev_score = self.dev_scores[epoch][task_name][task_metric][task_submetric]
                                info[((((prefix + 'dev_') + task_name) + '_') + task_submetric)] = submetric_dev_score
                    dev_score = self.dev_scores[epoch][task_name][main_metric][sum_metric]
                    info[((((prefix + 'dev_') + task_name) + '_') + main_metric)] = dev_score
                    if (task_name not in self.dev_losses[epoch]):
                        self.dev_losses[epoch][task_name] = 0.0
                    info[(((prefix + 'dev_') + task_name) + '_loss')] = self.dev_losses[epoch][task_name]
                    table.append([((task_name + '_') + sum_metric), self.train_losses[epoch][task_name], self.dev_losses[epoch][task_name], train_score, dev_score])
                else:
                    table.append([((task_name + '_') + sum_metric), self.train_losses[epoch][task_name], '-', train_score, '-'])
        if (len(self.dev_scores) > 0):
            table.append(['sum', self.train_losses[epoch]['sum'], self.dev_losses[epoch]['sum'], self.train_scores[epoch]['sum'], self.dev_scores[epoch]['sum']])
        else:
            table.append(['sum', self.train_losses[epoch]['sum'], '-', self.train_scores[epoch]['sum'], '-'])
    for row_idx in range(len(table)):
        for cell_idx in range(len(table[row_idx])):
            if (type(table[row_idx][cell_idx]) == float):
                table[row_idx][cell_idx] = '{:.4f}'.format(table[row_idx][cell_idx])
    maxes = []
    for columnIdx in range(len(table[0])):
        maxes.append(max([len(row[columnIdx]) for row in table]))
    for row in table:
        row_str = ''
        for (columnIdx, cell) in enumerate(row):
            spacing = (' ' * (maxes[columnIdx] - len(cell)))
            if (columnIdx == 0):
                row_str += ((cell + spacing) + ' ')
            else:
                row_str += ((spacing + cell) + ' ')
        logger.info(row_str)
    info_ordered = {}
    for item in info:
        if (('dev' not in item) and ('train' not in item)):
            info_ordered[item] = info[item]
    for item in info:
        if (('loss' in item) and ('train' in item)):
            info_ordered[item] = info[item]
    if ('sum' in self.train_scores[0]):
        if ('sum' in self.dev_scores):
            sums = [epoch['sum'] for epoch in self.dev_scores]
            best_epoch = sums.index(max(sums))
        else:
            best_epoch = (len(self.train_scores) - 1)
        info_ordered['best_train_sum'] = self.train_scores[best_epoch]['sum']
        info_ordered['train_sum'] = self.train_scores[(- 1)]['sum']
    for item in info:
        if (('loss' in item) and ('dev' in item)):
            info_ordered[item] = info[item]
    if ((len(self.dev_scores) > 0) and ('sum' in self.dev_scores[0])):
        sums = [epoch['sum'] for epoch in self.dev_scores]
        best_epoch = sums.index(max(sums))
        info_ordered['best_dev_sum'] = self.dev_scores[best_epoch]['sum']
        info_ordered['dev_sum'] = self.dev_scores[(- 1)]['sum']
    for item in info:
        if (('train' in item) and ('loss' not in item)):
            info_ordered[item] = info[item]
    for item in info:
        if (('dev' in item) and ('loss' not in item)):
            info_ordered[item] = info[item]
    json.dump(info_ordered, open(os.path.join(self.serialization_dir, (('metrics_epoch_' + str(cur_epoch)) + '.json')), 'w'), indent=4)
    if ((cur_epoch + 1) == self.num_epochs):
        json.dump(info_ordered, open(os.path.join(self.serialization_dir, 'metrics.json'), 'w'), indent=4)

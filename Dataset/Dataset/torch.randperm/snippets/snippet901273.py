import os
import time
import math
import logging
from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn
from torch import cuda
import torch.nn.functional as funct
import onqg.dataset.Constants as Constants
from onqg.dataset.data_processor import preprocess_batch
import ipdb


def train_epoch(self, device, epoch):
    ' Epoch operation in training phase'
    if (self.opt.extra_shuffle and (epoch > self.opt.curriculum)):
        self.logger.info('Shuffling...')
        self.training_data.shuffle()
    self.model.train()
    total_loss = {'classify': 0, 'generate': 0, 'unify': 0, 'coverage': 0, 'nll': 0}
    (n_word_total, n_word_correct) = (0, 0)
    (n_node_total, n_node_correct) = (0, 0)
    report_total_loss = {'classify': 0, 'generate': 0, 'unify': 0, 'coverage': 0, 'nll': 0}
    (report_n_word_total, report_n_word_correct) = (0, 0)
    (report_n_node_total, report_n_node_correct) = (0, 0)
    sample_num = 0
    batch_order = torch.randperm(len(self.training_data))
    for idx in tqdm(range(len(self.training_data)), mininterval=2, desc='  - (Training)   ', leave=False):
        batch_idx = (batch_order[idx] if (epoch > self.opt.curriculum) else idx)
        batch = self.training_data[batch_idx]
        (inputs, max_length, golds, copy) = preprocess_batch(batch, self.opt.edge_vocab_size, sparse=self.opt.sparse, feature=self.opt.feature, dec_feature=self.opt.dec_feature, copy=self.opt.copy, node_feature=self.opt.node_feature, device=device)
        (copy_gold, copy_switch) = (copy[0], copy[1])
        sample_num += len(golds[0])
        self.model.zero_grad()
        self.optimizer.zero_grad()
        rst = self.model(inputs, max_length=max_length)
        loss_input = {'classification': {}, 'generation': {}, 'unify': {}}
        if (self.opt.copy and (self.opt.training_mode != 'classify')):
            (loss_input['generation']['copy_pred'], loss_input['generation']['copy_gate']) = (rst['generation']['copy_pred'], rst['generation']['copy_gate'])
            (loss_input['generation']['copy_gold'], loss_input['generation']['copy_switch']) = (copy_gold, copy_switch)
        if (self.opt.coverage and (self.opt.training_mode != 'classify')):
            loss_input['generation']['coverage_pred'] = rst['generation']['coverage_pred']
        if (self.opt.training_mode != 'generate'):
            loss_input['classification']['pred'] = rst['classification']
            loss_input['classification']['gold'] = golds[1]
            (loss, n_correct_node) = self.cal_class_performance(loss_input['classification'], device)
            cls_loss = loss
            total_loss['classify'] += loss.item()
            report_total_loss['classify'] += loss.item()
        if (self.opt.training_mode != 'classify'):
            loss_input['generation']['pred'] = rst['generation']['pred']
            loss_input['generation']['gold'] = golds[0]
            (loss, n_correct_word, loss_package) = self.cal_performance(loss_input['generation'])
            gen_loss = loss
            (coverage_loss, nll_loss) = (loss_package[0], loss_package[1])
            total_loss['generate'] += loss.item()
            report_total_loss['generate'] += loss.item()
            if self.opt.coverage:
                total_loss['coverage'] += coverage_loss.item()
                report_total_loss['coverage'] += coverage_loss.item()
            total_loss['nll'] += nll_loss.item()
            report_total_loss['nll'] += nll_loss.item()
        if (self.opt.training_mode == 'unify'):
            loss_input['unify'] = rst['generation']['attention_scores']
            kl_loss = funct.kl_div(torch.log((loss_input['unify'][0] + 1e-16)), loss_input['unify'][1])
            total_loss['unify'] += kl_loss.item()
            report_total_loss['unify'] += kl_loss.item()
        self.cntBatch += 1
        if (self.opt.training_mode == 'unify'):
            ratio = ((self.cntBatch // 8000) + 4)
            if (((self.cntBatch // 128) % ratio) == 0):
                loss = cls_loss
            else:
                loss = gen_loss
        if (len(self.opt.gpus) > 1):
            loss = loss.mean()
        if (math.isnan(loss.item()) or (loss.item() > 1e+20)):
            print('catch NaN')
            import ipdb
            ipdb.set_trace()
        self.optimizer.backward(loss)
        self.optimizer.step()
        non_pad_mask = golds[0].ne(Constants.PAD)
        n_word = non_pad_mask.sum().item()
        if (self.opt.training_mode != 'classify'):
            n_word_total += n_word
            n_word_correct += n_correct_word
            report_n_word_total += n_word
            report_n_word_correct += n_correct_word
        if (self.opt.training_mode != 'generate'):
            n_node = golds[1].ne(Constants.PAD).sum().item()
            n_node_total += n_node
            n_node_correct += n_correct_node
            report_n_node_total += n_node
            report_n_node_correct += n_correct_node
        if ((self.cntBatch % self.opt.valid_steps) == 0):
            valid_results = self.eval_step(device, epoch)
            better = False
            valid_eval = 0
            if (self.opt.training_mode != 'generate'):
                report_avg_loss = (report_total_loss['classify'] / report_n_node_total)
                report_avg_accu = ((report_n_node_correct / report_n_node_total) * 100)
                (report_total_loss['classify'], report_n_node_total, report_n_node_correct) = (0, 0, 0)
                better = (valid_results['classification']['correct'] > self.best_accu)
                if better:
                    self.best_accu = valid_results['classification']['correct']
                valid_eval = valid_results['classification']['correct']
                self.logger.info('  +  Training accuracy: {accu:3.3f} %, loss: {loss:3.5f}'.format(accu=report_avg_accu, loss=report_avg_loss))
                self.logger.info('  +  Validation accuracy: {accu:3.3f} %, loss: {loss:3.5f}'.format(accu=(valid_results['classification']['correct'] * 100), loss=valid_results['classification']['loss']))
            if (self.opt.training_mode != 'classify'):
                report_avg_loss = (report_total_loss['generate'] / report_n_word_total)
                report_avg_ppl = math.exp(min((report_total_loss['nll'] / report_n_word_total), 16))
                report_avg_accu = (report_n_word_correct / report_n_word_total)
                if self.opt.coverage:
                    report_avg_coverage = (report_total_loss['coverage'] / sample_num)
                    report_total_loss['coverage'] = 0
                    self.logger.info('  +  Training coverage loss: {loss:2.5f}'.format(loss=report_avg_coverage))
                    self.logger.info('  +  Validation coverage loss: {loss:2.5f}'.format(loss=valid_results['generation']['coverage']))
                (report_total_loss['generate'], report_total_loss['nll']) = (0, 0)
                (report_n_word_correct, report_n_word_total) = (0, 0)
                better = (valid_results['generation']['perplexity'] < self.best_ppl)
                if better:
                    self.best_ppl = valid_results['generation']['perplexity']
                valid_eval = valid_results['generation']['bleu']
            if (self.opt.training_mode == 'unify'):
                report_avg_kldiv = (report_total_loss['unify'] / sample_num)
                report_total_loss['unify'] = 0
                self.logger.info('  +  Training kl-div loss: {loss:2.5f}'.format(loss=report_avg_kldiv))
                self.logger.info('  +  Validation kl-div loss: {loss:2.5f}'.format(loss=valid_results['unify']))
            sample_num = 0
            self.optimizer.update_learning_rate(better)
            if (self.opt.training_mode != 'classify'):
                record_log(self.opt.logfile_train, step=self.cntBatch, loss=report_avg_loss, ppl=report_avg_ppl, accu=report_avg_accu, bad_cnt=self.optimizer._bad_cnt, lr=self.optimizer._learning_rate)
                record_log(self.opt.logfile_dev, step=self.cntBatch, loss=valid_results['generation']['loss'], ppl=valid_results['generation']['perplexity'], accu=valid_results['generation']['correct'], bleu=valid_results['generation']['bleu'], bad_cnt=self.optimizer._bad_cnt, lr=self.optimizer._learning_rate)
            if self.opt.save_model:
                self.save_model(better, valid_eval)
            self.model.train()
    if (self.opt.training_mode == 'generate'):
        loss_per_word = (total_loss['generate'] / n_word_total)
        perplexity = math.exp(min(loss_per_word, 16))
        accuracy = ((n_word_correct / n_word_total) * 100)
        outputs = (perplexity, accuracy)
    elif (self.opt.training_mode == 'classify'):
        outputs = ((n_node_correct / n_node_total) * 100)
    else:
        outputs = total_loss['unify']
    return outputs

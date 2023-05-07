import os
import time
import warnings
from datetime import datetime
import torch
from .average import AverageMeter
from evaluate.inference import inference
from evaluate.evaluate import evaluate
from tqdm import tqdm
import pandas as pd
from solver.build import make_optimizer
from solver.lr_scheduler import make_scheduler
import logging
from google.colab import output


def fit(self):
    for epoch in range(self.epoch, self.config.SOLVER.MAX_EPOCHS):
        if (epoch < self.config.SOLVER.WARMUP_EPOCHS):
            lr_scale = min(1.0, (float((epoch + 1)) / float(self.config.SOLVER.WARMUP_EPOCHS)))
            for pg in self.optimizer.param_groups:
                pg['lr'] = (lr_scale * self.config.SOLVER.BASE_LR)
            self.do_scheduler = False
        else:
            self.do_scheduler = True
        if self.config.VERBOSE:
            lr = self.optimizer.param_groups[0]['lr']
            timestamp = datetime.utcnow().isoformat()
            self.logger.info(f'''
{timestamp}
LR: {lr}''')
        t = time.time()
        summary_loss = self.train_one_epoch()
        self.logger.info(f'[RESULT]: Train. Epoch: {self.epoch}, summary_loss: {summary_loss.avg:.5f}, time: {(time.time() - t):.5f}')
        self.save(f'{self.base_dir}/last-checkpoint.bin')
        t = time.time()
        (best_score_threshold, best_final_score) = self.validation()
        self.logger.info(f'[RESULT]: Val. Epoch: {self.epoch}, Best Score Threshold: {best_score_threshold:.2f}, Best Score: {best_final_score:.5f}, time: {(time.time() - t):.5f}')
        if (best_final_score > self.best_final_score):
            self.best_final_score = best_final_score
            self.best_score_threshold = best_score_threshold
            self.model.eval()
            self.save(f'{self.base_dir}/best-checkpoint.bin')
            self.save_model(f'{self.base_dir}/best-model.bin')
            self.save_predictions(f'{self.base_dir}/all_predictions.csv')
        self.early_stop(best_final_score)
        if (self.early_stop_epochs > self.config.SOLVER.EARLY_STOP_PATIENCE):
            self.logger.info('Early Stopping!')
            break
        if ((self.epoch % self.config.SOLVER.CLEAR_OUTPUT) == 0):
            output.clear()
        self.epoch += 1

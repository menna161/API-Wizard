import os
import sys
import argparse
import yaml
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torchlight
from torchlight import str2bool
from torchlight import DictAction
from torchlight import import_class
from .processor import Processor
from .data_tools import *


def test(self, evaluation=True, iter_time=0, save_motion=False, phase=False):
    self.model.eval()
    loss_value = []
    normed_test_dict = normalize_data(self.test_dict, self.data_mean, self.data_std, self.dim_use)
    self.actions = ['basketball', 'basketball_signal', 'directing_traffic', 'jumping', 'running', 'soccer', 'walking', 'washwindow']
    self.io.print_log(' ')
    print_str = '{0: <16} |'.format('milliseconds')
    for ms in [40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 560, 1000]:
        print_str = (print_str + ' {0:5d} |'.format(ms))
    self.io.print_log(print_str)
    for (action_num, action) in enumerate(self.actions):
        (encoder_inputs, decoder_inputs, targets) = srnn_sample(normed_test_dict, action, self.arg.source_seq_len, self.arg.target_seq_len, len(self.dim_use))
        encoder_inputs_v = np.zeros_like(encoder_inputs)
        encoder_inputs_v[(:, 1:, :)] = (encoder_inputs[(:, 1:, :)] - encoder_inputs[(:, :(- 1), :)])
        encoder_inputs_a = np.zeros_like(encoder_inputs)
        encoder_inputs_a[(:, 1:, :)] = (encoder_inputs_v[(:, 1:, :)] - encoder_inputs_v[(:, :(- 1), :)])
        encoder_inputs_p = torch.Tensor(encoder_inputs).float().to(self.dev)
        encoder_inputs_v = torch.Tensor(encoder_inputs_v).float().to(self.dev)
        encoder_inputs_a = torch.Tensor(encoder_inputs_a).float().to(self.dev)
        decoder_inputs = torch.Tensor(decoder_inputs).float().to(self.dev)
        decoder_inputs_previous = torch.Tensor(encoder_inputs[(:, (- 1), :)]).unsqueeze(1).to(self.dev)
        decoder_inputs_previous2 = torch.Tensor(encoder_inputs[(:, (- 2), :)]).unsqueeze(1).to(self.dev)
        targets = torch.Tensor(targets).float().to(self.dev)
        (N, T, D) = targets.size()
        targets = targets.contiguous().view(N, T, (- 1), 3).permute(0, 2, 1, 3)
        start_time = time.time()
        with torch.no_grad():
            outputs = self.model(encoder_inputs_p, encoder_inputs_v, encoder_inputs_a, decoder_inputs, decoder_inputs_previous, decoder_inputs_previous2, self.arg.target_seq_len, self.relrec_joint, self.relsend_joint, self.relrec_part, self.relsend_part, self.relrec_body, self.relsend_body, self.arg.lamda)
        if evaluation:
            mean_errors = np.zeros((8, 25), dtype=np.float32)
            for i in np.arange(8):
                output = outputs[i]
                (V, t, d) = output.shape
                output = output.permute(1, 0, 2).contiguous().view(t, (V * d))
                output_denorm = unnormalize_data(output.cpu().numpy(), self.data_mean, self.data_std, self.dim_ignore, self.dim_use, self.dim_zero)
                (t, D) = output_denorm.shape
                output_euler = np.zeros((t, D), dtype=np.float32)
                for j in np.arange(t):
                    for k in np.arange(0, 115, 3):
                        output_euler[(j, k:(k + 3))] = rotmat2euler(expmap2rotmat(output_denorm[(j, k:(k + 3))]))
                target = targets[i]
                target = target.permute(1, 0, 2).contiguous().view(t, (V * d))
                target_denorm = unnormalize_data(target.cpu().numpy(), self.data_mean, self.data_std, self.dim_ignore, self.dim_use, self.dim_zero)
                target_euler = np.zeros((t, D), dtype=np.float32)
                for j in np.arange(t):
                    for k in np.arange(0, 115, 3):
                        target_euler[(j, k:(k + 3))] = rotmat2euler(expmap2rotmat(target_denorm[(j, k:(k + 3))]))
                target_euler[(:, 0:6)] = 0
                idx_to_use1 = np.where((np.std(target_euler, 0) > 0.0001))[0]
                idx_to_use2 = self.dim_nonzero
                idx_to_use = idx_to_use1[np.in1d(idx_to_use1, idx_to_use2)]
                euc_error = np.power((target_euler[(:, idx_to_use)] - output_euler[(:, idx_to_use)]), 2)
                euc_error = np.sqrt(np.sum(euc_error, 1))
                mean_errors[(i, :euc_error.shape[0])] = euc_error
            mean_mean_errors = np.mean(np.array(mean_errors), 0)
            if (save_motion == True):
                save_dir = os.path.join(self.save_dir, ('motions_exp' + str((iter_time * self.arg.savemotion_interval))))
                if (not os.path.exists(save_dir)):
                    os.makedirs(save_dir)
                np.save((((save_dir + '/motions_') + action) + '.npy'), outputs.cpu().numpy())
            print_str = '{0: <16} |'.format(action)
            for (ms_idx, ms) in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 24]):
                if (self.arg.target_seq_len >= (ms + 1)):
                    print_str = (print_str + ' {0:.3f} |'.format(mean_mean_errors[ms]))
                    if (phase is not True):
                        self.MAE_tensor[(iter_time, action_num, ms_idx)] = mean_mean_errors[ms]
                else:
                    print_str = (print_str + '   n/a |')
                    if (phase is not True):
                        self.MAE_tensor[(iter_time, action_num, ms_idx)] = 0
            print_str = (print_str + 'T: {0:.3f} ms |'.format((((time.time() - start_time) * 1000) / 8)))
            self.io.print_log(print_str)
    self.io.print_log(' ')

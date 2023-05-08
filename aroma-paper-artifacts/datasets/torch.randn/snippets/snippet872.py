import math, pickle, os
import numpy as np
import torch
from torch.autograd import Variable
from torch import optim
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
from utils.dsp import *
import sys
import time
from layers.overtone import Overtone
from layers.vector_quant import VectorQuant
from layers.downsampling_encoder import DownsamplingEncoder
import utils.env as env
import utils.logger as logger
import random
import pytorch_warmup as warmup
import apex


def do_train(self, paths, dataset, optimiser, epochs, batch_size, step, lr=0.0001, valid_index=[], use_half=False, do_clip=False):
    if use_half:
        import apex
        optimiser = apex.fp16_utils.FP16_Optimizer(optimiser, dynamic_loss_scale=True)
    for p in optimiser.param_groups:
        p['lr'] = lr
    criterion = nn.NLLLoss().cuda()
    k = 0
    saved_k = 0
    pad_left = self.pad_left()
    pad_left_encoder = self.pad_left_encoder()
    pad_left_decoder = self.pad_left_decoder()
    if self.noise_x:
        extra_pad_right = 127
    else:
        extra_pad_right = 0
    pad_right = (self.pad_right() + extra_pad_right)
    window = (16 * self.total_scale())
    logger.log(f'pad_left={pad_left_encoder}|{pad_left_decoder}, pad_right={pad_right}, total_scale={self.total_scale()}')
    lr_lambda = (lambda epoch: min((epoch / 10), 1))
    lr_scheduler = torch.optim.lr_scheduler.LambdaLR(optimiser, lr_lambda=lr_lambda)
    for e in range(epochs):
        trn_loader = DataLoader(dataset, collate_fn=(lambda batch: env.collate_multispeaker_samples(pad_left, window, pad_right, batch)), batch_size=batch_size, num_workers=2, shuffle=True, pin_memory=True)
        start = time.time()
        running_loss_c = 0.0
        running_loss_f = 0.0
        running_loss_vq = 0.0
        running_loss_vqc = 0.0
        running_entropy = 0.0
        running_max_grad = 0.0
        running_max_grad_name = ''
        iters = len(trn_loader)
        for (i, (speaker, wave16)) in enumerate(trn_loader):
            speaker = speaker.cuda()
            wave16 = wave16.cuda()
            coarse = ((wave16 + (2 ** 15)) // 256)
            fine = ((wave16 + (2 ** 15)) % 256)
            coarse_f = ((coarse.float() / 127.5) - 1.0)
            fine_f = ((fine.float() / 127.5) - 1.0)
            total_f = ((wave16.float() + 0.5) / 32767.5)
            if self.noise_y:
                noisy_f = ((total_f * (0.02 * torch.randn(total_f.size(0), 1).cuda()).exp()) + (0.003 * torch.randn_like(total_f)))
            else:
                noisy_f = total_f
            if use_half:
                coarse_f = coarse_f.half()
                fine_f = fine_f.half()
                noisy_f = noisy_f.half()
            x = torch.cat([coarse_f[(:, (pad_left - pad_left_decoder):(- pad_right))].unsqueeze((- 1)), fine_f[(:, (pad_left - pad_left_decoder):(- pad_right))].unsqueeze((- 1)), coarse_f[(:, ((pad_left - pad_left_decoder) + 1):(1 - pad_right))].unsqueeze((- 1))], dim=2)
            y_coarse = coarse[(:, (pad_left + 1):(1 - pad_right))]
            y_fine = fine[(:, (pad_left + 1):(1 - pad_right))]
            if self.noise_x:
                total_len = coarse_f.size(1)
                translated = []
                for j in range(coarse_f.size(0)):
                    shift = (random.randrange(256) - 128)
                    translated.append(noisy_f[(j, ((pad_left - pad_left_encoder) + shift):((total_len - extra_pad_right) + shift))])
                translated = torch.stack(translated, dim=0)
            else:
                translated = noisy_f[(:, (pad_left - pad_left_encoder):)]
            (p_cf, vq_pen, encoder_pen, entropy) = self(speaker, x, translated)
            (p_c, p_f) = p_cf
            loss_c = criterion(p_c.transpose(1, 2).float(), y_coarse)
            loss_f = criterion(p_f.transpose(1, 2).float(), y_fine)
            encoder_weight = (0.01 * min(1, max(0.1, ((step / 1000) - 1))))
            loss = (((loss_c + loss_f) + vq_pen) + (encoder_weight * encoder_pen))
            optimiser.zero_grad()
            if use_half:
                optimiser.backward(loss)
                if do_clip:
                    raise RuntimeError('clipping in half precision is not implemented yet')
            else:
                loss.backward()
                if do_clip:
                    max_grad = 0
                    max_grad_name = ''
                    for (name, param) in self.named_parameters():
                        if (param.grad is not None):
                            param_max_grad = param.grad.data.abs().max()
                            if (param_max_grad > max_grad):
                                max_grad = param_max_grad
                                max_grad_name = name
                            if (1000000 < param_max_grad):
                                logger.log(f'Very large gradient at {name}: {param_max_grad}')
                    if (100 < max_grad):
                        for param in self.parameters():
                            if (param.grad is not None):
                                if (1000000 < max_grad):
                                    param.grad.data.zero_()
                                else:
                                    param.grad.data.mul_((100 / max_grad))
                    if (running_max_grad < max_grad):
                        running_max_grad = max_grad
                        running_max_grad_name = max_grad_name
                    if (100000 < max_grad):
                        torch.save(self.state_dict(), 'bad_model.pyt')
                        raise RuntimeError('Aborting due to crazy gradient (model saved to bad_model.pyt)')
            optimiser.step()
            if ((e == 0) and (i == 0)):
                lr_scheduler.step()
                print('schedulre!')
            running_loss_c += loss_c.item()
            running_loss_f += loss_f.item()
            running_loss_vq += vq_pen.item()
            running_loss_vqc += encoder_pen.item()
            running_entropy += entropy
            self.after_update()
            speed = ((i + 1) / (time.time() - start))
            avg_loss_c = (running_loss_c / (i + 1))
            avg_loss_f = (running_loss_f / (i + 1))
            avg_loss_vq = (running_loss_vq / (i + 1))
            avg_loss_vqc = (running_loss_vqc / (i + 1))
            avg_entropy = (running_entropy / (i + 1))
            step += 1
            k = (step // 1000)
            logger.status(f'Epoch: {(e + 1)}/{epochs} -- Batch: {(i + 1)}/{iters} -- Loss: c={avg_loss_c:#.4} f={avg_loss_f:#.4} vq={avg_loss_vq:#.4} vqc={avg_loss_vqc:#.4} -- Entropy: {avg_entropy:#.4} -- Grad: {running_max_grad:#.1} {running_max_grad_name} Speed: {speed:#.4} steps/sec -- Step: {k}k ')
        os.makedirs(paths.checkpoint_dir, exist_ok=True)
        torch.save(self.state_dict(), paths.model_path())
        np.save(paths.step_path(), step)
        logger.log_current_status()
        logger.log(f' <saved>; w[0][0] = {self.overtone.wavernn.gru.weight_ih_l0[0][0]}')
        if (k > (saved_k + 50)):
            torch.save(self.state_dict(), paths.model_hist_path(step))
            saved_k = k
            self.do_generate(paths, step, dataset.path, valid_index)

from lib.elbo_depth import gaussian_log_prob, laplacian_log_prob
from lib.utils.torch_utils import apply_dropout
from tqdm import tqdm
import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from time import time
import os


def pixel_wise_calibration_curve(model, x_t, true_img, mask, l1_likelihood, S=50):
    true_img = true_img.view((- 1))
    mask = mask.view((- 1))
    preds = []
    vars_aleatoric = []
    model.eval()
    model.apply(apply_dropout)
    with torch.no_grad():
        for _ in range(S):
            (pred, logvar_aleatoric) = model(x_t)
            preds.append(pred.cpu().view((- 1)))
            vars_aleatoric.append(logvar_aleatoric.exp().cpu().view((- 1)))
        del x_t
    model.train()
    probs_img = np.zeros(true_img.size(0))
    for i in range(S):
        if l1_likelihood:
            dist = torch.distributions.Laplace(preds[i], vars_aleatoric[i].sqrt())
        else:
            dist = torch.distributions.Normal(preds[i], vars_aleatoric[i].sqrt())
        probs_img += (dist.cdf(true_img).numpy() / S)
        preds[i] = preds[i].numpy()
        vars_aleatoric[i] = vars_aleatoric[i].numpy()
    var_aleatoric = np.array(vars_aleatoric).mean(0)
    preds = np.array(preds)
    preds_mean = preds.mean(0)
    preds_var_model = ((np.square(preds).mean(0) - np.square(preds_mean)) + 1e-08)
    preds_var = (preds_var_model + var_aleatoric)
    sharpness = preds_var[mask.numpy()].mean()
    n_levels = 10
    true_freq = np.linspace(0.0, 1.0, n_levels)
    pred_freq = np.zeros_like(true_freq)
    probs_masked = probs_img[mask.numpy()]
    for (i, level) in enumerate(true_freq):
        mask_level = (probs_masked <= level).astype(np.float32)
        if (mask_level.sum() > 0.0):
            pred_freq[i] = mask_level.mean()
        else:
            pred_freq[i] = 0.0
    calibration = (((true_freq - pred_freq) ** 2) * 1.0).sum()
    return (pred_freq, true_freq, calibration, sharpness, preds_mean, preds_var_model, var_aleatoric)

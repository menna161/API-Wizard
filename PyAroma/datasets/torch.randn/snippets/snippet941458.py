import torch
import math
import numpy as np
import matplotlib.pyplot as plt
from ..elbo_depth import weight_aleatoric
import cv2
import os


def pixel_wise_calibration_curve(true_img, mean_pred, std_pred_model, std_pred_aleatoric, mask_test, likelihood, c_threshold=None, S=50):
    true_img = true_img.view((- 1)).cpu()
    mean_pred = mean_pred.view((- 1)).cpu()
    mask = mask_test.view((- 1)).cpu()
    std_pred_model = std_pred_model.view((- 1)).cpu()
    std_pred_aleatoric = std_pred_aleatoric.view((- 1)).cpu()
    std_pred = (torch.pow(std_pred_model, 2) + torch.pow(std_pred_aleatoric, 2)).sqrt()
    if (likelihood == 'gaussian'):
        dist = torch.distributions.Normal(mean_pred, std_pred)
        probs_img = dist.cdf(true_img).cpu().detach().numpy()
    else:
        probs_img = torch.zeros_like(true_img)
        for s in range(S):
            eps = torch.randn_like(std_pred_model)
            f = (mean_pred + (std_pred_model * eps))
            if (likelihood == 'laplace'):
                scale = (std_pred_aleatoric / np.sqrt(2.0))
                dist = torch.distributions.Laplace(f, scale)
                probs_img += (dist.cdf(true_img) / S)
            elif (likelihood == 'berhu'):
                w_threshold = weight_aleatoric(c_threshold).cpu().numpy()
                scale = (std_pred_aleatoric / np.sqrt(w_threshold))
                probs_img += (berhu_cdf(true_img, f, scale, c_threshold.cpu()) / S)
        probs_img = probs_img.numpy()
    sharpness = (std_pred ** 2)[mask].mean().item()
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
    return (pred_freq, true_freq, calibration, sharpness)

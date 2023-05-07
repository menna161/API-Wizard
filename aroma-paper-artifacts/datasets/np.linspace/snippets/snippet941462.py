import numpy as np
import torch
import matplotlib.pyplot as plt
import os


def calibration_per_image(probs, mask, y):
    mask_probs = mask[(:, np.newaxis, :)].repeat(probs.shape[1], 1)
    probs = probs.flatten()[mask_probs.flatten()]
    mask = mask.flatten()
    y = y.flatten()[mask]
    y = np.eye(11)[y].transpose().flatten()
    n_levels = 10
    true_freq = np.linspace(0.0, 1.0, n_levels)
    obs_freq = np.zeros_like(true_freq)
    pred_freq = np.zeros_like(true_freq)
    level_prev = 0.0
    for (i, level) in enumerate(true_freq):
        mask_level = ((probs > level_prev) & (probs <= level))
        if (mask_level.astype(np.float32).sum() < 1.0):
            pred_freq[i] = 0.0
            obs_freq[i] = 0.0
        else:
            pred_freq[i] = probs[mask_level].mean()
            obs_freq[i] = y[mask_level].mean()
        level_prev = level
    calibration = (((obs_freq - pred_freq) ** 2) * 1.0).sum()
    idx = np.argsort(pred_freq)
    return (obs_freq[idx], pred_freq[idx], calibration)

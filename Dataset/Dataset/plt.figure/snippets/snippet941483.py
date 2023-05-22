from lib.elbo_depth import gaussian_log_prob, laplacian_log_prob
from lib.utils.torch_utils import apply_dropout
from tqdm import tqdm
import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
from time import time
import os


def test(model, x_test, y_test, idx, mask_test, epoch, dataset, l1_likelihood, trainset=False, saveplot=False):
    (pred_freq, true_freq, calibration, sharpness, img_pred, var_model, var_aleatoric) = pixel_wise_calibration_curve(model, x_test, y_test, mask_test, l1_likelihood)
    if (dataset == 'make3d'):
        C = 70.0
        (H, W) = (168, 224)
        im_ratio = float((H / W))
    sharpness *= (C ** 2)
    x_test = x_test.view(3, H, W).permute(1, 2, 0).cpu().numpy()
    _x_test = np.zeros_like(x_test)
    _x_test[(:, :, 0)] = x_test[(:, :, 2)]
    _x_test[(:, :, 1)] = x_test[(:, :, 1)]
    _x_test[(:, :, 2)] = x_test[(:, :, 0)]
    x_test = _x_test
    y_test = (C * y_test).view(H, W).numpy()
    img_pred = (C * img_pred).reshape(H, W)
    img_std_model = (C * np.sqrt(var_model)).reshape(H, W)
    img_std_aleatoric = (C * np.sqrt(var_aleatoric).reshape(H, W))
    mask_test = mask_test.view(H, W).numpy()
    RMSE = np.sqrt(np.square((img_pred - y_test)[mask_test]).mean())
    mean_log10_error = np.abs((np.log10(img_pred) - np.log10(y_test)))[mask_test].mean()
    mean_abs_rel_error = np.abs(((img_pred - y_test) / y_test))[mask_test].mean()
    _rgb_true = cv2.resize(x_test, None, fx=float((H / W)), fy=float((W / H)))
    _img_true = cv2.resize(y_test, None, fx=float((H / W)), fy=float((W / H)))
    _img_pred = cv2.resize(img_pred, None, fx=float((H / W)), fy=float((W / H)))
    _img_std_model = cv2.resize(img_std_model, None, fx=float((H / W)), fy=float((W / H)))
    _img_std_aleatoric = cv2.resize(img_std_aleatoric, None, fx=float((H / W)), fy=float((W / H)))
    if saveplot:
        print('Img idx: {} || Calibration score: {:4f} || Sharpness score: {:4f}'.format(idx, calibration, sharpness))
        (vmin_, vmax_) = (1.75, 35.0)
        fig = plt.figure(1, figsize=(12, 2))
        ax1 = plt.subplot(171)
        im1 = ax1.imshow(_rgb_true)
        ax1.axis('off')
        ax2 = plt.subplot(172)
        im2 = ax2.imshow(_img_true, cmap='magma', vmin=vmin_, vmax=vmax_)
        ax2.axis('off')
        cb2 = fig.colorbar(im2, ax=ax2, fraction=(0.046 * im_ratio), pad=0.04)
        cb2.ax.tick_params(labelsize=5)
        cb2.ax.tick_params(size=0)
        ax3 = plt.subplot(173)
        im3 = ax3.imshow(_img_pred, cmap='magma', vmin=vmin_, vmax=vmax_)
        ax3.axis('off')
        cb3 = fig.colorbar(im3, ax=ax3, fraction=(0.046 * im_ratio), pad=0.04)
        cb3.ax.tick_params(labelsize=5)
        cb3.ax.tick_params(size=0)
        ax4 = plt.subplot(174)
        im4 = ax4.imshow(np.sqrt(((_img_std_aleatoric ** 2) + (_img_std_model ** 2))), cmap='nipy_spectral')
        ax4.axis('off')
        cb4 = fig.colorbar(im4, ax=ax4, fraction=(0.046 * im_ratio), pad=0.04, format='%d')
        cb4.ax.tick_params(labelsize=5)
        cb4.ax.tick_params(size=0)
        ax5 = plt.subplot(175)
        ax5.set_aspect(im_ratio)
        ax5.xaxis.set_tick_params(labelsize=5)
        ax5.yaxis.set_tick_params(labelsize=5)
        ax5.plot(pred_freq, true_freq, color='red')
        ax5.plot([0.0, 1.0], [0.0, 1.0], 'g--')
        plt.tight_layout()
        if trainset:
            plt.savefig('results_{}_mcd_results_train_pred_{}.pdf'.format(dataset, idx), bbox_inches='tight', pad_inches=0.1)
        else:
            plt.savefig('results_{}_mcd_results_test_pred_{}.pdf'.format(dataset, idx), bbox_inches='tight', pad_inches=0.1)
        plt.close()
    return (calibration, sharpness, RMSE, mean_log10_error, mean_abs_rel_error, img_pred.reshape(1, (- 1)), y_test.reshape(1, (- 1)), mask_test.reshape(1, (- 1)))

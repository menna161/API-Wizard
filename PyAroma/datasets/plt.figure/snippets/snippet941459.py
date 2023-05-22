import torch
import math
import numpy as np
import matplotlib.pyplot as plt
from ..elbo_depth import weight_aleatoric
import cv2
import os


def test(model, img_test, y_test, idx, mask_test, dataset, exp_name, likelihood, c_threshold=None, trainset=False, saveplot=False):
    if (likelihood == 'berhu'):
        w_threshold = weight_aleatoric(c_threshold)
        (mean_pred, var_model_pred, var_aleatoric_pred) = model.predict(img_test, w_threshold)
    elif (likelihood == 'laplace'):
        w_threshold = 2.0
        (mean_pred, var_model_pred, var_aleatoric_pred) = model.predict(img_test, w_threshold)
    elif (likelihood == 'gaussian'):
        (mean_pred, var_model_pred, var_aleatoric_pred) = model.predict(img_test)
    if (dataset == 'make3d'):
        C = 70.0
        (H, W) = (168, 224)
    std_model_pred = var_model_pred.sqrt()
    std_aleatoric_pred = var_aleatoric_pred.sqrt()
    (pred_freq, true_freq, calibration, sharpness) = pixel_wise_calibration_curve(y_test, mean_pred, std_model_pred, std_aleatoric_pred, mask_test, likelihood, c_threshold=c_threshold)
    sharpness *= (C ** 2)
    mean_pred *= C
    y_test *= C
    std_model_pred *= C
    std_aleatoric_pred *= C
    im_ratio = float((H / W))
    img_test = img_test.view(3, H, W).permute(1, 2, 0).cpu().numpy()
    _img_test = np.zeros_like(img_test)
    _img_test[(:, :, 0)] = img_test[(:, :, 2)]
    _img_test[(:, :, 1)] = img_test[(:, :, 1)]
    _img_test[(:, :, 2)] = img_test[(:, :, 0)]
    img_test = _img_test
    mean_pred = mean_pred.view(H, W).cpu()
    y_test = y_test.view(H, W).cpu()
    mask_test = mask_test.view(H, W).cpu()
    std_model_pred = std_model_pred.view(H, W).cpu()
    std_aleatoric_pred = std_aleatoric_pred.view(H, W).cpu()
    RMSE = torch.sqrt(torch.pow((mean_pred - y_test), 2)[mask_test].mean())
    mean_log10_error = torch.abs((torch.log10(mean_pred) - torch.log10(y_test)))[mask_test].mean()
    mean_abs_rel_error = torch.abs(((mean_pred - y_test) / y_test))[mask_test].mean()
    if saveplot:
        print('Img idx: {} || Calibration score: {:4f} || Sharpness score: {:4f}'.format(idx, calibration, sharpness))
        rgb_true = cv2.resize(img_test, None, fx=float((H / W)), fy=float((W / H)))
        img_true = cv2.resize(y_test.numpy(), None, fx=float((H / W)), fy=float((W / H)))
        img_pred = cv2.resize(mean_pred.numpy(), None, fx=float((H / W)), fy=float((W / H)))
        (vmin_, vmax_) = (1.75, 35.0)
        img_std_aleatoric = cv2.resize(std_aleatoric_pred.numpy(), None, fx=float((H / W)), fy=float((W / H)))
        img_std_model = cv2.resize(std_model_pred.numpy(), None, fx=float((H / W)), fy=float((W / H)))
        fig = plt.figure(1, figsize=(12, 2))
        ax1 = plt.subplot(171)
        im1 = ax1.imshow(rgb_true)
        ax1.axis('off')
        ax2 = plt.subplot(172)
        im2 = ax2.imshow(img_true, cmap='magma', vmin=vmin_, vmax=vmax_)
        ax2.axis('off')
        cb2 = fig.colorbar(im2, ax=ax2, fraction=(0.046 * im_ratio), pad=0.04)
        cb2.ax.tick_params(labelsize=5)
        cb2.ax.tick_params(size=0)
        ax3 = plt.subplot(173)
        im3 = ax3.imshow(img_pred, cmap='magma', vmin=vmin_, vmax=vmax_)
        ax3.axis('off')
        cb3 = fig.colorbar(im3, ax=ax3, fraction=(0.046 * im_ratio), pad=0.04)
        cb3.ax.tick_params(labelsize=5)
        cb3.ax.tick_params(size=0)
        ax4 = plt.subplot(174)
        im4 = ax4.imshow(np.sqrt(((img_std_aleatoric ** 2) + (img_std_model ** 2))), cmap='nipy_spectral')
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
            plt.savefig('{}_{}_results_train_pred_{}.pdf'.format(dataset, exp_name, idx), bbox_inches='tight', pad_inches=0.1)
        else:
            plt.savefig('{}_{}_results_test_pred_{}.pdf'.format(dataset, exp_name, idx), bbox_inches='tight', pad_inches=0.1)
        plt.close()
    return (calibration, sharpness, RMSE, mean_log10_error, mean_abs_rel_error, mean_pred.view(1, (- 1)), y_test.view(1, (- 1)), mask_test.view(1, (- 1)))

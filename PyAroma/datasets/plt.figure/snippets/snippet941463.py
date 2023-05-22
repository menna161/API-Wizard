import numpy as np
import torch
import matplotlib.pyplot as plt
import os


def plot_per_image(rgb, ground_truth, pred, pred_entropy, probs, mask, dataset, exp_name, idx, deterministic=False):
    if (dataset == 'camvid'):
        (H, W) = (360, 480)
    im_ratio = float((H / W))
    rgb = rgb.view(3, H, W).permute(1, 2, 0).numpy()
    ground_truth = ground_truth.view(H, W).numpy()
    pred = pred.view(H, W).numpy()
    fig = plt.figure(1, figsize=(12, 2))
    ax1 = plt.subplot(151)
    im1 = ax1.imshow(rgb)
    ax1.axis('off')
    ax2 = plt.subplot(152)
    im2 = ax2.imshow(ground_truth)
    ax2.axis('off')
    ax3 = plt.subplot(153)
    im3 = ax3.imshow(pred)
    ax3.axis('off')
    if (not deterministic):
        pred_entropy = pred_entropy.view(H, W).numpy()
        probs = probs.numpy()
        mask = mask.view(1, (- 1)).numpy()
        ax4 = plt.subplot(154)
        im4 = ax4.imshow(pred_entropy, vmin=0.0, vmax=np.log(11.0))
        ax4.axis('off')
        cb4 = fig.colorbar(im4, ax=ax4, fraction=(0.046 * im_ratio), pad=0.04)
        cb4.ax.tick_params(labelsize=0)
        cb4.ax.tick_params(size=0)
        (true_freq, pred_freq, calibration) = calibration_per_image(probs, mask, ground_truth)
        print('Img: {} || Calibration: {:.5f}'.format(idx, calibration))
        ax5 = plt.subplot(155)
        ax5.set_aspect(im_ratio)
        ax5.xaxis.set_tick_params(labelsize=5)
        ax5.yaxis.set_tick_params(labelsize=5)
        ax5.plot(pred_freq, true_freq, color='red')
        ax5.plot([0.0, 1.0], [0.0, 1.0], 'g--')
        np.savetxt('{}_{}_calibration_score_{}.txt'.format(dataset, exp_name, idx), [calibration])
    plt.savefig('{}_{}_results_test_pred_{}.pdf'.format(dataset, exp_name, idx), bbox_inches='tight', pad_inches=0.1)
    plt.close()

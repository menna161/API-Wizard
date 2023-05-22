from . import dvf_generation
from . import intensity_augmentation
import os
import time
import SimpleITK as sitk
import numpy as np
import logging
import functions.image.image_processing as ip
import functions.setting.setting_utils as su
import matplotlib.pyplot as plt


def dvf_statistics(setting, dvf, spacing=None, im_info=None, stage=None):
    im_info_su = {'data': im_info['data'], 'deform_exp': im_info['deform_exp'], 'type_im': im_info['type_im'], 'cn': im_info['cn'], 'dsmooth': im_info['dsmooth'], 'stage': stage, 'padto': im_info['padto']}
    max_dvf = np.max(setting['deform_exp'][im_info['deform_exp']]['MaxDeform'])
    import matplotlib.pyplot as plt
    plt.figure()
    plt.hist(np.ravel(dvf), log=True, bins=np.arange((- max_dvf), (max_dvf + 1)))
    plt.draw()
    plt.savefig(su.address_generator(setting, 'DVF_histogram', **im_info_su))
    plt.close()
    jac = ip.calculate_jac(dvf, spacing)
    sitk.WriteImage(sitk.GetImageFromArray(jac.astype(np.float32)), su.address_generator(setting, 'Jac', **im_info_su))
    jac_hist_max = 3
    jac_hist_min = (- 1)
    step_h = 0.2
    if (np.max(jac) > jac_hist_max):
        jac_hist_max = np.ceil(np.max(jac))
    if (np.min(jac) < jac_hist_min):
        jac_hist_min = np.floor(np.min(jac))
    plt.figure()
    plt.hist(np.ravel(jac), log=True, bins=np.arange(jac_hist_min, (jac_hist_max + step_h), step_h))
    plt.title('min(Jac)={:.2f}, max(Jac)={:.2f}'.format(np.min(jac), np.max(jac)))
    plt.draw()
    plt.savefig(su.address_generator(setting, 'Jac_histogram', **im_info_su))
    plt.close()

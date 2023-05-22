from . import utils as ag_utils
import copy
from joblib import Parallel, delayed
import logging
import multiprocessing
import numpy as np
import os
import SimpleITK as sitk
import scipy.ndimage as ndimage
import functions.image.image_processing as ip
import functions.setting.setting_utils as su


def respiratory_motion(setting, im_info, stage, moving_image_mode='Exhale'):
    "\n    Respiratory motion consists of four deformations: [2009 Hub A stochastic approach to estimate the uncertainty]\n        1) Extension of the Chest in the Transversal Plane with scale of s0\n        2) Decompression of the Lung in Cranio-Caudal Direction with maximum of t0\n        3) Random Deformation\n        4) Tissue Sliding Between Lung and Rib Cage (not implemented yet)\n    :param setting:\n    :param im_info:\n    :param stage:\n    :param moving_image_mode: 'Exhale' : mode_coeff = 1, 'Inhale': mode_coeff = -1\n                               dvf[:, :, :, 2] = mode_coeff * dvf_craniocaudal\n                               dvf[:, :, :, 1] = mode_coeff * dvf_anteroposterior\n    :return:\n    "
    im_info_su = {'data': im_info['data'], 'deform_exp': im_info['deform_exp'], 'type_im': im_info['type_im'], 'cn': im_info['cn'], 'dsmooth': im_info['dsmooth'], 'stage': stage, 'padto': im_info['padto']}
    seed_number = ag_utils.seed_number_by_im_info(im_info, 'respiratory_motion', stage=stage)
    random_state = np.random.RandomState(seed_number)
    deform_number = im_info['deform_number']
    t0_max = setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_t0'][deform_number]
    s0_max = setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_s0'][deform_number]
    max_deform = (setting['deform_exp'][im_info['deform_exp']]['MaxDeform'] * setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_MaxDeformRatio'][deform_number])
    max_deform_single_freq = (setting['deform_exp'][im_info['deform_exp']]['MaxDeform'] * setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_SingleFrequency_MaxDeformRatio'][deform_number])
    grid_border_to_zero = setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_SetGridBorderToZero'][deform_number]
    grid_spacing = setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_BSplineGridSpacing'][deform_number]
    grid_smoothing_sigma = [(i / stage) for i in setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_GridSmoothingSigma'][deform_number]]
    t0 = random_state.uniform((0.8 * t0_max), (1.1 * t0_max))
    s0 = random_state.uniform((0.8 * s0_max), (1.1 * s0_max))
    if (moving_image_mode == 'Inhale'):
        mode_coeff = (- 1)
    else:
        mode_coeff = 1
    im_sitk = sitk.ReadImage(su.address_generator(setting, 'Im', **im_info_su))
    lung_im = sitk.GetArrayFromImage(sitk.ReadImage(su.address_generator(setting, 'Lung', **im_info_su))).astype(np.bool)
    i_lung = np.where(lung_im)
    diaphragm_slice = np.min(i_lung[0])
    anteroposterior_dim = 1
    shift_of_center_scale = random_state.uniform(2, 12)
    center_scale = np.round((np.max(i_lung[anteroposterior_dim]) - (shift_of_center_scale / stage)))
    logging.debug(('Diaphragm slice is ' + str(diaphragm_slice)))
    indices = ([None] * 3)
    (indices[0], indices[1], indices[2]) = [(i * stage) for i in np.meshgrid(np.arange(0, np.shape(lung_im)[0]), np.arange(0, np.shape(lung_im)[1]), np.arange(0, np.shape(lung_im)[2]), indexing='ij')]
    scale_transversal_plane = np.ones(np.shape(lung_im)[0])
    dvf_anteroposterior = np.zeros(np.shape(lung_im))
    dvf_craniocaudal = np.zeros(np.shape(lung_im))
    lung_extension = ((np.max(i_lung[0]) - diaphragm_slice) / 2)
    alpha = (1.3 / lung_extension)
    for z in range(np.shape(scale_transversal_plane)[0]):
        if (z < diaphragm_slice):
            scale_transversal_plane[z] = (1 + s0)
            dvf_craniocaudal[(z, :, :)] = t0
        elif (diaphragm_slice <= z < (diaphragm_slice + lung_extension)):
            scale_transversal_plane[z] = (1 + (s0 * (1 - (np.log((1 + ((z - diaphragm_slice) * alpha))) / np.log((1 + (lung_extension * alpha)))))))
            dvf_craniocaudal[(z, :, :)] = (t0 * (1 - (np.log((1 + ((z - diaphragm_slice) * alpha))) / np.log((1 + (lung_extension * alpha))))))
        else:
            scale_transversal_plane[z] = 1
            dvf_craniocaudal[(z, :, :)] = 0
        dvf_anteroposterior[(z, :, :)] = ((indices[anteroposterior_dim][(z, :, :)] - center_scale) * (scale_transversal_plane[z] - 1))
    dvf = np.zeros((list(np.shape(lung_im)) + [3]))
    dvf[(:, :, :, 2)] = (mode_coeff * dvf_craniocaudal)
    dvf[(:, :, :, 1)] = ((- mode_coeff) * dvf_anteroposterior)
    bcoeff = bspline_coeff(im_sitk, max_deform_single_freq, grid_border_to_zero, grid_smoothing_sigma, grid_spacing, random_state, dim_im=3, artificial_generation='respiratory_motion')
    dvf_single_freq_filter = sitk.TransformToDisplacementFieldFilter()
    dvf_single_freq_filter.SetSize(im_sitk.GetSize())
    dvf_single_freq_sitk = dvf_single_freq_filter.Execute(bcoeff)
    dvf_single_freq = sitk.GetArrayFromImage(dvf_single_freq_sitk)
    if setting['deform_exp'][im_info['deform_exp']]['DVFNormalization']:
        dvf_single_freq = normalize_dvf(dvf_single_freq, max_deform)
    dvf_single_freq[(:, :, :, 2)] = (dvf_single_freq[(:, :, :, 2)] * 0.3)
    dvf = (dvf + dvf_single_freq)
    mask_to_zero = setting['deform_exp'][im_info['deform_exp']]['MaskToZero']
    if (mask_to_zero is not None):
        sigma = setting['deform_exp'][im_info['deform_exp']]['RespiratoryMotion_BackgroundSmoothingSigma'][deform_number]
        dvf = do_mask_to_zero_gaussian(setting, im_info_su, dvf, mask_to_zero, stage, max_deform, sigma)
    else:
        raise ValueError('In the current implementation, respiratory_motion is not valid without mask_to_zero')
    if setting['deform_exp'][im_info['deform_exp']]['DVFNormalization']:
        dvf = normalize_dvf(dvf, (max_deform * 1.2))
    return dvf

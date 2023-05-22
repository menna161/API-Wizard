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


def mixed_freq(setting, im_info, stage):
    im_info_su = {'data': im_info['data'], 'deform_exp': im_info['deform_exp'], 'type_im': im_info['type_im'], 'cn': im_info['cn'], 'dsmooth': im_info['dsmooth'], 'stage': stage, 'padto': im_info['padto']}
    seed_number = ag_utils.seed_number_by_im_info(im_info, 'mixed_freq', stage=stage)
    random_state = np.random.RandomState(seed_number)
    deform_number = im_info['deform_number']
    max_deform = (setting['deform_exp'][im_info['deform_exp']]['MaxDeform'] * setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_MaxDeformRatio'][deform_number])
    grid_smoothing_sigma = [(i / stage) for i in setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_GridSmoothingSigma'][deform_number]]
    grid_border_to_zero = setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_SetGridBorderToZero'][deform_number]
    grid_spacing = setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_BSplineGridSpacing'][deform_number]
    number_dilation = setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_Np'][deform_number]
    im_canny_address = su.address_generator(setting, 'ImCanny', **im_info_su)
    im_sitk = sitk.ReadImage(su.address_generator(setting, 'Im', **im_info_su))
    if os.path.isfile(im_canny_address):
        im_canny_sitk = sitk.ReadImage(im_canny_address)
    else:
        im_canny_sitk = sitk.CannyEdgeDetection(sitk.Cast(im_sitk, sitk.sitkFloat32), lowerThreshold=setting['deform_exp'][im_info['deform_exp']]['Canny_LowerThreshold'], upperThreshold=setting['deform_exp'][im_info['deform_exp']]['Canny_UpperThreshold'])
        sitk.WriteImage(sitk.Cast(im_canny_sitk, sitk.sitkInt8), im_canny_address)
    lung_im = sitk.GetArrayFromImage(sitk.ReadImage(su.address_generator(setting, 'Lung', **im_info_su))).astype(np.bool)
    im_canny = sitk.GetArrayFromImage(im_canny_sitk)
    lung_dilated = ndimage.binary_dilation(lung_im)
    available_region = np.logical_and(lung_dilated, im_canny)
    available_region = np.tile(np.expand_dims(available_region, axis=(- 1)), 3)
    dilated_edge = np.copy(available_region)
    itr_edge = 0
    i_edge = ([None] * 3)
    select_voxel = ([None] * 3)
    block_low = ([None] * 3)
    block_high = ([None] * 3)
    for dim in range(3):
        i_edge[dim] = np.where((available_region[(:, :, :, dim)] > 0))
    if ((len(i_edge[0][0]) == 0) or (len(i_edge[1][0]) == 0) or (len(i_edge[2][0]) == 0)):
        logging.debug('dvf_generation: We are out of points. Plz change the threshold value of Canny method!!!!! ')
    while ((len(i_edge[0][0]) > 4) and (len(i_edge[1][0]) > 4) and (len(i_edge[2][0]) > 4) and (itr_edge < number_dilation)):
        no_more_dilatation_in_this_region = False
        for dim in range(3):
            select_voxel[dim] = int(random_state.randint(0, (len(i_edge[dim][0]) - 1), 1, dtype=np.int64))
            (block_low[dim], block_high[dim]) = center_to_block(setting, center=np.array([i_edge[dim][0][select_voxel[dim]], i_edge[dim][1][select_voxel[dim]], i_edge[dim][2][select_voxel[dim]]]), radius=round((setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_BlockRadius'] / stage)), im_ref=im_sitk)
        if (itr_edge == 0):
            struct = np.ones((3, 3, 3), dtype=bool)
            for dim in range(3):
                dilated_edge[(:, :, :, dim)] = ndimage.binary_dilation(dilated_edge[(:, :, :, dim)], structure=struct)
        elif (itr_edge < np.round(((10 * number_dilation) / 12))):
            no_more_dilatation_in_this_region = True
            for dim in range(3):
                dilated_edge[(block_low[dim][0]:block_high[dim][0], block_low[dim][1]:block_high[dim][1], block_low[dim][2]:block_high[dim][2], dim)] = False
        elif (itr_edge < np.round(((11 * number_dilation) / 12))):
            struct = ndimage.generate_binary_structure(3, 2)
            for dim in range(3):
                mask_for_edge_dilation = np.zeros(np.shape(dilated_edge[(:, :, :, dim)]), dtype=bool)
                mask_for_edge_dilation[(block_low[dim][0]:block_high[dim][0], block_low[dim][1]:block_high[dim][1], block_low[dim][2]:block_high[dim][2])] = True
                dilated_edge[(:, :, :, dim)] = ndimage.binary_dilation(dilated_edge[(:, :, :, dim)], structure=struct, mask=mask_for_edge_dilation)
            if ((itr_edge % 2) == 0):
                no_more_dilatation_in_this_region = True
        elif (itr_edge < number_dilation):
            struct = np.zeros((9, 9, 9), dtype=bool)
            if ((itr_edge % 3) == 0):
                struct[(0:5, :, :)] = True
            if ((itr_edge % 3) == 1):
                struct[(:, 0:5, :)] = True
            if ((itr_edge % 3) == 2):
                struct[(:, :, 0:5)] = True
            for dim in range(3):
                mask_for_edge_dilation = np.zeros(np.shape(dilated_edge[(:, :, :, dim)]), dtype=bool)
                mask_for_edge_dilation[(block_low[dim][0]:block_high[dim][0], block_low[dim][1]:block_high[dim][1], block_low[dim][2]:block_high[dim][2])] = True
                dilated_edge[(:, :, :, dim)] = ndimage.binary_dilation(dilated_edge[(:, :, :, dim)], structure=struct, mask=mask_for_edge_dilation)
            if (random_state.uniform() > 0.3):
                no_more_dilatation_in_this_region = True
        if no_more_dilatation_in_this_region:
            available_region[(block_low[dim][0]:block_high[dim][0], block_low[dim][1]:block_high[dim][1], block_low[dim][2]:block_high[dim][2], dim)] = False
        if (itr_edge >= np.round(((10 * number_dilation) / 12))):
            for dim in range(3):
                i_edge[dim] = np.where((available_region[(:, :, :, dim)] > 0))
        itr_edge += 1
    bcoeff = bspline_coeff(im_sitk, max_deform, grid_border_to_zero, grid_smoothing_sigma, grid_spacing, random_state, dim_im=3, artificial_generation='mixed_frequency')
    dvf_filter = sitk.TransformToDisplacementFieldFilter()
    dvf_filter.SetSize(im_sitk.GetSize())
    smoothed_values_sitk = dvf_filter.Execute(bcoeff)
    smoothed_values = sitk.GetArrayFromImage(smoothed_values_sitk)
    dvf = (dilated_edge.astype(np.float64) * smoothed_values).astype(np.float64)
    if (setting[('DVFPad_S' + str(stage))] > 0):
        pad = setting[('DVFPad_S' + str(stage))]
        dvf = np.pad(dvf, ((pad, pad), (pad, pad), (pad, pad), (0, 0)), 'constant', constant_values=(0,))
    sigma_range = setting['deform_exp'][im_info['deform_exp']]['MixedFrequency_SigmaRange'][deform_number]
    sigma = random_state.uniform(low=(sigma_range[0] / stage), high=(sigma_range[1] / stage), size=3)
    dvf = smooth_dvf(dvf, sigma_blur=sigma, parallel_processing=setting['ParallelSearching'])
    if setting['deform_exp'][im_info['deform_exp']]['DVFNormalization']:
        dvf = normalize_dvf(dvf, max_deform)
    return dvf

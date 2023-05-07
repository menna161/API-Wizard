from . import utils as ag_utils
import os
import time
import SimpleITK as sitk
import scipy.ndimage as ndimage
import numpy as np
import functions.image.image_processing as ip
import functions.setting.setting_utils as su


def add_occlusion(setting, im_info, stage, deformed_im_previous_sitk=None, dvf_sitk=None):
    im_info_su = {'data': im_info['data'], 'deform_exp': im_info['deform_exp'], 'type_im': im_info['type_im'], 'cn': im_info['cn'], 'dsmooth': im_info['dsmooth'], 'stage': 1, 'padto': im_info['padto']}
    seed_number = ag_utils.seed_number_by_im_info(im_info, 'add_occlusion', stage=stage)
    random_state = np.random.RandomState(seed_number)
    if (deformed_im_previous_sitk is None):
        deformed_im_previous_sitk = sitk.ReadImage(su.address_generator(setting, 'DeformedIm', deformed_im_ext='Noise', **im_info_su))
    if (dvf_sitk is None):
        dvf_address = su.address_generator(setting, 'DeformedDVF', **im_info_su)
        dvf_sitk = sitk.ReadImage(dvf_address)
    deformed_lung_address = su.address_generator(setting, 'DeformedLung', **im_info_su)
    if (not os.path.isfile(deformed_lung_address)):
        im_lung_sitk = sitk.ReadImage(su.address_generator(setting, 'Lung', **im_info_su))
        dvf_t = sitk.DisplacementFieldTransform(sitk.Cast(dvf_sitk, sitk.sitkVectorFloat64))
        deformed_lung_sitk = ip.resampler_by_transform(im_lung_sitk, dvf_t, im_ref=deformed_im_previous_sitk, default_pixel_value=0, interpolator=sitk.sitkNearestNeighbor)
        sitk.WriteImage(sitk.Cast(deformed_lung_sitk, sitk.sitkInt8), deformed_lung_address)
        time.sleep(5)
    deformed_im_noise = sitk.GetArrayFromImage(deformed_im_previous_sitk)
    deformed_lung = sitk.GetArrayFromImage(sitk.ReadImage(deformed_lung_address))
    struct = np.ones((9, 9, 9), dtype=bool)
    deformed_lung_erode = ndimage.binary_erosion(deformed_lung, structure=struct).astype(np.bool)
    ellipse_lung = np.zeros(deformed_im_noise.shape, dtype=np.bool)
    ellipse_center_lung = deformed_lung_erode.copy()
    for ellipse_number in range(setting['deform_exp'][im_info['deform_exp']]['Occlusion_NumberOfEllipse']):
        center_list = np.where((ellipse_center_lung > 0))
        selected_center_i = int(random_state.randint(0, (len(center_list[0]) - 1), 1, dtype=np.int64))
        a = (random_state.random_sample() * setting['deform_exp'][im_info['deform_exp']]['Occlusion_Max_a'])
        b = (random_state.random_sample() * setting['deform_exp'][im_info['deform_exp']]['Occlusion_Max_b'])
        c = (random_state.random_sample() * setting['deform_exp'][im_info['deform_exp']]['Occlusion_Max_c'])
        if (a < 3):
            a = 3
        if (b < 3):
            b = 3
        if (c < 3):
            c = 3
        ellipse_crop = np.zeros([((2 * round(a)) + 1), ((2 * round(b)) + 1), ((2 * round(c)) + 1)])
        for i1 in range(np.shape(ellipse_crop)[0]):
            for i2 in range(np.shape(ellipse_crop)[1]):
                for i3 in range(np.shape(ellipse_crop)[2]):
                    if ((((((i1 - a) / a) ** 2) + (((i2 - b) / b) ** 2)) + (((i3 - c) / c) ** 2)) < 1):
                        ellipse_crop[(i1, i2, i3)] = 1
        ellipse_lung[((center_list[0][selected_center_i] - round((a / 2))):((center_list[0][selected_center_i] - round((a / 2))) + np.shape(ellipse_crop)[0]), (center_list[1][selected_center_i] - round((b / 2))):((center_list[1][selected_center_i] - round((b / 2))) + np.shape(ellipse_crop)[1]), (center_list[2][selected_center_i] - round((c / 2))):((center_list[2][selected_center_i] - round((c / 2))) + np.shape(ellipse_crop)[2]))] = ellipse_crop
        margin = 5
        ellipse_center_lung[(((center_list[0][selected_center_i] - round((a / 2))) - margin):(((center_list[0][selected_center_i] - round((a / 2))) + np.shape(ellipse_crop)[0]) + margin), ((center_list[1][selected_center_i] - round((b / 2))) - margin):(((center_list[1][selected_center_i] - round((b / 2))) + np.shape(ellipse_crop)[1]) + margin), ((center_list[2][selected_center_i] - round((c / 2))) - margin):(((center_list[2][selected_center_i] - round((c / 2))) + np.shape(ellipse_crop)[2]) + margin))] = 0
    sitk.WriteImage(sitk.Cast(ip.array_to_sitk(ellipse_lung.astype(np.int8), im_ref=deformed_im_previous_sitk), sitk.sitkInt8), su.address_generator(setting, 'DeformedLungOccluded', **im_info_su))
    ellipse_lung_erode = ellipse_lung.copy().astype(np.bool)
    struct = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 1, 0], [1, 1, 1], [0, 1, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]]])
    weight_occluded_list = np.array([0.2, 0.6, 0.9])
    weight_image_list = (1 - weight_occluded_list)
    print('--------------------------------------will be corrected: occlusion intensity is not always an integer')
    print('--------------------------------------will be corrected: occlusion intensity is not always an integer')
    print('--------------------------------------will be corrected: occlusion intensity is not always an integer')
    occlusion_intensity = int(random_state.randint(setting['deform_exp'][im_info['deform_exp']]['Occlusion_IntensityRange'][0], setting['deform_exp'][im_info['deform_exp']]['Occlusion_IntensityRange'][1], 1, dtype=np.int64))
    for i in range(3):
        ellipse_lung_erode_new = ndimage.binary_erosion(ellipse_lung_erode, structure=struct).astype(np.bool)
        edge_lung = (ellipse_lung_erode ^ ellipse_lung_erode_new)
        i_edge = np.where(edge_lung)
        deformed_im_noise[i_edge] = ((deformed_im_noise[i_edge] * weight_image_list[i]) + (occlusion_intensity * weight_occluded_list[i]))
        ellipse_lung_erode = ellipse_lung_erode_new.copy()
    i_inside = np.where((ellipse_lung_erode_new > 0))
    deformed_im_noise[i_inside] = (occlusion_intensity + random_state.normal(scale=setting['deform_exp'][im_info['deform_exp']]['Im_NoiseSigma'], size=len(i_inside[0])))
    deformed_im_occluded_sitk = ip.array_to_sitk(deformed_im_noise, im_ref=deformed_im_previous_sitk)
    return deformed_im_occluded_sitk

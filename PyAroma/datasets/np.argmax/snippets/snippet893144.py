import copy
import logging
import numpy as np
import os
import SimpleITK as sitk
import tensorflow as tf
import time
import functions.image.image_processing as ip
import functions.network as network
import functions.setting.setting_utils as su
from functions.setting.experiment_setting import load_network_multi_stage_from_predefined


def multi_stage_error(setting, landmark_dict, pair_info, overwrite=False):
    '\n    :param setting:\n    :param pair_info: information of the pair to be registered.\n    :param overwrite:\n    :return: The output moved images and dvf will be written to the disk.\n             1: registration is performed correctly\n             2: skip overwriting\n             3: the dvf is available from the previous experiment [4, 2, 1]. Then just upsample it.\n    '
    stage_list = setting['ImagePyramidSchedule']
    if setting['CNN_Mode']:
        lstm_mode = False
    else:
        lstm_mode = True
    dvf_error_address = su.address_generator(setting, 'dvf_error', current_experiment=setting['lstm_exp'], pair_info=pair_info, stage_list=stage_list, base_reg=setting['BaseReg'])
    if os.path.isfile(dvf_error_address):
        if (not overwrite):
            logging.debug((('overwrite=False, file ' + dvf_error_address) + ' already exists, skipping .....'))
            return 2
        else:
            logging.debug((('overwrite=True, file ' + dvf_error_address) + ' already exists, but overwriting .....'))
    im_dict = dict()
    im_info_fixed = pair_info[0]
    im_info_moving = pair_info[1]
    base_reg = copy.copy(setting['BaseReg'])
    network_lstm_design = setting['network_lstm_dict']['NetworkDesign']
    setting['stage'] = 1
    setting = su.load_network_setting(setting, network_name=network_lstm_design)
    if (im_info_fixed['data'] == 'DIR-Lab_COPD'):
        if (setting['ImPad_S1'] < 42):
            setting['ImPad_S1'] = 42
    if (im_info_fixed['data'] == 'DIR-Lab_4D'):
        if (setting['ImPad_S1'] < 40):
            setting['ImPad_S1'] = 40
    setting['ImPad_S2'] = (setting['ImPad_S1'] + 7)
    setting['ImPad_S4'] = (setting['ImPad_S1'] + 10)
    base_key_list = ['fixed_im_s', 'fixed_mask_s', 'moved_im_s', 'moved_mask_s']
    for (i_stage, stage) in enumerate(stage_list):
        mask_to_zero_stage = setting['network_dict'][('stage' + str(stage))]['MaskToZero']
        fixed_im_stage_address = su.address_generator(setting, 'Im', stage=stage, **im_info_fixed)
        fixed_mask_stage_address = su.address_generator(setting, mask_to_zero_stage, stage=stage, **im_info_fixed)
        im_dict[('fixed_im_s' + str(stage))] = sitk.GetArrayFromImage(sitk.ReadImage(fixed_im_stage_address))
        im_dict[('fixed_mask_s' + str(stage))] = sitk.GetArrayFromImage(sitk.ReadImage(fixed_mask_stage_address))
        if (i_stage == 0):
            check_downsampled_base_reg(setting, stage, base_reg=base_reg, pair_info=pair_info, mask_to_zero_stage=mask_to_zero_stage)
            moved_im_stage_address = su.address_generator(setting, 'MovedImBaseReg', pair_info=pair_info, stage=stage, base_reg=base_reg, **im_info_moving)
            moved_mask_stage_address = su.address_generator(setting, (('Moved' + mask_to_zero_stage) + 'BaseReg'), pair_info=pair_info, stage=stage, base_reg=base_reg, **im_info_moving)
        elif setting['UseRegisteredImages']:
            moved_im_stage_address = su.address_generator(setting, 'MovedIm', current_experiment=setting['exp_multi_reg'], pair_info=pair_info, stage=stage, stage_list=stage_list, base_reg=base_reg)
            moved_mask_stage_address = su.address_generator(setting, ('Moved' + mask_to_zero_stage), current_experiment=setting['exp_multi_reg'], pair_info=pair_info, stage=stage, stage_list=stage_list, base_reg=base_reg)
        else:
            check_downsampled_base_reg(setting, stage, base_reg=base_reg, pair_info=pair_info, mask_to_zero_stage=mask_to_zero_stage)
            moved_im_stage_address = su.address_generator(setting, 'MovedImBaseReg', pair_info=pair_info, stage=stage, base_reg=base_reg, **im_info_moving)
            moved_mask_stage_address = su.address_generator(setting, (('Moved' + mask_to_zero_stage) + 'BaseReg'), pair_info=pair_info, stage=stage, base_reg=base_reg, **im_info_moving)
        im_dict[('moved_im_s' + str(stage))] = sitk.GetArrayFromImage(sitk.ReadImage(moved_im_stage_address))
        im_dict[('moved_mask_s' + str(stage))] = sitk.GetArrayFromImage(sitk.ReadImage(moved_mask_stage_address))
        logging.info((fixed_im_stage_address + ' loaded'))
        logging.info((fixed_mask_stage_address + ' loaded'))
        logging.info((moved_im_stage_address + ' loaded'))
        logging.info((moved_mask_stage_address + ' loaded'))
        default_pixel = setting['data'][pair_info[0]['data']]['DefaultPixelValue']
        im_dict[('fixed_im_s' + str(stage))][(im_dict[('fixed_mask_s' + str(stage))] == 0)] = default_pixel
        im_dict[('moved_im_s' + str(stage))][(im_dict[('moved_mask_s' + str(stage))] == 0)] = default_pixel
        if (setting[('ImPad_S' + str(stage))] > 0):
            for base_key in base_key_list:
                im_dict[(base_key + str(stage))] = np.pad(im_dict[(base_key + str(stage))], setting[('ImPad_S' + str(stage))], 'constant', constant_values=(default_pixel,))
    indices_padded = copy.deepcopy(landmark_dict['FixedLandmarksIndex'])
    indices_padded = (indices_padded + setting['ImPad_S1'])
    batch_size = 15
    for i in range(3):
        landmark_dict[(('DVF_error_times' + str(i)) + '_logits')] = np.zeros(((np.shape(landmark_dict['FixedLandmarksIndex'])[0],) + (setting['NumberOfLabels'],)))
        landmark_dict[(('DVF_error_times' + str(i)) + '_label')] = np.zeros(np.shape(landmark_dict['FixedLandmarksIndex'])[0])
    multi_stage_network_design = load_network_multi_stage_from_predefined(setting['exp_multi_reg'])
    multi_stage_network_load = get_parameter_multi_stage_network(setting, multi_stage_network_design)
    multi_stage_network_address = dict()
    for stage in setting['ImagePyramidSchedule']:
        multi_stage_network_address[('stage' + str(stage))] = su.address_generator(setting, 'saved_model_with_step', current_experiment=multi_stage_network_load[('stage' + str(stage))]['NetworkLoad'], step=multi_stage_network_load[('stage' + str(stage))]['GlobalStepLoad'])
    tf.reset_default_graph()
    tf.set_random_seed(0)
    with tf.variable_scope('InputImages'):
        images_s1_tf = tf.placeholder(tf.float32, shape=[batch_size, ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), 2], name='Images_S1')
        images_s2_tf = tf.placeholder(tf.float32, shape=[batch_size, ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), 2], name='Images_S2')
        images_s4_tf = tf.placeholder(tf.float32, shape=[batch_size, ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), ((2 * setting['R']) + 1), 2], name='Images_S4')
    bn_training = tf.placeholder(tf.bool, name='bn_training')
    if lstm_mode:
        (out0_tf, out1_tf, out2_tf, state0_tf, state1_tf) = getattr(getattr(network, network_lstm_design), 'network')(images_s1_tf, images_s2_tf, images_s4_tf, bn_training, detailed_summary=False, use_keras=setting['use_keras'], num_of_classes=setting['NumberOfLabels'], multi_stage_network_address=multi_stage_network_address)
    else:
        out2_tf = getattr(getattr(network, network_lstm_design), 'network')(images_s1_tf, images_s2_tf, images_s4_tf, bn_training, detailed_summary=setting['DetailedNetworkSummary'], use_keras=setting['use_keras'], num_of_classes=setting['NumberOfLabels'], multi_stage_network_address=multi_stage_network_address)
        (out0_tf, out1_tf, state0_tf, state1_tf) = (None, None, None, None)
    sess = tf.Session()
    saver_loading = tf.train.Saver(tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES))
    saver_loading.restore(sess, su.address_generator(setting, 'saved_model_with_step', current_experiment=setting['network_lstm_dict']['NetworkLoad'], step=setting['network_lstm_dict']['GlobalStepLoad']))
    time_before_dvf = time.time()
    begin_landmark_i = 0
    end_landmark_i = 0
    fill_last_batch = 0
    while (end_landmark_i < np.shape(landmark_dict['DVF_error_times2_logits'])[0]):
        end_landmark_i = (begin_landmark_i + batch_size)
        if (end_landmark_i > np.shape(landmark_dict['DVF_error_times2_logits'])[0]):
            fill_last_batch = (end_landmark_i - np.shape(landmark_dict['DVF_error_times2_logits'])[0])
            end_landmark_i = np.shape(landmark_dict['DVF_error_times2_logits'])[0]
        logging.info('begin_landmark_i={}, end_landmark_i={}'.format(begin_landmark_i, end_landmark_i))
        batch_im = extract_batch_from_patch_seq(setting, im_dict, indices_padded[(begin_landmark_i:end_landmark_i, :)])
        if fill_last_batch:
            batch_im = fill_junk_to_batch_size(setting, batch_size, batch_im)
        out_np = [None for _ in range(3)]
        if lstm_mode:
            [out_np[0], out_np[1], out_np[2]] = sess.run([out0_tf, out1_tf, out2_tf], feed_dict={images_s1_tf: batch_im['stage1'], images_s2_tf: batch_im['stage2'], images_s4_tf: batch_im['stage4'], bn_training: 0})
        else:
            [out_np[2]] = sess.run([out2_tf], feed_dict={images_s1_tf: batch_im['stage1'], images_s2_tf: batch_im['stage2'], images_s4_tf: batch_im['stage4'], bn_training: 0})
        for i in range(3):
            if (lstm_mode or (i == 2)):
                out_np_center = out_np[i][(:, (setting['Ry'] + 1), (setting['Ry'] + 1), (setting['Ry'] + 1), :)]
                out_np_center_label = np.argmax(out_np_center[(:, setting[('Labels_time' + str(i))])], axis=1)
                landmark_dict[(('DVF_error_times' + str(i)) + '_label')][begin_landmark_i:end_landmark_i] = out_np_center_label[0:(batch_size - fill_last_batch)]
                landmark_dict[(('DVF_error_times' + str(i)) + '_logits')][(begin_landmark_i:end_landmark_i, :)] = out_np_center[(0:(batch_size - fill_last_batch), :)]
        begin_landmark_i += 15
    time_after_dvf = time.time()
    logging.debug((pair_info[0]['data'] + ', CN{}, ImType{} is done in {:.2f}s '.format(pair_info[0]['cn'], pair_info[0]['type_im'], (time_after_dvf - time_before_dvf))))
    landmark_dict['DVF_nonrigidGroundTruth_magnitude'] = np.sqrt((((landmark_dict['DVF_nonrigidGroundTruth'][(:, 0)] ** 2) + (landmark_dict['DVF_nonrigidGroundTruth'][(:, 1)] ** 2)) + (landmark_dict['DVF_nonrigidGroundTruth'][(:, 2)] ** 2)))
    result_landmarks_folder = su.address_generator(setting, 'result_landmarks_folder', stage_list=stage_list, current_experiment=setting['lstm_exp'])
    if (not os.path.isdir(result_landmarks_folder)):
        os.makedirs(result_landmarks_folder)
    pair_info_text = ((((((setting['BaseReg'] + '_') + pair_info[0]['data']) + '_CN{}_TypeIm{},'.format(pair_info[0]['cn'], pair_info[0]['type_im'])) + '  Moving:') + pair_info[1]['data']) + '_CN{}_TypeIm{}'.format(pair_info[1]['cn'], pair_info[1]['type_im']))
    return landmark_dict

import copy
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import dill
from scipy.stats import wilcoxon
import SimpleITK as sitk
import time
import xlsxwriter
import functions.setting.setting_utils as su
from .image import landmark_info


def table_box_plot(setting, landmarks, compare_list=None, fig_measure_list=None, plot_per_pair=False, fig_ext='.png', plot_folder=None, paper_table=None, naming_strategy=None, jacobian=False, multi_jac_exp_list=None):
    "\n    merge the landmarks from different cases\n    :param setting:\n    :param landmarks:\n    :param compare_list:\n    :param\n    :param plot_folder: one of the experiment to save all plots in that directory. The plot folder should consider also the stages\n    for example: my_experiment_S4_S2_S1. if None, the last experiment will be chosen as the plot folder\n    :param naming_strategy: None\n                            'Fancy'\n                            'Clean'\n    :param paper_table: 'SPREAD', 'DIR-Lab'\n    :return:\n    "
    if (multi_jac_exp_list is None):
        if (paper_table == 'SPREAD-Multi'):
            multi_jac_exp_list = ['2020_multistage_crop45_K_NoResp_SingleOnly_more_itr_S4_S2_S1', 'BSpline_S4_S2_S1']
            multi_jac_exp_list = []
        if (paper_table == 'DIR-Lab-Multi'):
            multi_jac_exp_list = ['2020_multistage_crop45_K_Resp_more_itr_S4_S2_S1']
    if (compare_list is None):
        compare_list = ['Affine', 'BSpline']
    if (fig_measure_list is None):
        fig_measure_list = ['TRE']
    landmarks_merged = dict()
    if (plot_folder is None):
        plot_key = list(landmarks.items())[(- 1)][0]
    else:
        plot_key = plot_folder
    split_plot_folder = plot_key.split('_S')
    stage_list = []
    plot_folder_key_pure = split_plot_folder[0]
    for split_str in split_plot_folder:
        if (len(split_str) == 1):
            stage_list.append(int(split_str))
    result_folder = su.address_generator(setting, 'result_detail_folder', current_experiment=plot_folder_key_pure, stage_list=stage_list, pair_info=landmarks[plot_key][0]['pair_info'])
    if (not os.path.isdir(result_folder)):
        os.makedirs(result_folder)
    xlsx_address = (result_folder + 'results.xlsx')
    workbook = xlsxwriter.Workbook(xlsx_address)
    worksheet = workbook.add_worksheet()
    line = 0
    header = {'exp': 0, 'TRE_Mean': 1, 'TRE_STD': 2, 'TRE_Median': 3, 'MAE0_Mean': 4, 'MAE0_STD': 5, 'MAE1_Mean': 6, 'MAE1_STD': 7, 'MAE2_Mean': 8, 'MAE2_STD': 9, 'Jac_FoldingPercentage': 10, 'Jac_STD': 11, 'Error0_Mean': 12, 'Error0_STD': 13, 'Error1_Mean': 14, 'Error1_STD': 15, 'Error2_Mean': 16, 'Error2_STD': 17}
    for key in header.keys():
        worksheet.write(line, header[key], key)
    num_exp = len(landmarks.keys())
    for (exp_i, exp) in enumerate(landmarks.keys()):
        landmarks_merged[exp] = {'TRE': np.empty([0]), 'Error': np.empty([0, 3]), 'CleanName': su.clean_exp_name(exp), 'FancyName': su.fancy_exp_name(exp), 'Jac_NumberOfNegativeJacVoxels': 0, 'Jac_MaskSize': 0, 'Jac_Var': 0, 'Jac_STD_List': [], 'Jac_FoldingPercentage_List': []}
        num_pair = len(landmarks[exp])
        for (pair_i, landmark_pair) in enumerate(landmarks[exp]):
            pair_info = landmark_pair['pair_info']
            pair_info_text = ((((((landmarks_merged[exp]['CleanName'] + '_Fixed_') + pair_info[0]['data']) + '_CN{}_TypeIm{},'.format(pair_info[0]['cn'], pair_info[0]['type_im'])) + '_Moving_') + pair_info[1]['data']) + '_CN{}_TypeIm{}'.format(pair_info[1]['cn'], pair_info[1]['type_im']))
            landmarks_merged[exp]['TRE'] = np.append(landmarks_merged[exp]['TRE'], landmark_pair['landmark_info']['TRE'])
            landmarks_merged[exp]['Error'] = np.vstack((landmarks_merged[exp]['Error'], landmark_pair['landmark_info']['Error']))
            if jacobian:
                if (paper_table is not None):
                    if (exp in multi_jac_exp_list):
                        landmarks_merged[exp]['Jac_NumberOfNegativeJacVoxels'] += landmark_pair['landmark_info']['Jac_NumberOfNegativeJacVoxels']
                        landmarks_merged[exp]['Jac_MaskSize'] += landmark_pair['landmark_info']['Jac_MaskSize']
                        landmarks_merged[exp]['Jac_Var'] += ((landmark_pair['landmark_info']['Jac_Var'] * 1) / len(landmarks[exp]))
                        landmarks_merged[exp]['Jac_STD_List'].append(np.sqrt(landmark_pair['landmark_info']['Jac_Var']))
                        landmarks_merged[exp]['Jac_FoldingPercentage_List'].append(((landmark_pair['landmark_info']['Jac_NumberOfNegativeJacVoxels'] / landmark_pair['landmark_info']['Jac_MaskSize']) * 100))
            measure = calculate_measure(landmark_pair['landmark_info'])
            measure['exp'] = pair_info_text
            if plot_per_pair:
                print_latex(measure)
            line = ((exp_i + (pair_i * (num_exp + 1))) + 1)
            for key in header.keys():
                if (key in measure.keys()):
                    worksheet.write(line, header[key], measure[key])
                    landmark_pair['landmark_info'][key] = measure[key]
        measure_merged = calculate_measure(landmarks_merged[exp])
        if (naming_strategy == 'Clean'):
            measure_merged['exp'] = su.clean_exp_name(exp)
        elif (naming_strategy == 'Fancy'):
            measure_merged['exp'] = su.fancy_exp_name(exp)
        else:
            measure_merged['exp'] = exp
        print_latex(measure_merged)
        line = ((exp_i + (num_pair * (num_exp + 1))) + 2)
        for key in header.keys():
            if (key in measure.keys()):
                if ((key in header.keys()) and (key in measure_merged.keys())):
                    worksheet.write(line, header[key], measure_merged[key])
    workbook.close()
    if (paper_table == 'SPREAD'):
        print_latex_spread(landmarks, landmarks_merged, plot_key)
    if (paper_table == 'DIR-Lab'):
        print_latex_dir_lab_4d(landmarks, landmarks_merged, plot_key)
    if (paper_table == 'SPREAD-Multi'):
        print_latex_spread_multiple(landmarks, landmarks_merged, multi_jac_exp_list)
    if (paper_table == 'DIR-Lab-Multi'):
        print_latex_dir_lab_4d_multiple(landmarks, landmarks_merged, multi_jac_exp_list)
    for measure in fig_measure_list:
        if plot_per_pair:
            for pair_i in range(len(landmarks[next(iter(landmarks))])):
                (fig, ax) = plt.subplots(figsize=(15, 8))
                bplot1 = plt.boxplot([landmarks[exp][pair_i]['landmark_info'][measure] for exp in landmarks.keys()], patch_artist=True, notch=True)
                title_name = landmarks[next(iter(landmarks))][pair_i]['landmark_info']['exp']
                plt.title(title_name)
                plt.draw()
                plt.savefig(((((result_folder + measure) + '_') + title_name) + fig_ext))
                plt.close()
        (fig, ax) = plt.subplots(figsize=(15, 8))
        bplot1 = plt.boxplot([landmarks_merged[exp][measure] for exp in landmarks_merged.keys()], patch_artist=True, notch=True)
        title_name = (measure + '_Merged')
        plt.title(title_name)
        plt.savefig(((((result_folder + measure) + '_') + title_name) + fig_ext))
        plt.draw()
        plt.close()

import numpy as np
import matplotlib.pyplot as plt
import functions.color_constants as color_constants


def boxplot_tre(landmarks, exp_list, normalize=True, min1=20, max1=90, min2=20, max2=30, dash_line_exp=None, threshold=None, ylim=None):
    tre = dict()
    error = dict()
    fancy_name = dict()
    for exp in exp_list:
        tre[exp] = np.copy(landmarks[exp]['TRE'])
        error[exp] = np.copy(landmarks[exp]['Error'])
        fancy_name[exp] = landmarks[exp]['FancyName']
    if (threshold is None):
        ytick_value = [0, 5, 10, 15, min2, max2]
        ytick_label = ['0', '5', '10', '15', str(min1), str(max1)]
        title = 'TRE [mm] of all landmarks'
    else:
        affine_error = error['Affine']
        selected_landmarks = np.where(np.all((np.abs(affine_error) <= threshold), axis=1))
        for exp in exp_list:
            tre[exp] = tre[exp][selected_landmarks]
        ytick_value = [0, 5, 10, 15]
        ytick_label = [str(i) for i in ytick_value]
        while (ytick_value[(- 1)] < (threshold + 5)):
            ytick_value.append((ytick_value[(- 1)] + 5))
            ytick_label.append(str((ytick_value[(- 2)] + 5)))
        title = 'TRE [mm] of the capture range of {}'.format(threshold)
    if normalize:
        for exp in exp_list:
            ix = np.where((tre[exp] > min1))
            tre[exp][ix] = ((((tre[exp][ix] - min1) * (max2 - min1)) / (max1 - min2)) + min2)
    plt.rc('font', family='serif')
    (fig, ax) = plt.subplots(figsize=(15, 8))
    bplot1 = plt.boxplot([tre[exp] for exp in exp_list], patch_artist=True, notch=True)
    color_dict = color_constants.color_dict()
    color_keys = ['blue', 'springgreen', 'sapgreen', 'cyan2', 'peacock']
    color_list = [color_dict[color_key] for color_key in color_keys]
    for (i_patch, patch) in enumerate(bplot1['boxes']):
        if (i_patch == 0):
            color_i = 0
        elif (0 < i_patch < 3):
            color_i = 1
        elif (i_patch == 3):
            color_i = 2
        else:
            color_i = 3
        patch.set_facecolor(color_list[color_i])
    plt.xticks(np.arange(1, (len(exp_list) + 1)), [fancy_name[exp] for exp in exp_list], fontsize=16, rotation=90)
    plt.yticks(ytick_value, ytick_label, fontsize=24)
    if (dash_line_exp is not None):
        exp_i = np.where((np.array(exp_list) == dash_line_exp))
        plt.axhline(y=bplot1['boxes'][exp_i[0][0]]._path.vertices[(2, 1)], color='r', linestyle=':')
    if (ylim is not None):
        plt.ylim([0, ylim])
    plt.subplots_adjust(hspace=0, bottom=0.5)
    plt.title(title)
    plt.draw()

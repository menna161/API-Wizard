import numpy as np
import matplotlib.pyplot as plt
import functions.color_constants as color_constants


def table_tre(landmarks, exp_list, threshold=None):
    tre = dict()
    error = dict()
    fancy_name = dict()
    for exp in exp_list:
        tre[exp] = np.copy(landmarks[exp]['TRE'])
        error[exp] = np.copy(landmarks[exp]['Error'])
        fancy_name[exp] = landmarks[exp]['FancyName']
    tab = dict()
    latex_str = {}
    header_tab = ['exp', 'measure', 'measure_x', 'measure_y', 'measure_z']
    value_tab = np.empty([len(exp_list), 5], dtype=object)
    if (threshold is None):
        selected_landmarks = np.arange(len(landmarks[next(iter(landmarks))]['Error']))
    else:
        affine_error = error['Affine']
        selected_landmarks = np.where(np.all((np.abs(affine_error) <= threshold), axis=1))
        selected_landmarks = selected_landmarks[0]
    selected_landmarks = selected_landmarks.astype(np.int)
    for (i, exp) in enumerate(exp_list):
        tab[exp] = {}
        latex_str[exp] = (('&' + fancy_name[exp]) + ' &test ')
        tab[exp]['mean'] = np.mean(tre[exp][selected_landmarks])
        tab[exp]['std'] = np.std(tre[exp][selected_landmarks])
        value_tab[(i, 0)] = fancy_name[exp]
        value_tab[(i, 1)] = '${:.2f}\\pm{:.2f}$'.format(tab[exp]['mean'], tab[exp]['std'])
        latex_str[exp] += '&\\scriptsize${:.2f}\\pm{:.2f}$'.format(tab[exp]['mean'], tab[exp]['std'])
        for dim in range(3):
            tab[exp][('dim' + str(dim))] = {}
            tab[exp][('dim' + str(dim))]['mean'] = np.mean(np.abs([error[exp][k][dim] for k in selected_landmarks]))
            tab[exp][('dim' + str(dim))]['std'] = np.std(np.abs([error[exp][k][dim] for k in selected_landmarks]))
            value_tab[(i, (dim + 2))] = '${:.2f}\\pm{:.2f}$'.format(tab[exp][('dim' + str(dim))]['mean'], tab[exp][('dim' + str(dim))]['std'])
            latex_str[exp] += (' & ' + '\\scriptsize${:.2f}\\pm{:.2f}$'.format(tab[exp][('dim' + str(dim))]['mean'], tab[exp][('dim' + str(dim))]['std']))
        latex_str[exp] += '\\\\'
        print(latex_str[exp])
    plt.rc('font', family='serif')
    (fig, ax) = plt.subplots(figsize=(15, 8))
    fig.patch.set_visible(False)
    ax.table(cellText=value_tab, colLabels=header_tab, loc='center', colLoc='left', cellLoc='left', fontsize=50)
    ax.axis('off')
    ax.axis('tight')
    fig.tight_layout()
    if threshold:
        plt.title('TRE [mm] of the capture range of {}'.format(threshold))
    plt.draw()

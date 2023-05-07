import numpy as np
import matplotlib.pyplot as plt
import functions.color_constants as color_constants


def scatter_plot_dvf(landmarks, selected_exp, threshold=None, plt_limit=10):
    dvf = {selected_exp: np.copy(landmarks[selected_exp]['DVFRegNet']), 'GroundTruth': np.copy(landmarks['Affine']['GroundTruth'])}
    if (threshold is None):
        selected_landmarks = np.arange(len(landmarks['Affine']['Error']))
    else:
        affine_error = landmarks['Affine']['Error']
        selected_landmarks = np.where(np.all((np.abs(affine_error) <= threshold), axis=1))
        plt_limit = threshold
    for exp in dvf.keys():
        dvf[exp] = dvf[exp][selected_landmarks]
    plt.rc('font', family='serif')
    for dim in range(3):
        plt.figure(figsize=(6, 6))
        plt.scatter(dvf['GroundTruth'][(:, dim)], dvf[selected_exp][(:, dim)], color='green')
        plt.ylim((((- plt_limit) - 5), (plt_limit + 5)))
        plt.xlim((((- plt_limit) - 5), (plt_limit + 5)))
        plt.title(('Dimension' + str(dim)))
        plt.xlabel('Ground truth [mm]', fontsize=20)
        plt.ylabel((landmarks[selected_exp]['FancyName'] + ' [mm]'), fontsize=20)
        plt.plot([((- plt_limit) - 5), (plt_limit + 5)], [((- plt_limit) - 5), (plt_limit + 5)], color='blue', linewidth=2)
        plt.draw()

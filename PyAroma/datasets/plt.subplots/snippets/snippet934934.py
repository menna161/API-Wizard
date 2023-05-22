import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors


def plot(all_metrics, plot_param, out_file=None):
    data = {'x': [], 'y': [], 'size': [], 'color': []}
    for (experiment, metrics) in all_metrics.items():
        for key in data:
            data[key] += metrics[plot_param[key]['data']]
    for key in data:
        data[key] = np.array(data[key])
    nans = np.logical_or.reduce((np.isnan(data['x']), np.isnan(data['y']), np.isinf(data['x']), np.isinf(data['y'])))
    print(('\n ** Removing %d NaNs and infs before log **' % np.sum(nans)))
    for key in data:
        data[key] = data[key][np.invert(nans)]
    if (('plot_best_n_percent' in plot_param) and plot_param['plot_best_n_percent']):
        sorting_indices = np.argsort(data['x'])
        selected_indices = sorting_indices[:int(((plot_param['plot_best_n_percent'] / 100.0) * len(sorting_indices)))]
        for key in data:
            data[key] = data[key][selected_indices]
    data_x = ((np.log(data['x']) / np.log(10)) if plot_param['x']['log'] else np.copy(data['x']))
    data_y = ((np.log(data['y']) / np.log(10)) if plot_param['y']['log'] else np.copy(data['y']))
    nans = np.logical_or.reduce((np.isnan(data_x), np.isnan(data_y), np.isinf(data_x), np.isinf(data_y)))
    print(('\n ** Removing %d NaNs and infs after log **' % np.sum(nans)))
    for key in data:
        data[key] = data[key][np.invert(nans)]
    data_x = data_x[np.invert(nans)]
    data_y = data_y[np.invert(nans)]
    (fig, ax) = plt.subplots(figsize=(8, 8))
    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12
    plt.set_cmap('jet')
    plt.rc('font', size=16)
    plt.rc('axes', labelsize=20)
    (x_lim, y_lim) = compute_lims(data_x, data_y)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=8)
    x_label = plot_param['x']['data']
    y_label = plot_param['y']['data']
    if plot_param['x']['log']:
        x_label += ' (log)'
        ax.set_xticklabels([('%.3f' % np.power(10, float(t))) for t in ax.get_xticks()])
    if plot_param['y']['log']:
        y_label += ' (log)'
        ax.set_yticklabels([('%.2f' % np.power(10, float(t))) for t in ax.get_yticks()])
    else:
        ax.set_yticklabels([('%.2f' % float(t)) for t in ax.get_yticks()])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.scatter(data_x, data_y, s=data['size'], c=data['color'], alpha=0.5)
    corr = np.corrcoef(data_x, data_y)[(0, 1)]
    print(('Correlation %f' % corr))
    if ('title' in plot_param):
        title = plot_param['title']
    else:
        title = ((plot_param['y']['data'] + ' vs ') + plot_param['x']['data'])
    plt.title(('Correlation %.2f' % corr))
    if plot_param['print']:
        fig.savefig(out_file, bbox_inches='tight')

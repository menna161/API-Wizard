import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors


def plot_analysis(all_metrics, plot_param, out_file=None):
    if ('Regularization' in plot_param['title']):
        model_to_legend = {'25_nor_no_single_ctrl_bal_regr_all': 'No regularization', '25_nor_ndrop_single_ctrl_bal_regr_all': 'Dropout', '25_nor_saug_single_ctrl_bal_regr_all': 'Dropout + mild aug.', '25_nor_maug_single_ctrl_bal_regr_all': 'Dropout + heavy aug.'}
        model_to_id = {'25_nor_no_single_ctrl_bal_regr_all': 1, '25_nor_ndrop_single_ctrl_bal_regr_all': 2, '25_nor_saug_single_ctrl_bal_regr_all': 3, '25_nor_maug_single_ctrl_bal_regr_all': 4}
    elif ('Data distribution' in plot_param['title']):
        model_to_legend = {'25_nor_ndrop_single_ctrl_bal_regr_all': 'Three cameras with noise', '25_nor_ndrop_single_ctrl_bal_regr_jcen': 'Central camera with noise', '25_nor_ndrop_single_ctrl_bal_regr_nnjc': 'Central camera, no noise', '25_nor_ndrop_single_ctrl_seq_regr_all': 'Three cameras with noise, no balancing'}
        model_to_id = {'25_nor_ndrop_single_ctrl_bal_regr_nnjc': 1, '25_nor_ndrop_single_ctrl_bal_regr_jcen': 2, '25_nor_ndrop_single_ctrl_bal_regr_all': 3, '25_nor_ndrop_single_ctrl_seq_regr_all': 4}
    elif ('Model architecture' in plot_param['title']):
        model_to_legend = {'25_small_ndrop_single_ctrl_bal_regr_all': 'Shallow CNN', '25_nor_ndrop_single_ctrl_bal_regr_all': 'Standard CNN', '25_deep_ndrop_single_ctrl_bal_regr_all': 'Deep CNN', '25_nor_ndrop_lstm_ctrl_bal_regr_all': 'Standard LSTM'}
        model_to_id = {'25_small_ndrop_single_ctrl_bal_regr_all': 1, '25_nor_ndrop_single_ctrl_bal_regr_all': 2, '25_deep_ndrop_single_ctrl_bal_regr_all': 3, '25_nor_ndrop_lstm_ctrl_bal_regr_all': 4}
    else:
        model_to_legend = {'1_nor_maug_single_ctrl_bal_regr_all': '1 hour', '5_nor_maug_single_ctrl_bal_regr_all': '5 hours', '25_nor_maug_single_ctrl_bal_regr_all': '25 hours', '80_nor_maug_single_ctrl_bal_regr_all': '80 hours'}
        model_to_id = {'1_nor_maug_single_ctrl_bal_regr_all': 1, '5_nor_maug_single_ctrl_bal_regr_all': 2, '25_nor_maug_single_ctrl_bal_regr_all': 3, '80_nor_maug_single_ctrl_bal_regr_all': 4}
    town_to_legend = {'Town01_1': 'Town 1', 'Town02_14': 'Town 2'}
    town_to_id = {'Town01_1': 1, 'Town02_14': 2}

    def exp_to_legend_and_idx(exp):
        legend = exp
        idx = []
        for model in model_to_legend:
            if exp.startswith(model):
                legend = legend.replace(model, model_to_legend[model])
                idx.append(model_to_id[model])
                break
        for town in town_to_legend:
            if exp.endswith(town):
                legend = legend.replace(town, town_to_legend[town])
                idx.append(town_to_id[town])
                break
        legend = legend.replace('_', ', ')
        return (legend, idx)
    (fig, ax) = plt.subplots(figsize=(8, 8))
    plt.set_cmap('jet')
    cm = plt.get_cmap()
    c_norm = colors.Normalize(vmin=0, vmax=50)
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=cm)
    plt.rc('font', size=16)
    plt.rc('axes', titlesize=16)
    plt.rc('axes', labelsize=20)
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('legend', fontsize=14)
    plt.rc('figure', titlesize=16)
    print((np.log(plot_param['x_lim']) if plot_param['x']['log'] else plot_param['x_lim']))
    ax.set_xlim(((np.log(plot_param['x_lim']) / np.log(10.0)) if plot_param['x']['log'] else plot_param['x_lim']))
    ax.set_ylim(((np.log(plot_param['y_lim']) / np.log(10.0)) if plot_param['y']['log'] else plot_param['y_lim']))
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=8)
    x_label = 'Steering error'
    y_label = 'Success rate'
    if plot_param['x']['log']:
        x_label += ' (log)'
        ax.set_xticklabels([('%.1e' % np.power(10, float(t))) for t in ax.get_xticks()])
    if plot_param['y']['log']:
        y_label += ' (log)'
        ax.set_yticklabels([('%.1e' % np.power(10, float(t))) for t in ax.get_yticks()])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    scatter_handles = {}
    for (experiment, metrics) in all_metrics.items():
        print(experiment)
        data = {'x': [], 'y': [], 'size': [], 'color': []}
        for key in data:
            data[key] = np.array(metrics[plot_param[key]['data']])
        nans = np.logical_or.reduce((np.isnan(data['x']), np.isnan(data['y']), np.isinf(data['x']), np.isinf(data['y'])))
        print(('\n ** Removing %d NaNs and infs before log **' % np.sum(nans)))
        for key in data:
            data[key] = data[key][np.invert(nans)]
        data_x = ((np.log(data['x']) / np.log(10)) if plot_param['x']['log'] else np.copy(data['x']))
        data_y = ((np.log(data['y']) / np.log(10)) if plot_param['y']['log'] else np.copy(data['y']))
        nans = np.logical_or.reduce((np.isnan(data_x), np.isnan(data_y), np.isinf(data_x), np.isinf(data_y)))
        print(('\n ** Removing %d NaNs and infs after log **' % np.sum(nans)))
        for key in data:
            data[key] = data[key][np.invert(nans)]
        data_x = data_x[np.invert(nans)]
        data_y = data_y[np.invert(nans)]
        color_val = scalar_map.to_rgba((hash(experiment) % 50))
        color_vec = ([color_val] * len(data_x))
        scatter_handles[experiment] = ax.scatter(data_x, data_y, s=data['size'], c=color_vec, alpha=0.5)
        ax.plot(data_x, data_y, color=color_val)
    sorted_keys = sorted(scatter_handles.keys(), key=(lambda x: exp_to_legend_and_idx(x)[1]))
    ax.legend([scatter_handles[k] for k in sorted_keys], [exp_to_legend_and_idx(k)[0] for k in sorted_keys])
    plt.title(plot_param['title'])
    if plot_param['print']:
        fig.savefig(out_file, bbox_inches='tight')

import numpy as np
import matplotlib
from matplotlib import pyplot as plt, tri as tri
from matplotlib.ticker import LogLocator, MaxNLocator
from skopt import plots as skopt_plots
import plotly.plotly as plotlypy
import plotly.tools as tls
from utils import check_parameter_count_for_sample, partial_dependence_valid_samples_allow_paramcounts


def plot_flat_objective(result, param_thr, hyper_param_names, par_cnt_scheme='enc_dec_cnn_lstm_ff', levels=10, n_points=20, n_samples=250, size=2, zscale='linear', selected_dimensions=None, dimensions=None):
    "\n\tCopied from skopt and altered\n\tPairwise partial dependence plot of the objective function.\n\n\tThe diagonal shows the partial dependence for dimension `i` with\n\trespect to the objective function. The off-diagonal shows the\n\tpartial dependence for dimensions `i` and `j` with\n\trespect to the objective function. The objective function is\n\tapproximated by `result.model.`\n\n\tPairwise scatter plots of the points at which the objective\n\tfunction was directly evaluated are shown on the off-diagonal.\n\tA red point indicates the found minimum.\n\n\tNote: search spaces that contain `Categorical` dimensions are currently not supported by this function.\n\n\tParameters\n\t----------\n\t* `result` [`OptimizeResult`]\n\t\tThe result for which to create the scatter plot matrix.\n\n\t* `param_thr` [int]\n\t\tthreshold on trainable parameter count\n\n\t* `hyper_param_names`\n\t\tNames of the hyper parameters\n\n\t* `par_cnt_scheme` [default='enc_dec_cnn_lstm_ff']\n\t\tThe scheme to use to count the trainable parameters, to check if a sample is valid.\n\n\t* `levels` [int, default=10]\n\t\tNumber of levels to draw on the contour plot, passed directly\n\t\tto `plt.contour()`.\n\n\t* `n_points` [int, default=20]\n\t\tNumber of points at which to evaluate the partial dependence\n\t\talong each dimension.\n\n\t* `n_samples` [int, default=250]\n\t\tNumber of random samples to use for averaging the model function\n\t\tat each of the `n_points`.\n\n\t* `size` [float, default=2]\n\t\tHeight (in inches) of each facet.\n\n\t* `zscale` [str, default='linear']\n\t\tScale to use for the z axis of the contour plots. Either 'linear'\n\t\tor 'log'..\n\n\t* `selected_dimensions` [list, default='None']\n\t\tDimensions chosen to plot. If 'None', plot all dimensions\n\n\t* `dimensions` [list of str, default=None] Labels of the dimension\n\t\tvariables. `None` defaults to `space.dimensions[i].name`, or\n\t\tif also `None` to `['X_0', 'X_1', ..]`.\n\n\tReturns\n\t-------\n\t* `ax`: [`Axes`]:\n\t\tThe matplotlib axes.\n\t"
    space = result.space
    exps = np.asarray(result.x_iters)
    (_, exps_par_dicts) = check_parameter_count_for_sample(exps, hyper_param_names, param_thr, par_cnt_scheme)
    (_, res_x_par_dict) = check_parameter_count_for_sample(result.x, hyper_param_names, param_thr, par_cnt_scheme)
    if (selected_dimensions is None):
        selected_dimensions = range(space.n_dims)
    n_dims = len(selected_dimensions)
    if (dimensions is not None):
        dimensions = [dimensions[ind] for ind in selected_dimensions]
    if (zscale == 'log'):
        locator = LogLocator()
    elif (zscale == 'linear'):
        locator = None
    else:
        raise ValueError(("Valid values for zscale are 'linear' and 'log', not '%s'." % zscale))
    (fig, ax) = plt.subplots(n_dims, n_dims, figsize=((size * n_dims), (size * n_dims)))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.1, wspace=0.1)
    for (i, dim_i) in enumerate(selected_dimensions):
        for (j, dim_j) in enumerate(selected_dimensions):
            if (i == j):
                (xi, yi, yi_std) = partial_dependence_valid_samples_allow_paramcounts(space, result.models[(- 1)], param_thr, hyper_param_names, dim_i, j=None, par_cnt_scheme=par_cnt_scheme, n_samples=n_samples, n_points=n_points)
                ax[(i, i)].plot(xi, yi)
                ax[(i, i)].plot(xi, (yi + yi_std), ':', color='C0')
                ax[(i, i)].plot(xi, (yi - yi_std), ':', color='C0')
                ax[(i, i)].axvline(result.x[dim_i], linestyle='--', color='r', lw=1)
            elif (i > j):
                x = exps[(:, dim_j)]
                x = [float(xi) for xi in x]
                y = exps[(:, dim_i)]
                y = [float(yi) for yi in y]
                z = result.func_vals
                x_range = (max(x) - min(x))
                y_range = (max(y) - min(y))
                xi = np.linspace((min(x) - (x_range / 10)), (max(x) + (x_range / 10)), 1000)
                yi = np.linspace((min(y) - (y_range / 10)), (max(y) + (y_range / 10)), 1000)
                triang = tri.Triangulation(x, y)
                interpolator = tri.LinearTriInterpolator(triang, z)
                (Xi, Yi) = np.meshgrid(xi, yi)
                zi = interpolator(Xi, Yi)
                cntr1 = ax[(i, j)].contourf(xi, yi, zi, levels, locator=locator, cmap='viridis_r')
                fig.colorbar(cntr1, ax=ax[(i, j)])
                if isinstance(dim_j, str):
                    x_param_cnt = True
                    exps_xi = [exp_par_dict[dim_j] for exp_par_dict in exps_par_dicts]
                    res_xi = res_x_par_dict[dim_j]
                else:
                    x_param_cnt = False
                    exps_xi = exps[(:, dim_j)]
                    res_xi = result.x[dim_j]
                if isinstance(dim_i, str):
                    y_param_cnt = True
                    exps_yi = [exp_par_dict[dim_i] for exp_par_dict in exps_par_dicts]
                    res_yi = res_x_par_dict[dim_i]
                else:
                    y_param_cnt = False
                    exps_yi = exps[(:, dim_i)]
                    res_yi = result.x[dim_i]
                ax[(i, j)].scatter(exps_xi, exps_yi, c='k', s=10, lw=0.0)
                ax[(i, j)].scatter(res_xi, res_yi, c=['r'], s=20, lw=0.0)
    return _format_scatter_plot_axes(ax, space, ylabel='Partial dependence', selected_dimensions=selected_dimensions, dim_labels=dimensions)

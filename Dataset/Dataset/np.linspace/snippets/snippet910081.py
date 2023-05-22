import os
import functools
import collections
import six
import packaging
import packaging.version
import numpy as np
import scipy
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sklearn
import FlowCal.plot
import FlowCal.transform
import FlowCal.stats
from sklearn.mixture import GaussianMixture
from sklearn.mixture import GMM


def get_transform_fxn(data_beads, mef_values, mef_channels, clustering_fxn=clustering_gmm, clustering_params={}, clustering_channels=None, statistic_fxn=FlowCal.stats.median, statistic_params={}, selection_fxn=selection_std, selection_params={}, fitting_fxn=fit_beads_autofluorescence, fitting_params={}, verbose=False, plot=False, plot_dir=None, plot_filename=None, full_output=False):
    '\n    Get a transformation function to convert flow cytometry data to MEF.\n\n    Parameters\n    ----------\n    data_beads : FCSData object\n        Flow cytometry data describing calibration beads.\n    mef_values : sequence of sequences\n        Known MEF values for the calibration bead subpopulations, for each\n        channel specified in `mef_channels`. The innermost sequences must\n        have the same length (the same number of bead subpopulations must\n        exist for each channel). Values of np.nan or None specify that a\n        subpopulation should be omitted from the fitting procedure.\n    mef_channels : int, or str, or list of int, or list of str\n        Channels for which to generate transformation functions.\n    verbose : bool, optional\n        Flag specifying whether to print information about step completion\n        and warnings.\n    plot : bool, optional\n        Flag specifying whether to produce diagnostic plots.\n    plot_dir : str, optional\n        Directory where to save diagnostics plots. Ignored if `plot` is\n        False. If ``plot==True`` and ``plot_dir is None``, plot without\n        saving.\n    plot_filename : str, optional\n        Name to use for plot files. If None, use ``str(data_beads)``.\n    full_output : bool, optional\n        Flag specifying whether to include intermediate results in the\n        output. If `full_output` is True, the function returns a\n        `MEFOutput` ``namedtuple`` with fields as described below. If\n        `full_output` is False, the function only returns the calculated\n        transformation function.\n\n    Returns\n    -------\n    transform_fxn : function\n        Transformation function to convert flow cytometry data from RFI\n        units to MEF. This function has the following signature::\n\n            data_mef = transform_fxn(data_rfi, channels)\n\n    mef_channels : int, or str, or list, only if ``full_output==True``\n        Channels on which the transformation function has been generated.\n        Directly copied from the `mef_channels` argument.\n\n    clustering : dict, only if ``full_output==True``\n        Results of the clustering step. The structure of this dictionary\n        is::\n\n            clustering = {"labels": np.array}\n\n        A description of each ``"key": value`` is given below.\n\n        "labels" : array\n            Array of length ``N``, where ``N`` is the number of events in\n            `data_beads`. This array contains labels indicating which\n            subpopulation each event has been assigned to by the clustering\n            algorithm. Labels range from ``0`` to ``M - 1``, where ``M`` is\n            the number of MEF values specified, and therefore the number of\n            subpopulations identified by the clustering algorithm.\n\n    statistic : dict, only if ``full_output==True``\n        Results of the calculation of bead subpopulations\' fluorescence.\n        The structure of this dictionary is::\n\n            statistic = {"values": [np.array, ...]}\n\n        A description of each ``"key": value`` is given below.\n\n        "values" : list of arrays\n            Each array contains the representative fluorescence values of\n            all subpopulations, for a specific fluorescence channel from\n            `mef_channels`. Therefore, each array has a length equal to the\n            number of subpopulations, and the outer list has as many arrays\n            as the number of channels in `mef_channels`.\n\n    selection : dict, only if ``full_output==True``\n        Results of the subpopulation selection step. The structure of this\n        dictionary is::\n\n            selection = {"rfi": [np.array, ...],\n                         "mef": [np.array, ...]}\n\n        A description of each ``"key": value`` is given below.\n\n        "rfi" : list of arrays\n            Each array contains the fluorescence values of each selected\n            subpopulation in RFI units, for a specific fluorescence channel\n            from `mef_channels`. The outer list has as many arrays as the\n            number of channels in `mef_channels`. Because the selection\n            step may discard subpopulations, each array has a length less\n            than or equal to the total number of subpopulations.\n            Furthermore, different arrays in this list may not have the\n            same length. However, the length of each array is consistent\n            with the corresponding array in ``selection["mef"]`` (see\n            below).\n        "mef" : list of arrays\n            Each array contains the fluorescence values of each selected\n            subpopulation in MEF units, for a specific fluorescence channel\n            from `mef_channels`. The outer list has as many arrays as the\n            number of channels in `mef_channels`. Because the selection\n            step may discard subpopulations, each array has a length less\n            than or equal to the total number of subpopulations.\n            Furthermore, different arrays in this list may not have the\n            same length. However, the length of each array is consistent\n            with the corresponding array in ``selection["rfi"]`` (see\n            above).\n\n    fitting : dict, only if ``full_output==True``\n        Results of the model fitting step. The structure of this dictionary\n        is::\n\n            selection = {"std_crv": [func, ...],\n                         "beads_model": [func, ...],\n                         "beads_params": [np.array, ...],\n                         "beads_model_str": [str, ...],\n                         "beads_params_names": [[], ...]}\n\n        A description of each ``"key": value`` is given below.\n\n        "std_crv" : list of functions\n            Functions encoding the fitted standard curves, for each channel\n            in `mef_channels`. Each element of this list is the ``std_crv``\n            output of the fitting function (see required signature of the\n            ``fitting_fxn`` optional parameter), after applying it to the\n            MEF and RFI fluorescence values of a specific channel from\n            `mef_channels` .\n        "beads_model" : list of functions\n            Functions encoding the fluorescence model of the calibration\n            beads, for each channel in `mef_channels`. Each element of this\n            list is the ``beads_model`` output of the fitting function (see\n            required signature of the ``fitting_fxn`` optional parameter),\n            after applying it to the MEF and RFI fluorescence values of a\n            specific channel from `mef_channels` .\n        "beads_params" : list of arrays\n            Fitted parameter values of the bead fluorescence model, for\n            each channel in `mef_chanels`. Each element of this list is the\n            ``beads_params`` output of the fitting function (see required\n            signature of the ``fitting_fxn`` optional parameter), after\n            applying it to the MEF and RFI fluorescence values of a\n            specific channel from `mef_channels`.\n        "beads_model_str" : list of str\n            String representation of the bead models used, for each channel\n            in `mef_channels`. Each element of this list is the\n            ``beads_model_str`` output of the fitting function (see\n            required signature of the ``fitting_fxn`` optional parameter),\n            after applying it to the MEF and RFI fluorescence values of a\n            specific channel from `mef_channels` .\n        "beads_params_names" : list of list\n            Names of the parameters given in `beads_params`, for each\n            channel in `mef_channels`. Each element of this list is the\n            ``beads_params_names`` output of the fitting function (see\n            required signature of the ``fitting_fxn`` optional parameter),\n            after applying it to the MEF and RFI fluorescence values of a\n            specific channel from `mef_channels` .\n\n    Other parameters\n    ----------------\n    clustering_fxn : function, optional\n        Function used for clustering, or identification of subpopulations.\n        Must have the following signature::\n\n            labels = clustering_fxn(data, n_clusters, **clustering_params)\n\n        where `data` is a NxD FCSData object or numpy array, `n_clusters`\n        is the expected number of bead subpopulations, and `labels` is a 1D\n        numpy array of length N, assigning each event in `data` to one\n        subpopulation.\n\n    clustering_params : dict, optional\n        Additional keyword parameters to pass to `clustering_fxn`.\n\n    clustering_channels : list, optional\n        Channels used for clustering. If not specified, use `mef_channels`.\n        If more than three channels are specified and `plot` is True, only\n        a 3D scatter plot will be produced using the first three channels.\n\n    statistic_fxn : function, optional\n        Function used to calculate the representative fluorescence of each\n        subpopulation. Must have the following signature::\n\n            s = statistic_fxn(data, **statistic_params)\n\n        where `data` is a 1D FCSData object or numpy array, and `s` is a\n        float. Statistical functions from numpy, scipy, or FlowCal.stats\n        are valid options.\n\n    statistic_params : dict, optional\n        Additional keyword parameters to pass to `statistic_fxn`.\n\n    selection_fxn : function, optional\n        Function to use for bead population selection. Must have the\n        following signature::\n\n            selected_mask = selection_fxn(data_list, **selection_params)\n\n        where `data_list` is a list of FCSData objects, each one containing\n        the events of one population, and `selected_mask` is a boolean\n        array indicating whether the population has been selected (True) or\n        discarded (False). If None, don\'t use a population selection\n        procedure.\n\n    selection_params : dict, optional\n        Additional keyword parameters to pass to `selection_fxn`.\n\n    fitting_fxn : function, optional\n        Function used to fit the beads fluorescence model and obtain a\n        standard curve. Must have the following signature::\n\n            std_crv, beads_model, beads_params, \\\n            beads_model_str, beads_params_names = fitting_fxn(\n                fl_rfi, fl_mef, **fitting_params)\n\n        where `std_crv` is a function implementing the standard curve,\n        `beads_model` is a function implementing the beads fluorescence\n        model, `beads_params` is an array containing the fitted parameters\n        of the beads model, `beads_model_str` is a string representation\n        of the beads model used, `beads_params_names` is a list with the\n        parameter names in the same order as they are given in\n        `beads_params`, and `fl_rfi` and `fl_mef` are the fluorescence\n        values of the beads in RFI units and MEF units, respectively.\n        Note that the standard curve and the fitted beads model are not\n        necessarily the same.\n\n    fitting_params : dict, optional\n        Additional keyword parameters to pass to `fitting_fxn`.\n\n    Notes\n    -----\n    The steps involved in generating the MEF transformation function are:\n\n    1. The individual subpopulations of beads are first identified using a\n       clustering method of choice. Clustering is performed in all\n       specified channels simultaneously.\n    2. The fluorescence of each subpopulation is calculated, for each\n       channel in `mef_channels`.\n    3. Some subpopulations are then discarded if they are close to either\n       the minimum or the maximum channel range limits. In addition, if the\n       MEF value of some subpopulation is unknown (represented as a\n       ``np.nan`` in `mef_values`), the whole subpopulation is also\n       discarded.\n    4. The measured fluorescence of each subpopulation is compared with\n       the known MEF values in `mef_values`, and a standard curve function\n       is generated using the appropriate MEF model.\n\n    At the end, a transformation function is generated using the calculated\n    standard curves, `mef_channels`, and ``FlowCal.transform.to_mef()``.\n\n    Note that applying the resulting transformation function to other\n    flow cytometry samples only yields correct results if they have been\n    taken at the same settings as the calibration beads, for all channels\n    in `mef_channels`.\n\n    Examples\n    --------\n    Here is a simple application of this function:\n\n    >>> transform_fxn = FlowCal.mef.get_transform_fxn(\n    ...     beads_data,\n    ...     mef_channels=[\'FL1\', \'FL3\'],\n    ...     mef_values=[np.array([    0,   646,   1704,   4827,\n    ...                           15991, 47609, 135896, 273006],\n    ...                 np.array([    0,  1614,   4035,   12025,\n    ...                           31896, 95682, 353225, 1077421]],\n    ...     )\n    >>> sample_mef = transform_fxn(data=sample_rfi,\n    ...                            channels=[\'FL1\', \'FL3\'])\n\n    Here, we first generate ``transform_fxn`` from flow cytometry data\n    contained in ``FCSData`` object ``beads_data``, for channels FL1 and\n    FL3, using provided MEF values for each one of these channels. In the\n    next line, we use the resulting transformation function to transform\n    cell sample data in RFI to MEF.\n\n    More data about intermediate steps can be obtained with the option\n    ``full_output=True``:\n\n    >>> get_transform_output = FlowCal.mef.get_transform_fxn(\n    ...     beads_data,\n    ...     mef_channels=[\'FL1\', \'FL3\'],\n    ...     mef_values=[np.array([    0,   646,   1704,   4827,\n    ...                           15991, 47609, 135896, 273006],\n    ...                 np.array([    0,  1614,   4035,   12025,\n    ...                           31896, 95682, 353225, 1077421]],\n    ...     full_output=True)\n\n    In this case, the output ``get_transform_output`` will be a\n    `MEFOutput` ``namedtuple`` similar to the following::\n\n        FlowCal.mef.MEFOutput(\n            transform_fxn=<functools.partial object>,\n            mef_channels=[\'FL1\', \'FL3\'],\n            clustering={\n                \'labels\' : [7, 2, 2, ... 4, 3, 5]\n            },\n            statistic={\n                \'values\' : [np.array([ 101,  150,  231,  433,\n                                      1241, 3106, 7774, 9306]),\n                            np.array([   3,   30,   71,  204,\n                                       704, 2054, 6732, 9912])]\n            },\n            selection={\n                \'rfi\' : [np.array([  101,    150,    231,    433,\n                                    1241,   3106,   7774]),\n                         np.array([  30,      71,    204,    704,\n                                   2054,    6732])]\n                \'mef\' : [np.array([    0,    646,   1704,   4827,\n                                   15991,  47609, 135896]),\n                         np.array([ 1614,   4035,  12025,  31896,\n                                   95682, 353225])]\n            },\n            fitting={\n                \'std_crv\' : [<function <lambda>>,\n                             <function <lambda>>]\n                \'beads_model\' : [<function <lambda>>,\n                                 <function <lambda>>]\n                \'beads_params\' : [np.array([ 1.09e0, 2.02e0, 1.15e3]),\n                                  np.array([9.66e-1, 4.17e0, 6.63e1])]\n                \'beads_model_str\' : [\'m*log(fl_rfi) + b = log(fl_mef_auto + fl_mef)\',\n                                     \'m*log(fl_rfi) + b = log(fl_mef_auto + fl_mef)\']\n                \'beads_params_names\' : [[\'m\', \'b\', \'fl_mef_auto],\n                                        [\'m\', \'b\', \'fl_mef_auto]]\n            },\n        )\n\n    '
    if verbose:
        prev_precision = np.get_printoptions()['precision']
        np.set_printoptions(precision=2)
    if (plot and (plot_dir is not None)):
        if (not os.path.exists(plot_dir)):
            os.makedirs(plot_dir)
    if (plot_filename is None):
        plot_filename = str(data_beads)
    if (hasattr(mef_channels, '__iter__') and (not isinstance(mef_channels, six.string_types))):
        mef_channels = list(mef_channels)
    else:
        mef_channels = [mef_channels]
        mef_values = [mef_values]
    mef_values = np.array(mef_values, dtype=float)
    if (clustering_channels is None):
        clustering_channels = mef_channels
    n_clusters = len(mef_values[0])
    labels = clustering_fxn(data_beads[(:, clustering_channels)], n_clusters, **clustering_params)
    unique_labels = np.array(list(set(labels)))
    populations = [data_beads[(labels == i)] for i in unique_labels]
    population_dist = [np.sum((np.mean(population[(:, clustering_channels)], axis=0) ** 2)) for population in populations]
    population_sorted_idx = np.argsort(population_dist)
    populations = [populations[i] for i in population_sorted_idx]
    if verbose:
        population_count = np.array([population.shape[0] for population in populations])
        population_perc = ((population_count * 100.0) / population_count.sum())
        print('Step 1: Clustering')
        print('  Number of populations to find: {}'.format(n_clusters))
        print('  Percentage of events in each population:')
        print(('    ' + str(population_perc)))
    if plot:
        if (plot_dir is not None):
            savefig = '{}/clustering_{}.png'.format(plot_dir, plot_filename)
        else:
            savefig = None
        if (len(clustering_channels) == 1):
            plt.figure(figsize=(8, 4))
            FlowCal.plot.hist1d(populations, channel=clustering_channels[0], xscale='logicle', bins=256, alpha=0.75, savefig=savefig)
        elif (len(clustering_channels) == 2):
            plt.figure(figsize=(6, 4))
            FlowCal.plot.scatter2d(populations, channels=clustering_channels, xscale='logicle', yscale='logicle', savefig=savefig)
        elif (len(clustering_channels) >= 3):
            plt.figure(figsize=(8, 6))
            FlowCal.plot.scatter3d_and_projections(populations, channels=clustering_channels[:3], xscale='logicle', yscale='logicle', zscale='logicle', savefig=savefig)
        if (plot_dir is not None):
            plt.close()
    std_crv_res = []
    if full_output:
        stats_values_res = []
        selected_rfi_res = []
        selected_mef_res = []
        beads_model_res = []
        beads_params_res = []
        beads_model_str_res = []
        beads_params_names_res = []
    for (mef_channel, mef_values_channel) in zip(mef_channels, mef_values):
        populations_channel = [population[(:, mef_channel)] for population in populations]
        stats_values = [statistic_fxn(population, **statistic_params) for population in populations_channel]
        stats_values = np.array(stats_values)
        if full_output:
            stats_values_res.append(stats_values)
        if verbose:
            print('({}) Step 2: Population Statistic'.format(mef_channel))
            print('  Fluorescence of each population (RFI):')
            print(('    ' + str(stats_values)))
        if (selection_fxn is not None):
            selected_mask = selection_fxn([population for population in populations_channel], **selection_params)
        else:
            selected_mask = np.ones(n_clusters, dtype=bool)
        selected_mask = np.logical_and(selected_mask, (~ np.isnan(mef_values_channel)))
        selected_rfi = stats_values[selected_mask]
        selected_mef = mef_values_channel[selected_mask]
        if full_output:
            selected_rfi_res.append(selected_rfi)
            selected_mef_res.append(selected_mef)
        if verbose:
            print('({}) Step 3: Population Selection'.format(mef_channel))
            print('  {} populations selected.'.format(len(selected_rfi)))
            print('  Fluorescence of selected populations (RFI):')
            print(('    ' + str(selected_rfi)))
            print('  Fluorescence of selected populations (MEF):')
            print(('    ' + str(selected_mef)))
        if plot:
            color_levels = np.linspace(0, 1, n_clusters)
            colors = [(FlowCal.plot.cmap_default(level) if selected else (0.6, 0.6, 0.6)) for (selected, level) in zip(selected_mask, color_levels)]
            plt.figure(figsize=(8, 4))
            FlowCal.plot.hist1d(populations, channel=mef_channel, xscale='logicle', bins=256, alpha=0.75, facecolor=colors)
            ylim = plt.ylim()
            for (val, color) in zip(stats_values, colors):
                plt.plot([val, val], [ylim[0], ylim[1]], color=color)
            plt.ylim(ylim)
            if (plot_dir is not None):
                plt.tight_layout()
                plt.savefig('{}/populations_{}_{}.png'.format(plot_dir, mef_channel, plot_filename), dpi=FlowCal.plot.savefig_dpi)
                plt.close()
        fitting_output = fitting_fxn(selected_rfi, selected_mef, **fitting_params)
        std_crv = fitting_output[0]
        beads_model = fitting_output[1]
        beads_params = fitting_output[2]
        beads_model_str = fitting_output[3]
        beads_params_names = fitting_output[4]
        std_crv_res.append(std_crv)
        if full_output:
            beads_model_res.append(beads_model)
            beads_params_res.append(beads_params)
            beads_model_str_res.append(beads_model_str)
            beads_params_names_res.append(beads_params_names)
        if verbose:
            print('({}) Step 4: Standard Curve Fitting'.format(mef_channel))
            print('  Parameters of bead fluorescence model:')
            print(('    ' + str(beads_params)))
        if plot:
            xlim = populations[0].range(channels=mef_channel)
            if (xlim[0] <= 0):
                xlim[0] = min(1.0, (xlim[1] / 100000.0))
            plt.figure(figsize=(6, 4))
            plot_standard_curve(selected_rfi, selected_mef, beads_model, std_crv, xscale='log', yscale='log', xlim=xlim)
            plt.xlabel('{} (a.u.)'.format(mef_channel))
            plt.ylabel('{} (MEF)'.format(mef_channel))
            if (plot_dir is not None):
                plt.tight_layout()
                plt.savefig('{}/std_crv_{}_{}.png'.format(plot_dir, mef_channel, plot_filename), dpi=FlowCal.plot.savefig_dpi)
                plt.close()
    transform_fxn = functools.partial(FlowCal.transform.to_mef, sc_list=std_crv_res, sc_channels=mef_channels)
    if verbose:
        np.set_printoptions(precision=prev_precision)
    if full_output:
        clustering_res = {}
        clustering_res['labels'] = labels
        statistic_res = {}
        statistic_res['values'] = stats_values_res
        selection_res = {}
        selection_res['rfi'] = selected_rfi_res
        selection_res['mef'] = selected_mef_res
        fitting_res = {}
        fitting_res['std_crv'] = std_crv_res
        fitting_res['beads_model'] = beads_model_res
        fitting_res['beads_params'] = beads_params_res
        fitting_res['beads_model_str'] = beads_model_str_res
        fitting_res['beads_params_names'] = beads_params_names_res
        fields = ['mef_channels', 'transform_fxn', 'clustering', 'statistic', 'selection', 'fitting']
        MEFOutput = collections.namedtuple('MEFOutput', fields)
        out = MEFOutput(mef_channels=mef_channels, transform_fxn=transform_fxn, clustering=clustering_res, statistic=statistic_res, selection=selection_res, fitting=fitting_res)
        return out
    else:
        return transform_fxn

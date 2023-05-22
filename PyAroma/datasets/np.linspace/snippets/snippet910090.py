import packaging
import packaging.version
import collections
import numpy as np
import scipy.ndimage.filters
import matplotlib
import matplotlib.scale
import matplotlib.transforms
import matplotlib.ticker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
import warnings


def violin_dose_response(data, channel=None, positions=None, min_data=None, max_data=None, violin_width=None, model_fxn=None, xscale='linear', yscale='logicle', xlim=None, ylim=None, violin_width_to_span_fraction=0.1, num_bins=100, bin_edges=None, density=False, upper_trim_fraction=0.01, lower_trim_fraction=0.01, violin_kwargs=None, draw_summary_stat=True, draw_summary_stat_fxn=np.mean, draw_summary_stat_kwargs=None, log_zero_tick_label=None, min_bin_edges=None, min_upper_trim_fraction=0.01, min_lower_trim_fraction=0.01, min_violin_kwargs=None, min_draw_summary_stat_kwargs=None, draw_min_line=True, draw_min_line_kwargs=None, min_tick_label='Min', max_bin_edges=None, max_upper_trim_fraction=0.01, max_lower_trim_fraction=0.01, max_violin_kwargs=None, max_draw_summary_stat_kwargs=None, draw_max_line=True, draw_max_line_kwargs=None, max_tick_label='Max', draw_model_kwargs=None, draw_log_zero_divider=True, draw_log_zero_divider_kwargs=None, draw_minmax_divider=True, draw_minmax_divider_kwargs=None, xlabel=None, ylabel=None, title=None, savefig=None):
    '\n    Plot violin plot with min data, max data, and mathematical model.\n\n    Plot a violin plot (see ``FlowCal.plot.violin()`` description) with\n    vertical violins and separately illustrate a min violin, a max violin, and\n    a mathematical model. Useful for illustrating "dose response" or "transfer"\n    functions, which benefit from the added context of minimum and maximum\n    bounds and which are often described by mathematical models. Min and max\n    violins are illustrated to the left of the plot, and the mathematical\n    model is correctly illustrated even when a position=0 violin is\n    illustrated separately when `xscale` is ``log``.\n\n    Parameters\n    ----------\n    data : 1D or ND array or list of 1D or ND arrays\n        A population or collection of populations for which to plot violins.\n        If ND arrays are used (e.g., FCSData), `channel` must be specified.\n    channel : int or str, optional\n        Channel from `data` to plot. If specified, data are assumed to be ND\n        arrays. String channel specifications are only supported for data\n        types that support string-based indexing (e.g., FCSData).\n    positions : scalar or array, optional\n        Positions at which to center violins.\n    min_data : 1D or ND array, optional\n        A population representing a minimum control. This violin is separately\n        illustrated at the left of the plot.\n    max_data : 1D or ND array, optional\n        A population representing a maximum control. This violin is separately\n        illustrated at the left of the plot.\n    violin_width : scalar, optional\n        Width of violin. If `xscale` is ``log``, the units are decades. If not\n        specified, `violin_width` is calculated from `xlim` and\n        `violin_width_to_span_fraction`. If only one violin is specified in\n        `data`, `violin_width` = 0.5.\n    model_fxn : function, optional\n        Function used to calculate model y-values. 100 x-values are linearly\n        (if `xscale` is ``linear``) or logarithmically (if `xscale` is\n        ``log``) generated spanning `xlim`. If `xscale` is ``log`` and a\n        position=0 violin is specified, the result of ``model_fxn(0.0)`` is\n        illustrated as a horizontal line with the position=0 violin.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xscale : {\'linear\', \'log\'}, optional\n        Scale of the x-axis.\n    yscale : {\'logicle\', \'linear\', \'log\'}, optional\n        Scale of the y-axis.\n    xlim : tuple, optional\n        Limits of the x-axis view. If not specified, `xlim` is calculated to\n        pad leftmost and rightmost violins with 0.5 * `violin_width`. If\n        `violin_width` is also not specified, `violin_width` is calculated to\n        satisfy the 0.5 * `violin_width` padding and\n        `violin_width_to_span_fraction`.\n    ylim : tuple, optional\n        Limits of the y-axis view. If not specified, `ylim` is calculated to\n        span all violins (before they are aesthetically trimmed).\n    violin_width_to_span_fraction : float, optional\n        Fraction of the x-axis span that a violin should span. Ignored if\n        `violin_width` is specified.\n    num_bins : int, optional\n        Number of bins to bin population members. Ignored if `bin_edges` is\n        specified.\n    bin_edges : array or list of arrays, optional\n        Bin edges used to bin population members for `data` violins. Bin edges\n        can be specified for individual violins using a list of arrays of the\n        same length as `data`. If not specified, `bin_edges` is calculated to\n        span `ylim` logicly (if `yscale` is ``logicle``), linearly (if\n        `yscale` is ``linear``), or logarithmically (if `yscale` is ``log``)\n        using `num_bins`.\n    density : bool, optional\n        `density` parameter passed to the ``np.histogram()`` command that bins\n        population members for each violin. If True, violin width represents\n        relative frequency *density* instead of relative frequency (i.e., bins\n        are normalized by their width).\n    upper_trim_fraction : float or list of floats, optional\n        Fraction of members to trim (discard) from the top of the `data`\n        violins (e.g., for aesthetic purposes). Upper trim fractions can be\n        specified for individual violins using a list of floats of the same\n        length as `data`.\n    lower_trim_fraction : float or list of floats, optional\n        Fraction of members to trim (discard) from the bottom of the `data`\n        violins (e.g., for aesthetic purposes). Lower trim fractions can be\n        specified for individual violins using a list of floats of the same\n        length as `data`.\n    violin_kwargs : dict or list of dicts, optional\n        Keyword arguments passed to the ``plt.fill_betweenx()`` command that\n        illustrates the `data` violins. Keyword arguments can be specified for\n        individual violins using a list of dicts of the same length as `data`.\n        Default = {\'facecolor\':\'gray\', \'edgecolor\':\'black\'}.\n    draw_summary_stat : bool, optional\n        Flag specifying to illustrate a summary statistic for each violin.\n    draw_summary_stat_fxn : function, optional\n        Function used to calculate the summary statistic for each violin.\n        Summary statistics are calculated prior to aesthetic trimming.\n    draw_summary_stat_kwargs : dict or list of dicts, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the `data` violin summary statistics. Keyword arguments\n        can be specified for individual violins using a list of dicts of the\n        same length as `data`. Default = {\'color\':\'black\'}.\n    log_zero_tick_label : str, optional\n        Label of position=0 violin tick if `xscale` is ``log``. Default is\n        generated by the default log tick formatter\n        (``matplotlib.ticker.LogFormatterSciNotation``) with x=0.\n    min_bin_edges : array, optional\n        Bin edges used to bin population members for the min violin. If not\n        specified, `min_bin_edges` is calculated to span `ylim` logicaly (if\n        `yscale` is ``logicle``), linearly (if `yscale` is ``linear``), or\n        logarithmically (if `yscale` is ``log``) using `num_bins`.\n    min_upper_trim_fraction : float, optional\n        Fraction of members to trim (discard) from the top of the min violin.\n    min_lower_trim_fraction : float, optional\n        Fraction of members to trim (discard) from the bottom of the min\n        violin.\n    min_violin_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.fill_betweenx()`` command that\n        illustrates the min violin. Default = {\'facecolor\':\'black\',\n        \'edgecolor\':\'black\'}.\n    min_draw_summary_stat_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the min violin summary statistic. Default =\n        {\'color\':\'gray\'}.\n    draw_min_line : bool, optional\n        Flag specifying to illustrate a line from the min violin summary\n        statistic across the plot.\n    draw_min_line_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the min violin line. Default = {\'color\':\'gray\',\n        \'linestyle\':\'--\', \'zorder\':-2}.\n    min_tick_label : str, optional\n        Label of min violin tick. Default=\'Min\'.\n    max_bin_edges : array, optional\n        Bin edges used to bin population members for the max violin. If not\n        specified, `max_bin_edges` is calculated to span `ylim` logicaly (if\n        `yscale` is ``logicle``), linearly (if `yscale` is ``linear``), or\n        logarithmically (if `yscale` is ``log``) using `num_bins`.\n    max_upper_trim_fraction : float, optional\n        Fraction of members to trim (discard) from the top of the max violin.\n    max_lower_trim_fraction : float, optional\n        Fraction of members to trim (discard) from the bottom of the max\n        violin.\n    max_violin_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.fill_betweenx()`` command that\n        illustrates the max violin. Default = {\'facecolor\':\'black\',\n        \'edgecolor\':\'black\'}.\n    max_draw_summary_stat_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the max violin summary statistic. Default =\n        {\'color\':\'gray\'}.\n    draw_max_line : bool, optional\n        Flag specifying to illustrate a line from the max violin summary\n        statistic across the plot.\n    draw_max_line_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the max violin line. Default = {\'color\':\'gray\',\n        \'linestyle\':\'--\', \'zorder\':-2}.\n    max_tick_label : str, optional\n        Label of max violin tick. Default=\'Max\'.\n    draw_model_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the model. Default = {\'color\':\'gray\', \'zorder\':-1,\n        \'solid_capstyle\':\'butt\'}.\n    draw_log_zero_divider : bool, optional\n        Flag specifying to illustrate a line separating the position=0 violin\n        from the `data` violins if `xscale` is ``log``.\n    draw_log_zero_divider_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.axvline()`` command that\n        illustrates the position=0 violin divider. Default = {\'color\':\'gray\',\n        \'linestyle\':\':\'}.\n    draw_minmax_divider : bool, optional\n        Flag specifying to illustrate a vertical line separating the min and\n        max violins from other violins.\n    draw_minmax_divider_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.axvline()`` command that\n        illustrates the min/max divider. Default = {\'color\':\'gray\',\n        \'linestyle\':\'-\'}.\n    xlabel : str, optional\n        Label to use on the x-axis.\n    ylabel : str, optional\n        Label to use on the y-axis. If None, channel name will be used if\n        possible (extracted from the last data object).\n    title : str, optional\n        Plot title.\n\n    '
    if (violin_kwargs is None):
        violin_kwargs = {'facecolor': 'gray', 'edgecolor': 'black'}
    if (min_violin_kwargs is None):
        min_violin_kwargs = {'facecolor': 'black', 'edgecolor': 'black'}
    if (max_violin_kwargs is None):
        max_violin_kwargs = {'facecolor': 'black', 'edgecolor': 'black'}
    if (draw_summary_stat_kwargs is None):
        draw_summary_stat_kwargs = {'color': 'black'}
    if (min_draw_summary_stat_kwargs is None):
        min_draw_summary_stat_kwargs = {'color': 'gray'}
    if (max_draw_summary_stat_kwargs is None):
        max_draw_summary_stat_kwargs = {'color': 'gray'}
    if (draw_min_line_kwargs is None):
        draw_min_line_kwargs = {'color': 'gray', 'linestyle': '--', 'zorder': (- 2)}
    if (draw_max_line_kwargs is None):
        draw_max_line_kwargs = {'color': 'gray', 'linestyle': '--', 'zorder': (- 2)}
    if (draw_model_kwargs is None):
        draw_model_kwargs = {'color': 'gray', 'zorder': (- 1), 'solid_capstyle': 'butt'}
    if (draw_log_zero_divider_kwargs is None):
        draw_log_zero_divider_kwargs = {'color': 'gray', 'linestyle': ':'}
    if (draw_minmax_divider_kwargs is None):
        draw_minmax_divider_kwargs = {'color': 'gray', 'linestyle': '-'}
    if (xscale not in ('linear', 'log')):
        msg = "`xscale` must be 'linear' or 'log'"
        raise ValueError(msg)
    if (yscale not in ('logicle', 'linear', 'log')):
        msg = "`yscale` must be 'logicle', 'linear', or 'log'"
        raise ValueError(msg)
    if (channel is None):
        try:
            first_element = next(iter(data))
        except TypeError:
            msg = '`data` should be 1D array or list of 1D arrays.'
            msg += ' Specify `channel` to use ND array or list of ND'
            msg += ' arrays.'
            raise TypeError(msg)
        except StopIteration:
            data_length = 0
        else:
            try:
                iter(first_element)
                data_length = len(data)
            except TypeError:
                data = [data]
                data_length = 1
    else:
        try:
            first_element = next(iter(data))
        except TypeError:
            msg = '`data` should be ND array or list of ND arrays.'
            msg += ' Set `channel` to None to use 1D array or list of'
            msg += ' 1D arrays.'
            raise TypeError(msg)
        except StopIteration:
            data_length = 0
        else:
            try:
                first_element_first_element = next(iter(first_element))
            except TypeError:
                msg = '`data` should be ND array or list of ND arrays.'
                msg += ' Set `channel` to None to use 1D array or list of'
                msg += ' 1D arrays.'
                raise TypeError(msg)
            except StopIteration:
                data_length = len(data)
            else:
                try:
                    iter(first_element_first_element)
                    data_length = len(data)
                except TypeError:
                    data = [data]
                    data_length = 1
        try:
            data = [d[(:, channel)] for d in data]
        except TypeError:
            data = [[row[channel] for row in d] for d in data]
        if (min_data is not None):
            try:
                min_data = min_data[(:, channel)]
            except TypeError:
                min_data = [row[channel] for row in min_data]
        if (max_data is not None):
            try:
                max_data = max_data[(:, channel)]
            except TypeError:
                max_data = [row[channel] for row in max_data]
    if (positions is None):
        positions = np.arange(1, (data_length + 1), dtype=float)
        if (xscale == 'log'):
            positions = (10 ** positions)
        positions_length = len(positions)
    else:
        try:
            positions_length = len(positions)
        except TypeError:
            positions = [positions]
            positions_length = 1
    if (positions_length != data_length):
        msg = '`positions` must have the same length as `data`'
        raise ValueError(msg)
    all_data = list(data)
    if (min_data is not None):
        all_data.append(min_data)
    if (max_data is not None):
        all_data.append(max_data)
    if (ylim is None):
        ymin = np.inf
        ymax = (- np.inf)
        for idx in range(len(all_data)):
            violin_data = np.array(all_data[idx], dtype=float).flat
            if (len(violin_data) > 0):
                violin_min = np.min(violin_data)
                violin_max = np.max(violin_data)
                if (violin_min < ymin):
                    ymin = violin_min
                if (violin_max > ymax):
                    ymax = violin_max
        ylim = (ymin, ymax)
        if all(np.isinf(ylim)):
            ylim = (0.0, 1.0)
    if (bin_edges is None):
        if (yscale == 'logicle'):
            t = _LogicleTransform(data=all_data, channel=channel)
            t_ymin = t.inverted().transform_non_affine(x=ylim[0], mask_out_of_range=False)
            t_ymax = t.inverted().transform_non_affine(x=ylim[1], mask_out_of_range=False)
            t_bin_edges = np.linspace(t_ymin, t_ymax, (num_bins + 1))
            bin_edges = t.transform_non_affine(t_bin_edges)
        elif (yscale == 'linear'):
            bin_edges = np.linspace(ylim[0], ylim[1], (num_bins + 1))
        else:
            bin_edges = np.logspace(np.log10(ylim[0]), np.log10(ylim[1]), (num_bins + 1))
    if (min_bin_edges is None):
        if (yscale == 'logicle'):
            t = _LogicleTransform(data=all_data, channel=channel)
            t_ymin = t.inverted().transform_non_affine(x=ylim[0], mask_out_of_range=False)
            t_ymax = t.inverted().transform_non_affine(x=ylim[1], mask_out_of_range=False)
            t_min_bin_edges = np.linspace(t_ymin, t_ymax, (num_bins + 1))
            min_bin_edges = t.transform_non_affine(t_min_bin_edges)
        elif (yscale == 'linear'):
            min_bin_edges = np.linspace(ylim[0], ylim[1], (num_bins + 1))
        else:
            min_bin_edges = np.logspace(np.log10(ylim[0]), np.log10(ylim[1]), (num_bins + 1))
    if (max_bin_edges is None):
        if (yscale == 'logicle'):
            t = _LogicleTransform(data=all_data, channel=channel)
            t_ymin = t.inverted().transform_non_affine(x=ylim[0], mask_out_of_range=False)
            t_ymax = t.inverted().transform_non_affine(x=ylim[1], mask_out_of_range=False)
            t_max_bin_edges = np.linspace(t_ymin, t_ymax, (num_bins + 1))
            max_bin_edges = t.transform_non_affine(t_max_bin_edges)
        elif (yscale == 'linear'):
            max_bin_edges = np.linspace(ylim[0], ylim[1], (num_bins + 1))
        else:
            max_bin_edges = np.logspace(np.log10(ylim[0]), np.log10(ylim[1]), (num_bins + 1))
    log_zero_data = None
    log_zero_violin_kwargs = None
    log_zero_draw_summary_stat_kwargs = None
    log_zero_bin_edges = None
    log_zero_upper_trim_fraction = None
    log_zero_lower_trim_fraction = None
    if ((xscale == 'log') and (0 in list(positions))):
        data = list(data)
        positions = list(positions)
        zero_idx = [idx for (idx, pos) in enumerate(positions) if (pos == 0)]
        if (len(zero_idx) > 1):
            msg = 'attempting to separately illustrate position=0 violin,'
            msg += ' but found multiple instances'
            raise ValueError(msg)
        zero_idx = zero_idx[0]
        log_zero_data = data.pop(zero_idx)
        del positions[zero_idx]
        data_length = len(data)
        positions_length = len(positions)
        if isinstance(violin_kwargs, collectionsAbc.Sequence):
            violin_kwargs = list(violin_kwargs)
            log_zero_violin_kwargs = violin_kwargs.pop(zero_idx)
        else:
            log_zero_violin_kwargs = violin_kwargs
        if isinstance(draw_summary_stat_kwargs, collectionsAbc.Sequence):
            draw_summary_stat_kwargs = list(draw_summary_stat_kwargs)
            log_zero_draw_summary_stat_kwargs = draw_summary_stat_kwargs.pop(zero_idx)
        else:
            log_zero_draw_summary_stat_kwargs = draw_summary_stat_kwargs
        if (bin_edges is not None):
            try:
                first_element = next(iter(bin_edges))
                try:
                    iter(first_element)
                    bin_edges = list(bin_edges)
                    log_zero_bin_edges = bin_edges.pop(zero_idx)
                except TypeError:
                    log_zero_bin_edges = bin_edges
            except TypeError:
                msg = '`bin_edges` should be array or list of arrays'
                raise TypeError(msg)
        if isinstance(upper_trim_fraction, collectionsAbc.Sequence):
            upper_trim_fraction = list(upper_trim_fraction)
            log_zero_upper_trim_fraction = upper_trim_fraction.pop(zero_idx)
        else:
            log_zero_upper_trim_fraction = upper_trim_fraction
        if isinstance(lower_trim_fraction, collectionsAbc.Sequence):
            lower_trim_fraction = list(lower_trim_fraction)
            log_zero_lower_trim_fraction = lower_trim_fraction.pop(zero_idx)
        else:
            log_zero_lower_trim_fraction = lower_trim_fraction
    if (xlim is None):
        if (violin_width is None):
            if (data_length <= 1):
                violin_width = 0.5
            elif (xscale == 'log'):
                log_positions_span = (np.log10(np.max(positions)) - np.log10(np.min(positions)))
                log_span = (log_positions_span / (1 - (2.0 * violin_width_to_span_fraction)))
                violin_width = (violin_width_to_span_fraction * log_span)
            else:
                positions_span = (np.max(positions) - np.min(positions))
                span = (positions_span / (1 - (2.0 * violin_width_to_span_fraction)))
                violin_width = (violin_width_to_span_fraction * span)
        if (xscale == 'log'):
            if (data_length == 0):
                xlim = ((10 ** (np.log10(10.0) - violin_width)), (10 ** (np.log10(10.0) + violin_width)))
            else:
                xlim = ((10 ** (np.log10(np.min(positions)) - violin_width)), (10 ** (np.log10(np.max(positions)) + violin_width)))
        elif (data_length == 0):
            xlim = ((1.0 - violin_width), (1.0 + violin_width))
        else:
            xlim = ((np.min(positions) - violin_width), (np.max(positions) + violin_width))
    if (violin_width is None):
        if (xscale == 'log'):
            log_span = (np.log10(xlim[1]) - np.log10(xlim[0]))
            violin_width = (violin_width_to_span_fraction * log_span)
        else:
            span = (xlim[1] - xlim[0])
            violin_width = (violin_width_to_span_fraction * span)
    for idx in range(data_length):
        violin_position = positions[idx]
        violin_data = np.array(data[idx], dtype=float).flat
        if isinstance(violin_kwargs, collectionsAbc.Sequence):
            v_kwargs = violin_kwargs[idx]
        else:
            v_kwargs = violin_kwargs
        if isinstance(draw_summary_stat_kwargs, collectionsAbc.Sequence):
            v_draw_summary_stat_kwargs = draw_summary_stat_kwargs[idx]
        else:
            v_draw_summary_stat_kwargs = draw_summary_stat_kwargs
        try:
            first_element = next(iter(bin_edges))
            try:
                iter(first_element)
                violin_bin_edges = bin_edges[idx]
            except TypeError:
                violin_bin_edges = bin_edges
        except TypeError:
            msg = '`bin_edges` should be array or list or arrays'
            raise TypeError(msg)
        if isinstance(upper_trim_fraction, collectionsAbc.Sequence):
            v_upper_trim_fraction = upper_trim_fraction[idx]
        else:
            v_upper_trim_fraction = upper_trim_fraction
        if isinstance(lower_trim_fraction, collectionsAbc.Sequence):
            v_lower_trim_fraction = lower_trim_fraction[idx]
        else:
            v_lower_trim_fraction = lower_trim_fraction
        _plot_single_violin(violin_position=violin_position, violin_data=violin_data, violin_width=violin_width, violin_kwargs=v_kwargs, bin_edges=violin_bin_edges, density=density, vert=True, scale=xscale, upper_trim_fraction=v_upper_trim_fraction, lower_trim_fraction=v_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=v_draw_summary_stat_kwargs)
    if (model_fxn is not None):
        if (xscale == 'log'):
            model_xvalues = np.logspace(np.log10(xlim[0]), np.log10(xlim[1]), 100)
        else:
            model_xvalues = np.linspace(xlim[0], xlim[1], 100)
        try:
            model_yvalues = model_fxn(model_xvalues)
        except Exception:
            model_yvalues = [model_fxn(xvalue) for xvalue in model_xvalues]
        plt.plot(model_xvalues, model_yvalues, **draw_model_kwargs)
    data_xlim = xlim
    if (xscale == 'log'):
        next_violin_position = (10 ** (np.log10(data_xlim[0]) - violin_width))
    else:
        next_violin_position = (data_xlim[0] - violin_width)
    if ((xscale == 'log') and (log_zero_data is not None)):
        _plot_single_violin(violin_position=next_violin_position, violin_data=log_zero_data, violin_width=violin_width, violin_kwargs=log_zero_violin_kwargs, bin_edges=log_zero_bin_edges, density=density, vert=True, scale=xscale, upper_trim_fraction=log_zero_upper_trim_fraction, lower_trim_fraction=log_zero_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=log_zero_draw_summary_stat_kwargs)
        if (model_fxn is not None):
            model_zero_yvalue = model_fxn(0.0)
            plt.plot([(10 ** (np.log10(next_violin_position) - violin_width)), (10 ** (np.log10(next_violin_position) + violin_width))], [model_zero_yvalue, model_zero_yvalue], **draw_model_kwargs)
        if draw_log_zero_divider:
            plt.axvline((10 ** (np.log10(next_violin_position) + violin_width)), **draw_log_zero_divider_kwargs)
        xlim = ((10 ** (np.log10(next_violin_position) - violin_width)), xlim[1])
        next_violin_position = (10 ** (np.log10(next_violin_position) - (2 * violin_width)))
    if (max_data is not None):
        max_data = np.array(max_data, dtype=float).flat
        _plot_single_violin(violin_position=next_violin_position, violin_data=max_data, violin_width=violin_width, violin_kwargs=max_violin_kwargs, bin_edges=max_bin_edges, density=density, vert=True, scale=xscale, upper_trim_fraction=max_upper_trim_fraction, lower_trim_fraction=max_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=max_draw_summary_stat_kwargs)
        if (draw_max_line and (len(max_data) > 0)):
            summary_stat = draw_summary_stat_fxn(max_data)
            plt.plot([next_violin_position, xlim[1]], [summary_stat, summary_stat], **draw_max_line_kwargs)
        if draw_minmax_divider:
            if (xscale == 'log'):
                plt.axvline((10 ** (np.log10(next_violin_position) + violin_width)), **draw_minmax_divider_kwargs)
            else:
                plt.axvline((next_violin_position + violin_width), **draw_minmax_divider_kwargs)
        if (xscale == 'log'):
            xlim = ((10 ** (np.log10(next_violin_position) - violin_width)), xlim[1])
        else:
            xlim = ((next_violin_position - violin_width), xlim[1])
        if (xscale == 'log'):
            next_violin_position = (10 ** (np.log10(next_violin_position) - (2 * violin_width)))
        else:
            next_violin_position = (next_violin_position - (2 * violin_width))
    if (min_data is not None):
        min_data = np.array(min_data, dtype=float).flat
        _plot_single_violin(violin_position=next_violin_position, violin_data=min_data, violin_width=violin_width, violin_kwargs=min_violin_kwargs, bin_edges=min_bin_edges, density=density, vert=True, scale=xscale, upper_trim_fraction=min_upper_trim_fraction, lower_trim_fraction=min_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=min_draw_summary_stat_kwargs)
        if (draw_min_line and (len(min_data) > 0)):
            summary_stat = draw_summary_stat_fxn(min_data)
            plt.plot([next_violin_position, xlim[1]], [summary_stat, summary_stat], **draw_min_line_kwargs)
        if (draw_minmax_divider and (max_data is None)):
            if (xscale == 'log'):
                plt.axvline((10 ** (np.log10(next_violin_position) + violin_width)), **draw_minmax_divider_kwargs)
            else:
                plt.axvline((next_violin_position + violin_width), **draw_minmax_divider_kwargs)
        if (xscale == 'log'):
            xlim = ((10 ** (np.log10(next_violin_position) - violin_width)), xlim[1])
        else:
            xlim = ((next_violin_position - violin_width), xlim[1])
    plt.xscale(xscale)
    if (yscale == 'logicle'):
        plt.yscale(yscale, data=all_data, channel=channel)
    else:
        plt.yscale(yscale)
    plt.xlim(xlim)
    plt.ylim(ylim)
    ax = plt.gca()
    if (xscale == 'log'):
        next_violin_position = (10 ** (np.log10(data_xlim[0]) - violin_width))
        if (log_zero_data is not None):
            zero_tick_loc = next_violin_position
            next_violin_position = (10 ** (np.log10(next_violin_position) - (2 * violin_width)))
        else:
            zero_tick_loc = None
        if (max_data is not None):
            max_tick_loc = next_violin_position
            next_violin_position = (10 ** (np.log10(next_violin_position) - (2 * violin_width)))
        else:
            max_tick_loc = None
        min_tick_loc = (None if (min_data is None) else next_violin_position)
        if ((min_data is not None) or (max_data is not None) or (log_zero_data is not None)):
            data_lim_min = data_xlim[0]
        else:
            data_lim_min = None
        major_locator = _ViolinLogLocator(min_tick_loc=min_tick_loc, max_tick_loc=max_tick_loc, zero_tick_loc=zero_tick_loc, data_lim_min=data_lim_min)
        minor_locator = _ViolinLogLocator(min_tick_loc=None, max_tick_loc=None, zero_tick_loc=None, data_lim_min=data_lim_min, subs='auto')
        major_formatter = _ViolinLogFormatterSciNotation(min_tick_loc=min_tick_loc, max_tick_loc=max_tick_loc, zero_tick_loc=zero_tick_loc, min_tick_label=min_tick_label, max_tick_label=max_tick_label, zero_tick_label=log_zero_tick_label)
        minor_formatter = _ViolinLogFormatterSciNotation(min_tick_loc=min_tick_loc, max_tick_loc=max_tick_loc, zero_tick_loc=zero_tick_loc, min_tick_label=min_tick_label, max_tick_label=max_tick_label, zero_tick_label=log_zero_tick_label)
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.xaxis.set_minor_locator(minor_locator)
        ax.xaxis.set_minor_formatter(minor_formatter)
    else:
        next_violin_position = (data_xlim[0] - violin_width)
        if (max_data is not None):
            max_tick_loc = next_violin_position
            next_violin_position -= (2 * violin_width)
        else:
            max_tick_loc = None
        min_tick_loc = (None if (min_data is None) else next_violin_position)
        if ((min_data is not None) or (max_data is not None)):
            data_lim_min = data_xlim[0]
        else:
            data_lim_min = None
        major_locator = _ViolinAutoLocator(min_tick_loc=min_tick_loc, max_tick_loc=max_tick_loc, data_lim_min=data_lim_min)
        major_formatter = _ViolinScalarFormatter(min_tick_loc=min_tick_loc, max_tick_loc=max_tick_loc, min_tick_label=min_tick_label, max_tick_label=max_tick_label)
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
    if (xlabel is not None):
        plt.xlabel(xlabel)
    if (ylabel is not None):
        plt.ylabel(ylabel)
    elif ((data_length > 0) and hasattr(data[(- 1)], 'channels')):
        plt.ylabel(data[(- 1)].channels[0])
    if (title is not None):
        plt.title(title)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

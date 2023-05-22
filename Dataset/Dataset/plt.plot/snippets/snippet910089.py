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


def violin(data, channel=None, positions=None, violin_width=None, xscale=None, yscale=None, xlim=None, ylim=None, vert=True, num_bins=100, bin_edges=None, density=False, upper_trim_fraction=0.01, lower_trim_fraction=0.01, violin_width_to_span_fraction=0.1, violin_kwargs=None, draw_summary_stat=True, draw_summary_stat_fxn=np.mean, draw_summary_stat_kwargs=None, log_zero_tick_label=None, draw_log_zero_divider=True, draw_log_zero_divider_kwargs=None, xlabel=None, ylabel=None, title=None, savefig=None):
    '\n    Plot violin plot.\n\n    Illustrate the relative frequency of members of different populations\n    using normalized, symmetrical histograms ("violins") centered at\n    corresponding positions. Wider regions of violins indicate regions that\n    occur with greater frequency.\n\n    Parameters\n    ----------\n    data : 1D or ND array or list of 1D or ND arrays\n        A population or collection of populations for which to plot violins.\n        If ND arrays are used (e.g., FCSData), `channel` must be specified.\n    channel : int or str, optional\n        Channel from `data` to plot. If specified, data are assumed to be ND\n        arrays. String channel specifications are only supported for data\n        types that support string-based indexing (e.g., FCSData).\n    positions : scalar or array, optional\n        Positions at which to center violins.\n    violin_width : scalar, optional\n        Width of violin. If the scale of the position axis (`xscale` if `vert`\n        is True, `yscale` if `vert` is False) is ``log``, the units are\n        decades. If not specified, `violin_width` is calculated from the\n        limits of the position axis (`xlim` if `vert` is True, `ylim` if\n        `vert` is False) and `violin_width_to_span_fraction`. If only one\n        violin is specified in `data`, `violin_width` = 0.5.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xscale : {\'linear\', \'log\', \'logicle\'}, optional\n        Scale of the x-axis. ``logicle`` is only supported for horizontal\n        violin plots (i.e., when `vert` is False). Default is ``linear`` if\n        `vert` is True, ``logicle`` if `vert` is False.\n    yscale : {\'logicle\', \'linear\', \'log\'}, optional\n        Scale of the y-axis. If `vert` is False, ``logicle`` is not\n        supported. Default is ``logicle`` if `vert` is True, ``linear`` if\n        `vert` is False.\n    xlim, ylim : tuple, optional\n        Limits of the x-axis and y-axis views. If not specified, the view of\n        the position axis (`xlim` if `vert` is True, `ylim` if `vert` if\n        False) is calculated to pad the extreme violins with\n        0.5 * `violin_width`. If `violin_width` is also not specified,\n        `violin_width` is calculated to satisfy the 0.5 * `violin_width`\n        padding and `violin_width_to_span_fraction`. If not specified, the\n        view of the data axis (`ylim` if `vert` is True, `xlim` if `vert` is\n        False) is calculated to span all violins (before they are\n        aesthetically trimmed).\n    vert : bool, optional\n        Flag specifying to illustrate a vertical violin plot. If False, a\n        horizontal violin plot is illustrated.\n    num_bins : int, optional\n        Number of bins to bin population members. Ignored if `bin_edges` is\n        specified.\n    bin_edges : array or list of arrays, optional\n        Bin edges used to bin population members. Bin edges can be specified\n        for individual violins using a list of arrays of the same length as\n        `data`. If not specified, `bin_edges` is calculated to span the data\n        axis (`ylim` if `vert` is True, `xlim` if `vert` is False) logicly,\n        linearly, or logarithmically (based on the scale of the data axis;\n        `yscale` if `vert` is True, `xscale` if `vert` is False) using\n        `num_bins`.\n    density : bool, optional\n        `density` parameter passed to the ``np.histogram()`` command that bins\n        population members for each violin. If True, violin width represents\n        relative frequency *density* instead of relative frequency (i.e., bins\n        are normalized by their width).\n    upper_trim_fraction : float or list of floats, optional\n        Fraction of members to trim (discard) from the top of the violin\n        (e.g., for aesthetic purposes). Upper trim fractions can be specified\n        for individual violins using a list of floats of the same length as\n        `data`.\n    lower_trim_fraction : float or list of floats, optional\n        Fraction of members to trim (discard) from the bottom of the violin\n        (e.g., for aesthetic purposes). Lower trim fractions can be specified\n        for individual violins using a list of floats of the same length as\n        `data`.\n    violin_width_to_span_fraction : float, optional\n        Fraction of the position axis span (`xlim` if `vert` is True, `ylim`\n        if `vert` is False) that a violin should span. Ignored if\n        `violin_width` is specified.\n    violin_kwargs : dict or list of dicts, optional\n        Keyword arguments passed to the ``plt.fill_between()`` command that\n        illustrates each violin. Keyword arguments can be specified for\n        individual violins using a list of dicts of the same length as `data`.\n        Default = {\'facecolor\':\'gray\', \'edgecolor\':\'black\'}.\n    draw_summary_stat : bool, optional\n        Flag specifying to illustrate a summary statistic for each violin.\n    draw_summary_stat_fxn : function, optional\n        Function used to calculate the summary statistic for each violin.\n        Summary statistics are calculated prior to aesthetic trimming.\n    draw_summary_stat_kwargs : dict or list of dicts, optional\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates each violin\'s summary statistic. Keyword arguments can be\n        specified for individual violins using a list of dicts of the same\n        length as `data`. Default = {\'color\':\'black\'}.\n    log_zero_tick_label : str, optional\n        Label of position=0 violin tick if the position axis scale (`xscale`\n        if `vert` is True, `yscale` if `vert` is False) is ``log``. Default\n        is generated by the default log tick formatter\n        (``matplotlib.ticker.LogFormatterSciNotation``) with x=0.\n    draw_log_zero_divider : bool, optional\n        Flag specifying to illustrate a line separating the position=0 violin\n        from the other violins if the position axis scale (`xscale` if `vert`\n        is True, `yscale` if `vert` is False) is ``log``.\n    draw_log_zero_divider_kwargs : dict, optional\n        Keyword arguments passed to the ``plt.axvline()`` or ``plt.axhline()``\n        command that illustrates the position=0 violin divider. Default =\n        {\'color\':\'gray\',\'linestyle\':\':\'}.\n    xlabel, ylabel : str, optional\n        Labels to use on the x and y axes. If a label for the data axis is not\n        specified (`ylabel` if `vert` is True, `xlabel` if `vert` is False),\n        the channel name will be used if possible (extracted from the last\n        data object).\n    title : str, optional\n        Plot title.\n\n    '
    if (xscale is None):
        xscale = ('linear' if vert else 'logicle')
    if (yscale is None):
        yscale = ('logicle' if vert else 'linear')
    if (violin_kwargs is None):
        violin_kwargs = {'facecolor': 'gray', 'edgecolor': 'black'}
    if (draw_summary_stat_kwargs is None):
        draw_summary_stat_kwargs = {'color': 'black'}
    if (draw_log_zero_divider_kwargs is None):
        draw_log_zero_divider_kwargs = {'color': 'gray', 'linestyle': ':'}
    if vert:
        if (xscale not in ('linear', 'log')):
            msg = "when `vert` is True, `xscale` must be 'linear' or 'log'"
            raise ValueError(msg)
        if (yscale not in ('logicle', 'linear', 'log')):
            msg = "when `vert` is True, `yscale` must be 'logicle',"
            msg += " 'linear', or 'log'"
            raise ValueError(msg)
        data_scale = yscale
        position_scale = xscale
    else:
        if (xscale not in ('logicle', 'linear', 'log')):
            msg = "when `vert` is False, `xscale` must be 'logicle',"
            msg += " 'linear', or 'log'"
            raise ValueError(msg)
        if (yscale not in ('linear', 'log')):
            msg = "when `vert` is False, `yscale` must be 'linear' or 'log'"
            raise ValueError(msg)
        data_scale = xscale
        position_scale = yscale
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
    if (positions is None):
        positions = np.arange(1, (data_length + 1), dtype=float)
        if (position_scale == 'log'):
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
    if ((vert and (ylim is None)) or ((not vert) and (xlim is None))):
        data_min = np.inf
        data_max = (- np.inf)
        for idx in range(data_length):
            violin_data = np.array(data[idx], dtype=float).flat
            if (len(violin_data) > 0):
                violin_min = np.min(violin_data)
                violin_max = np.max(violin_data)
                if (violin_min < data_min):
                    data_min = violin_min
                if (violin_max > data_max):
                    data_max = violin_max
        data_lim = (data_min, data_max)
        if all(np.isinf(data_lim)):
            data_lim = (0.0, 1.0)
    else:
        data_lim = (ylim if vert else xlim)
    if (bin_edges is None):
        if (data_scale == 'logicle'):
            t = _LogicleTransform(data=data, channel=channel)
            t_min = t.inverted().transform_non_affine(x=data_lim[0], mask_out_of_range=False)
            t_max = t.inverted().transform_non_affine(x=data_lim[1], mask_out_of_range=False)
            t_bin_edges = np.linspace(t_min, t_max, (num_bins + 1))
            bin_edges = t.transform_non_affine(t_bin_edges)
        elif (data_scale == 'linear'):
            bin_edges = np.linspace(data_lim[0], data_lim[1], (num_bins + 1))
        else:
            bin_edges = np.logspace(np.log10(data_lim[0]), np.log10(data_lim[1]), (num_bins + 1))
    log_zero_data = None
    log_zero_violin_kwargs = None
    log_zero_draw_summary_stat_kwargs = None
    log_zero_bin_edges = None
    log_zero_upper_trim_fraction = None
    log_zero_lower_trim_fraction = None
    if ((position_scale == 'log') and (0 in list(positions))):
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
    if ((vert and (xlim is None)) or ((not vert) and (ylim is None))):
        if (violin_width is None):
            if (data_length <= 1):
                violin_width = 0.5
            elif (position_scale == 'log'):
                log_positions_span = (np.log10(np.max(positions)) - np.log10(np.min(positions)))
                log_span = (log_positions_span / (1 - (2.0 * violin_width_to_span_fraction)))
                violin_width = (violin_width_to_span_fraction * log_span)
            else:
                positions_span = (np.max(positions) - np.min(positions))
                span = (positions_span / (1 - (2.0 * violin_width_to_span_fraction)))
                violin_width = (violin_width_to_span_fraction * span)
        if (position_scale == 'log'):
            if (data_length == 0):
                position_lim = ((10 ** (np.log10(10.0) - violin_width)), (10 ** (np.log10(10.0) + violin_width)))
            else:
                position_lim = ((10 ** (np.log10(np.min(positions)) - violin_width)), (10 ** (np.log10(np.max(positions)) + violin_width)))
        elif (data_length == 0):
            position_lim = ((1.0 - violin_width), (1.0 + violin_width))
        else:
            position_lim = ((np.min(positions) - violin_width), (np.max(positions) + violin_width))
    else:
        position_lim = (xlim if vert else ylim)
    if (violin_width is None):
        if (position_scale == 'log'):
            log_span = (np.log10(position_lim[1]) - np.log10(position_lim[0]))
            violin_width = (violin_width_to_span_fraction * log_span)
        else:
            span = (position_lim[1] - position_lim[0])
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
        _plot_single_violin(violin_position=violin_position, violin_data=violin_data, violin_width=violin_width, violin_kwargs=v_kwargs, bin_edges=violin_bin_edges, density=density, vert=vert, scale=position_scale, upper_trim_fraction=v_upper_trim_fraction, lower_trim_fraction=v_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=v_draw_summary_stat_kwargs)
    data_position_lim = position_lim
    if ((position_scale == 'log') and (log_zero_data is not None)):
        next_violin_position = (10 ** (np.log10(data_position_lim[0]) - violin_width))
        _plot_single_violin(violin_position=next_violin_position, violin_data=log_zero_data, violin_width=violin_width, violin_kwargs=log_zero_violin_kwargs, bin_edges=log_zero_bin_edges, density=density, vert=vert, scale=position_scale, upper_trim_fraction=log_zero_upper_trim_fraction, lower_trim_fraction=log_zero_lower_trim_fraction, draw_summary_stat=draw_summary_stat, draw_summary_stat_fxn=draw_summary_stat_fxn, draw_summary_stat_kwargs=log_zero_draw_summary_stat_kwargs)
        if draw_log_zero_divider:
            if vert:
                plt.axvline((10 ** (np.log10(next_violin_position) + violin_width)), **draw_log_zero_divider_kwargs)
            else:
                plt.axhline((10 ** (np.log10(next_violin_position) + violin_width)), **draw_log_zero_divider_kwargs)
        position_lim = ((10 ** (np.log10(next_violin_position) - violin_width)), position_lim[1])
    if (xscale == 'logicle'):
        plt.xscale(xscale, data=data, channel=channel)
    else:
        plt.xscale(xscale)
    if (yscale == 'logicle'):
        plt.yscale(yscale, data=data, channel=channel)
    else:
        plt.yscale(yscale)
    if vert:
        plt.xlim(position_lim)
        plt.ylim(data_lim)
    else:
        plt.xlim(data_lim)
        plt.ylim(position_lim)
    ax = plt.gca()
    if (position_scale == 'log'):
        if (log_zero_data is not None):
            next_violin_position = (10 ** (np.log10(data_position_lim[0]) - violin_width))
            zero_tick_loc = next_violin_position
            data_lim_min = data_position_lim[0]
        else:
            zero_tick_loc = None
            data_lim_min = None
        major_locator = _ViolinLogLocator(zero_tick_loc=zero_tick_loc, data_lim_min=data_lim_min)
        minor_locator = _ViolinLogLocator(zero_tick_loc=None, data_lim_min=data_lim_min, subs='auto')
        major_formatter = _ViolinLogFormatterSciNotation(zero_tick_loc=zero_tick_loc, zero_tick_label=log_zero_tick_label)
        minor_formatter = _ViolinLogFormatterSciNotation(zero_tick_loc=zero_tick_loc, zero_tick_label=log_zero_tick_label)
        if vert:
            ax.xaxis.set_major_locator(major_locator)
            ax.xaxis.set_major_formatter(major_formatter)
            ax.xaxis.set_minor_locator(minor_locator)
            ax.xaxis.set_minor_formatter(minor_formatter)
        else:
            ax.yaxis.set_major_locator(major_locator)
            ax.yaxis.set_major_formatter(major_formatter)
            ax.yaxis.set_minor_locator(minor_locator)
            ax.yaxis.set_minor_formatter(minor_formatter)
    else:
        data_lim_min = None
        major_locator = _ViolinAutoLocator(data_lim_min=data_lim_min)
        major_formatter = _ViolinScalarFormatter()
        if vert:
            ax.xaxis.set_major_locator(major_locator)
            ax.xaxis.set_major_formatter(major_formatter)
        else:
            ax.yaxis.set_major_locator(major_locator)
            ax.yaxis.set_major_formatter(major_formatter)
    if (xlabel is not None):
        plt.xlabel(xlabel)
    if (ylabel is not None):
        plt.ylabel(ylabel)
    if (vert and (ylabel is None) and (data_length > 0) and hasattr(data[(- 1)], 'channels')):
        plt.ylabel(data[(- 1)].channels[0])
    elif ((not vert) and (xlabel is None) and (data_length > 0) and hasattr(data[(- 1)], 'channels')):
        plt.xlabel(data[(- 1)].channels[0])
    if (title is not None):
        plt.title(title)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()

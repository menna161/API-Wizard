import os
import copy
import collections
import datetime
import six
import warnings
import numpy as np
import FlowCal.plot


def hist_bins(self, channels=None, nbins=None, scale='logicle', **kwargs):
    '\n        Get histogram bin edges for the specified channel(s).\n\n        These cover the range specified in ``FCSData.range(channels)`` with\n        a number of bins `nbins`, with linear, logarithmic, or logicle\n        spacing.\n\n        Parameters\n        ----------\n        channels : int, str, list of int, list of str\n            Channel(s) for which to generate histogram bins. If None,\n            return a list with bins for all channels, in the order of\n            ``FCSData.channels``.\n        nbins : int or list of ints, optional\n            The number of bins to calculate. If `channels` specifies a list\n            of channels, `nbins` should be a list of integers. If `nbins`\n            is None, use ``FCSData.resolution(channel)``.\n        scale : str, optional\n            Scale in which to generate bins. Can be either ``linear``,\n            ``log``, or ``logicle``.\n        kwargs : optional\n            Keyword arguments specific to the selected bin scaling. Linear\n            and logarithmic scaling do not use additional arguments.\n            For logicle scaling, the following parameters can be provided:\n\n            T : float, optional\n                Maximum range of data. If not provided, use ``range[1]``.\n            M : float, optional\n                (Asymptotic) number of decades in scaled units. If not\n                provided, calculate from the following::\n\n                    max(4.5, 4.5 / np.log10(262144) * np.log10(T))\n\n            W : float, optional\n                Width of linear range in scaled units. If not provided,\n                calculate using the following relationship::\n\n                    W = (M - log10(T / abs(r))) / 2\n\n                Where ``r`` is the minimum negative event. If no negative\n                events are present, W is set to zero.\n\n        Return\n        ------\n        array or list of arrays\n            Histogram bin edges for the specified channel(s).\n\n        Notes\n        -----\n        If ``range[0]`` is equal or less than zero and `scale` is  ``log``,\n        the lower limit of the range is replaced with one.\n\n        Logicle scaling uses the LogicleTransform class in the plot module.\n\n        References\n        ----------\n        .. [1] D.R. Parks, M. Roederer, W.A. Moore, "A New Logicle Display\n        Method Avoids Deceptive Effects of Logarithmic Scaling for Low\n        Signals and Compensated Data," Cytometry Part A 69A:541-551, 2006,\n        PMID 16604519.\n\n        '
    if (channels is None):
        channels = list(self._channels)
    channels = self._name_to_index(channels)
    channel_list = channels
    if (not isinstance(channel_list, list)):
        channel_list = [channel_list]
    if (not isinstance(nbins, list)):
        nbins = ([nbins] * len(channel_list))
    if (not isinstance(scale, list)):
        scale = ([scale] * len(channel_list))
    bins = []
    for (channel, nbins_channel, scale_channel) in zip(channel_list, nbins, scale):
        res_channel = self.resolution(channel)
        if (nbins_channel is None):
            nbins_channel = res_channel
        range_channel = self.range(channel)
        if (scale_channel == 'linear'):
            delta_res = ((range_channel[1] - range_channel[0]) / (res_channel - 1))
            bins_channel = np.linspace((range_channel[0] - (delta_res / 2)), (range_channel[1] + (delta_res / 2)), (nbins_channel + 1))
        elif (scale_channel == 'log'):
            if (range_channel[0] <= 0):
                range_channel[0] = min(1.0, (range_channel[1] / 100000.0))
            range_channel = [np.log10(range_channel[0]), np.log10(range_channel[1])]
            delta_res = ((range_channel[1] - range_channel[0]) / (res_channel - 1))
            bins_channel = np.linspace((range_channel[0] - (delta_res / 2)), (range_channel[1] + (delta_res / 2)), (nbins_channel + 1))
            bins_channel = (10 ** bins_channel)
        elif (scale_channel == 'logicle'):
            t = FlowCal.plot._LogicleTransform(data=self, channel=channel, **kwargs)
            delta_res = (float(t.M) / (res_channel - 1))
            s = np.linspace(((- delta_res) / 2.0), (t.M + (delta_res / 2.0)), (nbins_channel + 1))
            bins_channel = t.transform_non_affine(s)
        else:
            raise ValueError('scale "{}" not supported'.format(scale_channel))
        bins.append(bins_channel)
    if (not isinstance(channels, list)):
        bins = bins[0]
    return bins

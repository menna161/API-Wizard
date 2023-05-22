import numpy as np
import scipy.ndimage.filters
import skimage.measure
import collections


def density2d(data, channels=[0, 1], bins=1024, gate_fraction=0.65, xscale='logicle', yscale='logicle', sigma=10.0, bin_mask=None, full_output=False):
    '\n    Gate that preserves events in the region with highest density.\n\n    Gate out all events in `data` but those near regions of highest\n    density for the two specified channels.\n\n    Parameters\n    ----------\n    data : FCSData or numpy array\n        NxD flow cytometry data where N is the number of events and D is\n        the number of parameters (aka channels).\n    channels : list of int, list of str, optional\n        Two channels on which to perform gating.\n    bins : int or array_like or [int, int] or [array, array], optional\n        Bins used for gating:\n\n          - If None, use ``data.hist_bins`` to obtain bin edges for both\n            axes. None is not allowed if ``data.hist_bins`` is not\n            available.\n          - If int, `bins` specifies the number of bins to use for both\n            axes. If ``data.hist_bins`` exists, it will be used to generate\n            a number `bins` of bins.\n          - If array_like, `bins` directly specifies the bin edges to use\n            for both axes.\n          - If [int, int], each element of `bins` specifies the number of\n            bins for each axis. If ``data.hist_bins`` exists, use it to\n            generate ``bins[0]`` and ``bins[1]`` bin edges, respectively.\n          - If [array, array], each element of `bins` directly specifies\n            the bin edges to use for each axis.\n          - Any combination of the above, such as [int, array], [None,\n            int], or [array, int]. In this case, None indicates to generate\n            bin edges using ``data.hist_bins`` as above, int indicates the\n            number of bins to generate, and an array directly indicates the\n            bin edges. Note that None is not allowed if ``data.hist_bins``\n            does not exist.\n    gate_fraction : float, optional\n        Fraction of events to retain after gating. Should be between 0 and\n        1, inclusive.\n    xscale : str, optional\n        Scale of the bins generated for the x axis, either ``linear``,\n        ``log``, or ``logicle``. `xscale` is ignored in `bins` is an array\n        or a list of arrays.\n    yscale : str, optional\n        Scale of the bins generated for the y axis, either ``linear``,\n        ``log``, or ``logicle``. `yscale` is ignored in `bins` is an array\n        or a list of arrays.\n    sigma : scalar or sequence of scalars, optional\n        Standard deviation for Gaussian kernel used by\n        `scipy.ndimage.filters.gaussian_filter` to smooth 2D histogram\n        into a density.\n    bin_mask : 2D numpy array of bool, optional\n        A 2D mask array that selects the 2D histogram bins permitted by the\n        gate. Corresponding bin edges should be specified via `bins`. If\n        `bin_mask` is specified, `gate_fraction` and `sigma` are ignored.\n    full_output : bool, optional\n        Flag specifying to return additional outputs. If true, the outputs\n        are given as a namedtuple.\n\n    Returns\n    -------\n    gated_data : FCSData or numpy array\n        Gated flow cytometry data of the same format as `data`.\n    mask : numpy array of bool, only if ``full_output==True``\n        Boolean gate mask used to gate data such that ``gated_data =\n        data[mask]``.\n    contour : list of 2D numpy arrays, only if ``full_output==True``\n        List of 2D numpy array(s) of x-y coordinates tracing out the edge of\n        the gated region. If `bin_mask` is specified, `contour` is None.\n    bin_edges : 2-tuple of numpy arrays, only if ``full_output==True``\n        X-axis and y-axis bin edges used by the np.histogram2d() command that\n        bins events (bin_edges=(x_edges,y_edges)).\n    bin_mask : 2D numpy array of bool, only if ``full_output==True``\n        A 2D mask array that selects the 2D histogram bins permitted by the\n        gate.\n\n    Raises\n    ------\n    ValueError\n        If more or less than 2 channels are specified.\n    ValueError\n        If `data` has less than 2 dimensions or less than 2 events.\n    Exception\n        If an unrecognized matplotlib Path code is encountered when\n        attempting to generate contours.\n\n    Notes\n    -----\n    The algorithm for gating based on density works as follows:\n\n        1) Calculate 2D histogram of `data` in the specified channels.\n        2) Map each event from `data` to its histogram bin (implicitly\n           gating out any events which exist outside specified `bins`).\n        3) Use `gate_fraction` to determine number of events to retain\n           (rounded up). Only events which are not implicitly gated out\n           are considered.\n        4) Smooth 2D histogram using a 2D Gaussian filter.\n        5) Normalize smoothed histogram to obtain valid probability mass\n           function (PMF).\n        6) Sort bins by probability.\n        7) Accumulate events (starting with events belonging to bin with\n           highest probability ("densest") and proceeding to events\n           belonging to bins with lowest probability) until at least the\n           desired number of events is achieved. While the algorithm\n           attempts to get as close to `gate_fraction` fraction of events\n           as possible, more events may be retained based on how many\n           events fall into each histogram bin (since entire bins are\n           retained at a time, not individual events).\n\n    '
    if (len(channels) != 2):
        raise ValueError('2 channels should be specified')
    data_ch = data[(:, channels)]
    if (data_ch.ndim == 1):
        data_ch = data_ch.reshape(((- 1), 1))
    if (data_ch.ndim < 2):
        raise ValueError('data should have at least 2 dimensions')
    if (data_ch.shape[0] <= 1):
        raise ValueError('data should have more than one event')
    if (hasattr(data_ch, 'hist_bins') and hasattr(data_ch.hist_bins, '__call__')):
        if (hasattr(bins, '__iter__') and (len(bins) == 2)):
            if (not hasattr(bins[0], '__iter__')):
                bins[0] = data_ch.hist_bins(channels=0, nbins=bins[0], scale=xscale)
            if (not hasattr(bins[1], '__iter__')):
                bins[1] = data_ch.hist_bins(channels=1, nbins=bins[1], scale=yscale)
        elif (not hasattr(bins, '__iter__')):
            bins = [data_ch.hist_bins(channels=0, nbins=bins, scale=xscale), data_ch.hist_bins(channels=1, nbins=bins, scale=yscale)]
    (H, xe, ye) = np.histogram2d(data_ch[(:, 0)], data_ch[(:, 1)], bins=bins)
    xe = np.array(xe, dtype=float)
    ye = np.array(ye, dtype=float)
    event_indices = np.arange(data_ch.shape[0])
    x_bin_indices = (np.digitize(data_ch[(:, 0)], bins=xe) - 1)
    y_bin_indices = (np.digitize(data_ch[(:, 1)], bins=ye) - 1)
    x_bin_indices[(data_ch[(:, 0)] == xe[(- 1)])] = (len(xe) - 2)
    y_bin_indices[(data_ch[(:, 1)] == ye[(- 1)])] = (len(ye) - 2)
    outlier_mask = ((((x_bin_indices == (- 1)) | (x_bin_indices == (len(xe) - 1))) | (y_bin_indices == (- 1))) | (y_bin_indices == (len(ye) - 1)))
    event_indices = event_indices[(~ outlier_mask)]
    x_bin_indices = x_bin_indices[(~ outlier_mask)]
    y_bin_indices = y_bin_indices[(~ outlier_mask)]
    filler = np.frompyfunc((lambda x: list()), 1, 1)
    H_events = np.empty_like(H, dtype=object)
    filler(H_events, H_events)
    for (event_idx, x_bin_idx, y_bin_idx) in zip(event_indices, x_bin_indices, y_bin_indices):
        H_events[(x_bin_idx, y_bin_idx)].append(event_idx)
    contours = None
    if (bin_mask is None):
        if ((gate_fraction < 0) or (gate_fraction > 1)):
            msg = 'gate fraction should be between 0 and 1, inclusive'
            raise ValueError(msg)
        n = int(np.ceil((gate_fraction * float(len(event_indices)))))
        if (n == 0):
            mask = np.zeros(shape=data_ch.shape[0], dtype=bool)
            gated_data = data[mask]
            if full_output:
                return Density2dGateOutput(gated_data=gated_data, mask=mask, contour=[], bin_edges=(xe, ye), bin_mask=np.zeros_like(H, dtype=bool))
            else:
                return gated_data
        sH = scipy.ndimage.filters.gaussian_filter(H, sigma=sigma, order=0, mode='constant', cval=0.0, truncate=6.0)
        D = (sH / np.sum(sH))
        vD = D.ravel(order='C')
        vH = H.ravel(order='C')
        sidx = np.argsort(vD)[::(- 1)]
        svH = vH[sidx]
        csvH = np.cumsum(svH)
        Nidx = np.nonzero((csvH >= n))[0][0]
        accepted_bin_indices = sidx[:(Nidx + 1)]
        bin_mask = np.zeros_like(H, dtype=bool)
        v_bin_mask = bin_mask.ravel(order='C')
        v_bin_mask[accepted_bin_indices] = True
        bin_mask = v_bin_mask.reshape(H.shape, order='C')
        if full_output:
            contours_ij = skimage.measure.find_contours(D, vD[sidx[Nidx]])
            xc = ((xe[:(- 1)] + xe[1:]) / 2.0)
            yc = ((ye[:(- 1)] + ye[1:]) / 2.0)
            contours = [np.array([np.interp(contour_ij[(:, 0)], np.arange(len(xc)), xc), np.interp(contour_ij[(:, 1)], np.arange(len(yc)), yc)]).T for contour_ij in contours_ij]
    accepted_data_indices = H_events[bin_mask]
    accepted_data_indices = np.array([item for sublist in accepted_data_indices for item in sublist], dtype=int)
    mask = np.zeros(shape=data.shape[0], dtype=bool)
    mask[accepted_data_indices] = True
    gated_data = data[mask]
    if full_output:
        return Density2dGateOutput(gated_data=gated_data, mask=mask, contour=contours, bin_edges=(xe, ye), bin_mask=bin_mask)
    else:
        return gated_data

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


def tick_values(self, vmin, vmax):
    '\n        Get a set of tick values properly spaced for logicle axis.\n\n        '
    b = self._transform.base
    if ((self._transform.W == 0) or ((self._transform.M / self._transform.W) > self.numticks)):
        self._transform = _LogicleTransform(T=self._transform.T, M=self._transform.M, W=(self._transform.M / self.numticks))
    t = (- self._transform.transform_non_affine(0))
    if (vmax < vmin):
        (vmin, vmax) = (vmax, vmin)
    vmins = self._transform.inverted().transform_non_affine(vmin)
    vmaxs = self._transform.inverted().transform_non_affine(vmax)
    has_linear = has_log = False
    if (vmin <= t):
        has_linear = True
        if (vmax > t):
            has_log = True
    else:
        has_log = True
    if has_linear:
        fraction_linear = ((min(vmaxs, (2 * self._transform.W)) - vmins) / (vmaxs - vmins))
        numticks_linear = np.round((self.numticks * fraction_linear))
    else:
        numticks_linear = 0
    if has_log:
        fraction_log = ((vmaxs - max(vmins, (2 * self._transform.W))) / (vmaxs - vmins))
        numticks_log = np.round((self.numticks * fraction_log))
    else:
        numticks_log = 0
    if has_log:
        log_ext_range = [np.floor((np.log(max(vmin, t)) / np.log(b))), np.ceil((np.log(vmax) / np.log(b)))]
        if (vmin <= 0):
            zero_s = self._transform.inverted().transform_non_affine(0)
            min_tick_space = (1.0 / self.numticks)
            while True:
                min_tick_s = self._transform.inverted().transform_non_affine((b ** log_ext_range[0]))
                if ((((min_tick_s - zero_s) / (vmaxs - vmins)) < min_tick_space) and ((log_ext_range[0] + 1) < log_ext_range[1])):
                    log_ext_range[0] += 1
                else:
                    break
        log_decades = (log_ext_range[1] - log_ext_range[0])
        if (numticks_log > 1):
            log_step = max(np.floor((float(log_decades) / (numticks_log - 1))), 1)
        else:
            log_step = 1
    else:
        linear_range = [vmin, vmax]
        linear_step = (_base_down((linear_range[1] - linear_range[0]), b) / b)
        while (((linear_range[1] - linear_range[0]) / linear_step) > numticks_linear):
            linear_step *= b
        vmin_ext = (np.floor((linear_range[0] / linear_step)) * linear_step)
        vmax_ext = (np.ceil((linear_range[1] / linear_step)) * linear_step)
        linear_range_ext = [vmin_ext, vmax_ext]
    major_ticklocs = []
    if has_log:
        if has_linear:
            major_ticklocs.append((- (b ** log_ext_range[0])))
            major_ticklocs.append(0)
        major_ticklocs.extend((b ** np.arange(log_ext_range[0], np.nextafter(log_ext_range[1], np.inf), log_step)))
    else:
        major_ticklocs.extend(np.arange(linear_range_ext[0], np.nextafter(linear_range_ext[1], np.inf), linear_step))
    major_ticklocs = np.array(major_ticklocs)
    subs = self._subs
    if ((subs is not None) and ((len(subs) > 1) or (subs[0] != 1.0))):
        ticklocs = []
        if has_log:
            for major_tickloc in major_ticklocs:
                ticklocs.extend((subs * major_tickloc))
            major_ticklocs_pos = major_ticklocs[(major_ticklocs > 0)]
            if len(major_ticklocs_pos):
                tickloc_next_low = (np.min(major_ticklocs_pos) / b)
                ticklocs.append(tickloc_next_low)
                ticklocs.extend((subs * tickloc_next_low))
            if (vmin < 0):
                ticklocs.extend([(- ti) for ti in ticklocs if (ti < (- vmin))])
        else:
            ticklocs = list(major_ticklocs)
            if ((vmin < 0) and (vmax > 0)):
                major_ticklocs_nonzero = major_ticklocs[np.nonzero(major_ticklocs)]
                tickloc_next_low = (np.min(np.abs(major_ticklocs_nonzero)) / b)
                ticklocs.append(tickloc_next_low)
                ticklocs.extend((subs * tickloc_next_low))
                ticklocs.append((- tickloc_next_low))
                ticklocs.extend((subs * (- tickloc_next_low)))
    else:
        ticklocs = major_ticklocs
    ticklocs = [t for t in ticklocs if ((t >= vmin) and (t <= vmax))]
    return self.raise_if_exceeds(np.array(ticklocs))

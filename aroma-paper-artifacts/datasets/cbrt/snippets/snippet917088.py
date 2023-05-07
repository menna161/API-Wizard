import math
import torch
from torch.nn import functional as F
from pixelflow.transforms.functional.splines._utils import searchsorted, cbrt


def unconstrained_cubic_spline(inputs, unnormalized_widths, unnormalized_heights, unnorm_derivatives_left, unnorm_derivatives_right, inverse=False, tail_bound=1.0, tails='linear', min_bin_width=DEFAULT_MIN_BIN_WIDTH, min_bin_height=DEFAULT_MIN_BIN_HEIGHT, eps=DEFAULT_EPS, quadratic_threshold=DEFAULT_QUADRATIC_THRESHOLD):
    inside_interval_mask = ((inputs >= (- tail_bound)) & (inputs <= tail_bound))
    outside_interval_mask = (~ inside_interval_mask)
    outputs = torch.zeros_like(inputs)
    logabsdet = torch.zeros_like(inputs)
    if (tails == 'linear'):
        outputs[outside_interval_mask] = inputs[outside_interval_mask]
        logabsdet[outside_interval_mask] = 0
    else:
        raise RuntimeError('{} tails are not implemented.'.format(tails))
    (outputs[inside_interval_mask], logabsdet[inside_interval_mask]) = cubic_spline(inputs=inputs[inside_interval_mask], unnormalized_widths=unnormalized_widths[(inside_interval_mask, :)], unnormalized_heights=unnormalized_heights[(inside_interval_mask, :)], unnorm_derivatives_left=unnorm_derivatives_left[(inside_interval_mask, :)], unnorm_derivatives_right=unnorm_derivatives_right[(inside_interval_mask, :)], inverse=inverse, left=(- tail_bound), right=tail_bound, bottom=(- tail_bound), top=tail_bound, min_bin_width=min_bin_width, min_bin_height=min_bin_height, eps=eps, quadratic_threshold=quadratic_threshold)
    return (outputs, logabsdet)

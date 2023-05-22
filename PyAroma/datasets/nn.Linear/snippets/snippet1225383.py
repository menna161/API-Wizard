from .weight_norm import WeightNorm
from .reparameterization import Reparameterization


def remove_weight_norm(module, name='', remove_all=False):
    '\n    Removes the weight normalization reparameterization of a parameter from a module.\n    If no parameter is supplied then all weight norm parameterizations are removed.\n    Args:\n        module (nn.Module): containing module\n        name (str, optional): name of weight parameter\n    Example:\n        >>> m = apply_weight_norm(nn.Linear(20, 40))\n        >>> remove_weight_norm(m)\n    '
    return remove_reparameterization(module, reparameterization=WeightNorm, name=name, remove_all=remove_all)

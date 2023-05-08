from .weight_norm import WeightNorm
from .reparameterization import Reparameterization


def apply_reparameterization(module, reparameterization=None, name='', dim=0, hook_child=True):
    "\n    Applies a given weight reparameterization (such as weight normalization) to\n    a parameter in the given module. If no parameter is given, applies the reparameterization\n    to all parameters in model (except 1-d vectors and scalars).\n\n    Args:\n        module (nn.Module): containing module\n        reparameterization (Reparameterization): reparamaterization class to apply\n        name (str, optional): name of weight parameter\n        dim (int, optional): dimension over which to perform reparameterization op\n        hook_child (boolean, optional): adds reparameterization hook to direct parent of the \n            parameters. If False, it's added to `module` instead. Default: True\n\n    Returns:\n        The original module with the reparameterization hook\n\n    Example::\n\n        >>> m = apply_reparameterization(nn.Linear(20, 40), WeightNorm)\n        Linear (20 -> 40)\n\n    "
    assert (reparameterization is not None)
    if (name != ''):
        Reparameterization.apply(module, name, dim, reparameterization, hook_child)
    else:
        names = list(module.state_dict().keys())
        for name in names:
            apply_reparameterization(module, reparameterization, name, dim, hook_child)
    return module

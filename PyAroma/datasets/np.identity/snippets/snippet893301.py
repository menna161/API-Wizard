import numpy as np
from . import _base


@classmethod
def exp(cls, phi):
    'Exponential map for :math:`SO(3)`, which computes a transformation from a tangent vector:\n\n        .. math::\n            \\mathbf{C}(\\boldsymbol{\\phi}) =\n            \\exp(\\boldsymbol{\\phi}^\\wedge) =\n            \\begin{cases}\n                \\mathbf{1} + \\boldsymbol{\\phi}^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\cos \\phi \\mathbf{1} +\n                (1 - \\cos \\phi) \\mathbf{a}\\mathbf{a}^T +\n                \\sin \\phi \\mathbf{a}^\\wedge, & \\text{otherwise}\n            \\end{cases}\n\n        This is the inverse operation to :meth:`~liegroups.SO3.log`.\n        '
    if (len(phi) != cls.dof):
        raise ValueError('phi must have length 3')
    angle = np.linalg.norm(phi)
    if np.isclose(angle, 0.0):
        return cls((np.identity(cls.dim) + cls.wedge(phi)))
    axis = (phi / angle)
    s = np.sin(angle)
    c = np.cos(angle)
    return cls((((c * np.identity(cls.dim)) + ((1 - c) * np.outer(axis, axis))) + (s * cls.wedge(axis))))

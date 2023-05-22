import numpy as np
from . import _base


@classmethod
def inv_left_jacobian(cls, phi):
    ':math:`SO(2)` inverse left Jacobian.\n\n        .. math::\n            \\mathbf{J}^{-1}(\\phi) = \n            \\begin{cases}\n                \\mathbf{1} - \\frac{1}{2} \\phi^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\frac{\\phi}{2} \\cot \\frac{\\phi}{2} \\mathbf{1} -\n                \\frac{\\phi}{2} 1^\\wedge, & \\text{otherwise}\n            \\end{cases}\n        '
    if np.isclose(phi, 0.0):
        return (np.identity(cls.dim) - (0.5 * cls.wedge(phi)))
    half_angle = (0.5 * phi)
    cot_half_angle = (1.0 / np.tan(half_angle))
    return (((half_angle * cot_half_angle) * np.identity(cls.dim)) - (half_angle * cls.wedge(1.0)))

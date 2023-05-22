import numpy as np
from . import _base


@classmethod
def inv_left_jacobian(cls, phi):
    ':math:`SO(3)` inverse left Jacobian.\n\n        .. math::\n            \\mathbf{J}^{-1}(\\boldsymbol{\\phi}) =\n            \\begin{cases}\n                \\mathbf{1} - \\frac{1}{2} \\boldsymbol{\\phi}^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\frac{\\phi}{2} \\cot \\frac{\\phi}{2} \\mathbf{1} +\n                \\left( 1 - \\frac{\\phi}{2} \\cot \\frac{\\phi}{2} \\right) \\mathbf{a}\\mathbf{a}^T -\n                \\frac{\\phi}{2} \\mathbf{a}^\\wedge, & \\text{otherwise}\n            \\end{cases}\n        '
    if (len(phi) != cls.dof):
        raise ValueError('phi must have length 3')
    angle = np.linalg.norm(phi)
    if np.isclose(angle, 0.0):
        return (np.identity(cls.dof) - (0.5 * cls.wedge(phi)))
    axis = (phi / angle)
    half_angle = (0.5 * angle)
    cot_half_angle = (1.0 / np.tan(half_angle))
    return ((((half_angle * cot_half_angle) * np.identity(cls.dof)) + ((1 - (half_angle * cot_half_angle)) * np.outer(axis, axis))) - (half_angle * cls.wedge(axis)))

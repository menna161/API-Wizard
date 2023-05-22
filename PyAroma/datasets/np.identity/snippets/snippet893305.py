import numpy as np
from . import _base


@classmethod
def left_jacobian(cls, phi):
    ':math:`SO(3)` left Jacobian.\n\n        .. math::\n            \\mathbf{J}(\\boldsymbol{\\phi}) =\n            \\begin{cases}\n                \\mathbf{1} + \\frac{1}{2} \\boldsymbol{\\phi}^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\frac{\\sin \\phi}{\\phi} \\mathbf{1} +\n                \\left(1 - \\frac{\\sin \\phi}{\\phi} \\right) \\mathbf{a}\\mathbf{a}^T +\n                \\frac{1 - \\cos \\phi}{\\phi} \\mathbf{a}^\\wedge, & \\text{otherwise}\n            \\end{cases}\n        '
    if (len(phi) != cls.dof):
        raise ValueError('phi must have length 3')
    angle = np.linalg.norm(phi)
    if np.isclose(angle, 0.0):
        return (np.identity(cls.dof) + (0.5 * cls.wedge(phi)))
    axis = (phi / angle)
    s = np.sin(angle)
    c = np.cos(angle)
    return ((((s / angle) * np.identity(cls.dof)) + ((1 - (s / angle)) * np.outer(axis, axis))) + (((1 - c) / angle) * cls.wedge(axis)))

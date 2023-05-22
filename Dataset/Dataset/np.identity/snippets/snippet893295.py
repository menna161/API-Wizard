import numpy as np
from . import _base


@classmethod
def left_jacobian(cls, phi):
    ':math:`SO(2)` left Jacobian.\n\n        .. math::\n            \\mathbf{J}(\\phi) = \n            \\begin{cases}\n                \\mathbf{1} + \\frac{1}{2} \\phi^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\frac{\\sin \\phi}{\\phi} \\mathbf{1} - \n                \\frac{1 - \\cos \\phi}{\\phi} 1^\\wedge, & \\text{otherwise}\n            \\end{cases}\n        '
    if np.isclose(phi, 0.0):
        return (np.identity(cls.dim) + (0.5 * cls.wedge(phi)))
    s = np.sin(phi)
    c = np.cos(phi)
    return (((s / phi) * np.identity(cls.dim)) + (((1 - c) / phi) * cls.wedge(1.0)))

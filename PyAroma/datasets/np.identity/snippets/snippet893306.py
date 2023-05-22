import numpy as np
from . import _base


def log(self):
    'Logarithmic map for :math:`SO(3)`, which computes a tangent vector from a transformation:\n\n        .. math::\n            \\phi &= \\frac{1}{2} \\left( \\mathrm{Tr}(\\mathbf{C}) - 1 \\right) \\\\\n            \\boldsymbol{\\phi}(\\mathbf{C}) &= \n            \\ln(\\mathbf{C})^\\vee =\n            \\begin{cases}\n                \\mathbf{1} - \\boldsymbol{\\phi}^\\wedge, & \\text{if } \\phi \\text{ is small} \\\\\n                \\left( \\frac{1}{2} \\frac{\\phi}{\\sin \\phi} \\left( \\mathbf{C} - \\mathbf{C}^T \\right) \\right)^\\vee, & \\text{otherwise}\n            \\end{cases}\n\n        This is the inverse operation to :meth:`~liegroups.SO3.log`.\n        '
    cos_angle = ((0.5 * np.trace(self.mat)) - 0.5)
    cos_angle = np.clip(cos_angle, (- 1.0), 1.0)
    angle = np.arccos(cos_angle)
    if np.isclose(angle, 0.0):
        return self.vee((self.mat - np.identity(3)))
    return self.vee((((0.5 * angle) / np.sin(angle)) * (self.mat - self.mat.T)))

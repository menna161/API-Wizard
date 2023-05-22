import numpy as np
from . import _base
from .so3 import SO3Matrix


@classmethod
def left_jacobian(cls, xi):
    ':math:`SE(3)` left Jacobian.\n\n        .. math::\n            \\mathcal{J}(\\boldsymbol{\\xi}) = \n            \\begin{bmatrix}\n                \\mathbf{J} & \\mathbf{Q} \\\\\n                \\mathbf{0} & \\mathbf{J}\n            \\end{bmatrix}\n\n        with :math:`\\mathbf{J}` as in :meth:`liegroups.SO3.left_jacobian` and :math:`\\mathbf{Q}` as in :meth:`~liegroups.SE3.left_jacobian_Q_matrix`.\n        '
    rho = xi[0:3]
    phi = xi[3:6]
    if np.isclose(np.linalg.norm(phi), 0.0):
        return (np.identity(cls.dof) + (0.5 * cls.curlywedge(xi)))
    so3_jac = cls.RotationType.left_jacobian(phi)
    Q_mat = cls.left_jacobian_Q_matrix(xi)
    jac = np.zeros([cls.dof, cls.dof])
    jac[(0:3, 0:3)] = so3_jac
    jac[(0:3, 3:6)] = Q_mat
    jac[(3:6, 3:6)] = so3_jac
    return jac

import numpy as np
from numpy.linalg import inv, norm
import matplotlib.pyplot as plt


def L_curve(A, y, visible=None):
    "\n    Minimize the Lagrangian L(x,lambda) = || A*x - y||**2 + lambda*||x||**2 based on the idea of Tikhonov Regularization.\n    This program is used to accurately estimate the parameters x and the Lagrange multiplier lambda. \n    The final Lagrange multiplier is determained by the L-curve method. The L-curve can be visualized by outputing an image.\n\n    Usage:\n    accu_lamb,accu_x = L_curve(A,y) \n\n    Inputs:\n    A -> [float 2d array] Design matrix\n    y -> [float array] Measurements\n\n    Parameters:\n    visible -> [optional, str, default = None] If None, the visualization of L-vurve will be closed. If 'visible', the L-curve will be visualized by outputing an image.\n    \n    Outputs:\n    accu_lamb -> [float] Lagrange multiplier\n    accu_x -> [float array] Estimated parameters\n    \n    For more information, please refer to \n    (1) [NumPy/SciPy Recipes for Data Science: Regularized Least Squares Optimization](https://www.researchgate.net/publication/274138835_NumPy_SciPy_Recipes_for_Data_Science_Regularized_Least_Squares_Optimization)\n    (2) [Choosing the Regularization Parameter](http://www2.compute.dtu.dk/~pcha/DIP/chap5.pdf)\n    "
    m = A.shape[1]
    (appr_lamb, appr_x, log10_residual_norm, log10_solution_norm, appr_curvature) = solve_lambda_x(A, y)
    lambs_exponent = np.linspace((np.log10(appr_lamb) - 2), (np.log10(appr_lamb) + 2), 2000)
    (accu_lamb, accu_x, log10_residual_norm, log10_solution_norm, accu_curvature) = solve_lambda_x(A, y, lambs_exponent)
    if (visible is not None):
        fig_dir = 'figures/'
        if (not os.path.exists(fig_dir)):
            os.makedirs(fig_dir)
        plt.clf()
        (fig, (ax1, ax2)) = plt.subplots(1, 2, dpi=200)
        fig.subplots_adjust(wspace=0.4)
        ax1.plot(log10_residual_norm, log10_solution_norm)
        ax1.set_xlabel('$\\log \\parallel A x_{\\lambda}-y \\parallel_2$')
        ax1.set_ylabel('$\\log \\parallel x_{\\lambda} \\parallel_2$')
        ax1.set_title('L-Curve')
        ax2.plot(lambs_exponent, accu_curvature)
        ax2.set_xlabel('$\\log \\parallel \\lambda \\parallel_2$')
        ax2.set_ylabel('Curvature')
        ax2.set_title('curvature of L-Curve')
        plt.savefig((fig_dir + 'L-Curve.png'))
    return (accu_lamb, accu_x)

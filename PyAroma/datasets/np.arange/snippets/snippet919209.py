


def func(x, a0, a1):
    '\n    Define a linear function f(x) = a0 + a1/T*x to be fitted, where a0 and a1 are parameters for intercept and slope.\n\n    Usage:\n    y = func(x,a0,a1)\n\n    Inputs:\n    x -> [float array] Independent variables\n    a0 -> [float] Intercept\n    a1 -> [float] Slope\n\n    Outputs:\n    y -> [float array] Dependent variables\n\n    Examples:\n    >>> import numpy as np\n    >>> xs = np.arange(0,120,12)\n    >>> a0,a1 = 1,2\n    >>> ys = func(xs,a0,a1)\n    >>> print(xs)\n    [  0  12  24  36  48  60  72  84  96 108]\n    >>> print(ys)\n    [ 1.  3.  5.  7.  9. 11. 13. 15. 17. 19.]\n    '
    T = 12
    return (a0 + ((a1 / T) * x))

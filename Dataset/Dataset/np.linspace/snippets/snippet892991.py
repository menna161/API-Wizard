import numpy as np


def convDownsampleKernel(kernelName, dimension, kernelSize, a=(- 0.5), b=(1 / 3), c=(1 / 3), normalizeKernel=None):
    numOfPoints = (kernelSize + 2)
    XInput = np.linspace((- 2), 2, num=numOfPoints)
    if (dimension == 1):
        if (kernelName == 'linear'):
            Y = np.stack([linear1d(XInput[i]) for i in range(0, len(XInput))])
        elif (kernelName == 'spline'):
            Y = np.stack([spline1D(XInput[i], a=a) for i in range(0, len(XInput))])
        elif (kernelName == 'bspline'):
            Y = np.stack([bspline1D(XInput[i]) for i in range(0, len(XInput))])
        elif (kernelName == 'mitchell'):
            Y = np.stack([bspline1D(XInput[i]) for i in range(0, len(XInput))])
        else:
            raise ValueError((('cannot find the  kernel ' + kernelName) + ' !'))
        Y = Y[1:(- 1)]
    if (dimension == 2):
        YInput = np.linspace((- 2), 2, num=numOfPoints)
        (xv, yv) = np.meshgrid(XInput, YInput)
        if (kernelName == 'linear'):
            Y = np.stack([linear2d(xv[(i, j)], yv[(i, j)]) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0])])
        if (kernelName == 'spline'):
            Y = np.stack([spline2D(xv[(i, j)], yv[(i, j)], a=a) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0])])
        if (kernelName == 'bspline'):
            Y = np.stack([bspline2D(xv[(i, j)], yv[(i, j)]) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0])])
        Y = np.reshape(Y, [len(XInput), len(XInput)])
        Y = Y[(1:(- 1), 1:(- 1))]
    if (dimension == 3):
        YInput = np.linspace((- 2), 2, num=numOfPoints)
        ZInput = np.linspace((- 2), 2, num=numOfPoints)
        (xv, yv, zv) = np.meshgrid(XInput, YInput, ZInput)
        if (kernelName == 'linear'):
            Y = np.stack([linear3d(xv[(i, j, k)], yv[(i, j, k)], zv[(i, j, k)]) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0]) for k in range(0, np.shape(xv)[0])])
        if (kernelName == 'spline'):
            Y = np.stack([spline3D(xv[(i, j, k)], yv[(i, j, k)], zv[(i, j, k)], a=a) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0]) for k in range(0, np.shape(xv)[0])])
        if (kernelName == 'bspline'):
            Y = np.stack([bspline3D(xv[(i, j, k)], yv[(i, j, k)], zv[(i, j, k)]) for i in range(0, np.shape(xv)[0]) for j in range(0, np.shape(xv)[0]) for k in range(0, np.shape(xv)[0])])
        Y = np.reshape(Y, [len(XInput), len(XInput), len(XInput)])
        Y = Y[(1:(- 1), 1:(- 1), 1:(- 1))]
    if normalizeKernel:
        if (np.sum(Y) != normalizeKernel):
            ratio = (normalizeKernel / np.sum(Y))
            Y = (ratio * Y)
    Y[(abs(Y) < 1e-06)] = 0
    return Y.astype(np.float32)

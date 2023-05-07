import numpy as np
import random
import copy


def fkl(angles, parent, offset, rotInd, expmapInd):
    njoints = 32
    xyzStruct = [dict() for x in range(njoints)]
    for i in np.arange(njoints):
        if (not rotInd[i]):
            (xangle, yangle, zangle) = (0, 0, 0)
        else:
            xangle = angles[(rotInd[i][0] - 1)]
            yangle = angles[(rotInd[i][1] - 1)]
            zangle = angles[(rotInd[i][2] - 1)]
        r = angles[expmapInd[i]]
        thisRotation = expmap2rotmat(r)
        thisPosition = np.array([xangle, yangle, zangle])
        if (parent[i] == (- 1)):
            xyzStruct[i]['rotation'] = thisRotation
            xyzStruct[i]['xyz'] = (np.reshape(offset[(i, :)], (1, 3)) + thisPosition)
        else:
            xyzStruct[i]['xyz'] = ((offset[(i, :)] + thisPosition).dot(xyzStruct[parent[i]]['rotation']) + xyzStruct[parent[i]]['xyz'])
            xyzStruct[i]['rotation'] = thisRotation.dot(xyzStruct[parent[i]]['rotation'])
    xyz = [xyzStruct[i]['xyz'] for i in range(njoints)]
    xyz = np.array(xyz).squeeze()
    xyz = xyz[(:, [0, 2, 1])]
    return np.reshape(xyz, [(- 1)])

import numpy as np
import copy
from .ann import getLayer, getNodeOrder


def mutAddNode(self, connG, nodeG, innov, gen, p):
    'Add new node to genome\n\n    Args:\n      connG    - (np_array) - connection genes\n                 [5 X nUniqueGenes] \n                 [0,:] == Innovation Number (unique Id)\n                 [1,:] == Source Node Id\n                 [2,:] == Destination Node Id\n                 [3,:] == Weight Value\n                 [4,:] == Enabled?  \n      nodeG    - (np_array) - node genes\n                 [3 X nUniqueGenes]\n                 [0,:] == Node Id\n                 [1,:] == Type (1=input, 2=output 3=hidden 4=bias)\n                 [2,:] == Activation function (as int)\n      innov    - (np_array) - innovation record\n                 [5 X nUniqueGenes]\n                 [0,:] == Innovation Number\n                 [1,:] == Source\n                 [2,:] == Destination\n                 [3,:] == New Node?\n                 [4,:] == Generation evolved\n      gen      - (int)      - current generation\n      p        - (dict)     - algorithm hyperparameters (see p/hypkey.txt)\n\n    Returns:\n      connG    - (np_array) - updated connection genes\n      nodeG    - (np_array) - updated node genes\n      innov    - (np_array) - updated innovation record\n\n    '
    if (innov is None):
        newNodeId = int(max((nodeG[(0, :)] + 1)))
        newConnId = (connG[(0, (- 1))] + 1)
    else:
        newNodeId = int((max(innov[(2, :)]) + 1))
        newConnId = (innov[(0, (- 1))] + 1)
    connActive = np.where((connG[(4, :)] == 1))[0]
    if (len(connActive) < 1):
        return (connG, nodeG, innov)
    connSplit = connActive[np.random.randint(len(connActive))]
    newActivation = p['ann_actRange'][np.random.randint(len(p['ann_actRange']))]
    newNode = np.array([[newNodeId, 3, newActivation]]).T
    connTo = connG[(:, connSplit)].copy()
    connTo[0] = newConnId
    connTo[2] = newNodeId
    connTo[3] = 1
    connFrom = connG[(:, connSplit)].copy()
    connFrom[0] = (newConnId + 1)
    connFrom[1] = newNodeId
    connFrom[3] = connG[(3, connSplit)]
    newConns = np.vstack((connTo, connFrom)).T
    connG[(4, connSplit)] = 0
    if (innov is not None):
        newInnov = np.empty((5, 2))
        newInnov[(:, 0)] = np.hstack((connTo[0:3], newNodeId, gen))
        newInnov[(:, 1)] = np.hstack((connFrom[0:3], (- 1), gen))
        innov = np.hstack((innov, newInnov))
    nodeG = np.hstack((nodeG, newNode))
    connG = np.hstack((connG, newConns))
    return (connG, nodeG, innov)

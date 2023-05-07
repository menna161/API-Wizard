import numpy as np
import itertools
from .ind import Ind, getLayer, getNodeOrder


def topoMutate(self, child, innov, gen):
    'Randomly alter topology of individual\n  Note: This operator forces precisely ONE topological change \n\n  Args:\n    child    - (Ind) - individual to be mutated\n      .conns - (np_array) - connection genes\n               [5 X nUniqueGenes] \n               [0,:] == Innovation Number (unique Id)\n               [1,:] == Source Node Id\n               [2,:] == Destination Node Id\n               [3,:] == Weight Value\n               [4,:] == Enabled?  \n      .nodes - (np_array) - node genes\n               [3 X nUniqueGenes]\n               [0,:] == Node Id\n               [1,:] == Type (1=input, 2=output 3=hidden 4=bias)\n               [2,:] == Activation function (as int)\n    innov    - (np_array) - innovation record\n               [5 X nUniqueGenes]\n               [0,:] == Innovation Number\n               [1,:] == Source\n               [2,:] == Destination\n               [3,:] == New Node?\n               [4,:] == Generation evolved\n\n  Returns:\n      child   - (Ind)      - newly created individual\n      innov   - (np_array) - innovation record\n\n  '
    p = self.p
    nConn = np.shape(child.conn)[1]
    connG = np.copy(child.conn)
    nodeG = np.copy(child.node)
    topoRoulette = np.array((p['prob_addConn'], p['prob_addNode'], p['prob_enable'], p['prob_mutAct']))
    spin = (np.random.rand() * np.sum(topoRoulette))
    slot = topoRoulette[0]
    choice = topoRoulette.size
    for i in range(1, topoRoulette.size):
        if (spin < slot):
            choice = i
            break
        else:
            slot += topoRoulette[i]
    if (choice is 1):
        (connG, innov) = self.mutAddConn(connG, nodeG, innov, gen)
    elif (choice is 2):
        (connG, nodeG, innov) = self.mutAddNode(connG, nodeG, innov, gen)
    elif (choice is 3):
        disabled = np.where((connG[(4, :)] == 0))[0]
        if (len(disabled) > 0):
            enable = np.random.randint(len(disabled))
            connG[(4, disabled[enable])] = 1
    elif (choice is 4):
        start = ((1 + child.nInput) + child.nOutput)
        end = nodeG.shape[1]
        if (start != end):
            mutNode = np.random.randint(start, end)
            newActPool = listXor([int(nodeG[(2, mutNode)])], list(p['ann_actRange']))
            nodeG[(2, mutNode)] = int(newActPool[np.random.randint(len(newActPool))])
    child.conn = connG
    child.node = nodeG
    child.birth = gen
    return (child, innov)

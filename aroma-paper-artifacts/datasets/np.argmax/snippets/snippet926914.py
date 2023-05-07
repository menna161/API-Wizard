import numpy as np


def selectAct(action, actSelect):
    if (actSelect == 'hard'):
        action = np.argmax(np.sum(action, axis=0), axis=0)
    elif (actSelect == 'softmax'):
        action = softmax(action)
    elif (actSelect == 'prob'):
        action = weightedRandom(np.sum(action, axis=0))
    else:
        action = action.flatten()
    return action

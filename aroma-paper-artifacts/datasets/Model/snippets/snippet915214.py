import os
import _jsonnet
import json


def getModel(name):
    modelDir = 'logs/'
    nameDir = ((modelDir + name) + '/')
    if os.path.isdir(nameDir):
        for modelDir in reversed(os.listdir(nameDir)):
            modelPath = ((nameDir + modelDir) + '/model.pt')
            if os.path.isfile(modelPath):
                return modelPath
    return ''

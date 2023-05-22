import numpy as np
from copy import deepcopy
import time
import pickle
import pprint as pp
import torch
import torch.nn as nn
from torch.autograd import Variable
import sys, os
from AI_physicist.pytorch_net.util import to_np_array, to_Variable, filter_filename, standardize_symbolic_expression, get_coeffs, substitute
from AI_physicist.pytorch_net.net import load_model_dict
from AI_physicist.settings.global_param import PrecisionFloorLoss, COLOR_LIST, Dt
from AI_physicist.settings.filepath import theory_PATH
from sklearn.model_selection import train_test_split
import random
from AI_physicist.theory_learning.theory_model import Theory_Training
from sklearn.model_selection import train_test_split
import pandas as pd
from AI_physicist.settings.global_param import COLOR_LIST
from AI_physicist.settings.global_param import COLOR_LIST
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from operator import itemgetter
import pandas as pd
import itertools
import matplotlib.pylab as plt
import matplotlib.pylab as plt
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib
import matplotlib.pyplot as plt


def load_info_dict(exp_id, datetime, filename, exp_mode=None):
    if (exp_mode is not None):
        dirname = (theory_PATH + '/{0}_{1}_{2}/'.format(exp_id, exp_mode, datetime))
    else:
        dirname = (theory_PATH + '/{0}_{1}/'.format(exp_id, datetime))
    return pickle.load(open((dirname + filename), 'rb'))

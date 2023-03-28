import gc
from log_utils import log, timeclass
import CONSTANT
from joblib import Parallel, delayed
from .feat_opt import *
from .feat_namer import FeatNamer
from data_utils import downcast, check_density, revert_pivot_feat_join, numpy_downward_fill
from functools import partial
import time


def transform(self, table, mode='pred'):
    todo_col = table.key_time_col
    if (mode == 'train'):
        df = table.train_X
    elif (mode == 'pred'):
        df = table.pred_X
    col2type = {}
    new_cols = []
    opt = time_atr
    for atr in self.attrs:
        obj = todo_col
        param = atr
        new_col = FeatNamer.gen_feat_name(self.__class__.__name__, obj, param, CONSTANT.CATEGORY_TYPE)
        new_cols.append(new_col)
        col2type[new_col] = CONSTANT.CATEGORY_TYPE
        df[new_col] = opt(df[todo_col], atr)
    ts = df[todo_col]
    ts = pd.to_datetime(ts, unit='s')
    param = 'timestamp'
    new_col = FeatNamer.gen_feat_name(self.__class__.__name__, obj, param, CONSTANT.NUMERICAL_TYPE)
    df[new_col] = (ts.astype('int64') // (10 ** 9))
    new_cols.append(new_col)
    table.time_attr_cols = new_cols
    col2type[new_col] = CONSTANT.NUMERICAL_TYPE
    table.update_data(df, col2type, mode)

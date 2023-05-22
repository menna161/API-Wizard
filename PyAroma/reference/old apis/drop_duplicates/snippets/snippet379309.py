import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from log_utils import log, timeclass
from data_utils import downcast
import CONSTANT


def fit(self, ss):
    cats = ss.dropna().drop_duplicates().values
    if (len(self.cats) == 0):
        self.cats = sorted(list(cats))
    else:
        added_cats = sorted((set(cats) - set(self.cats)))
        self.cats.extend(added_cats)

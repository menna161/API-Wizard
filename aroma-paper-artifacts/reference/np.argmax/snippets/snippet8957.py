import GPy
import numpy as np
from utilities.upsampler import downsample_projection
from utilities.utilities import subset_select, subset_select_for_learning
from .base import BaseModel


def _update_model(self, X_all, Y_all_raw, itr=0):
    '\n        :param X_all: observed input data\n        :param Y_all_raw: observed output raw data\n        :param itr: BO iteration counter\n        '
    if self.normalize_Y:
        Y_all = ((Y_all_raw - Y_all_raw.mean()) / Y_all_raw.std())
        self.Y_mean = Y_all_raw.mean()
        self.Y_std = Y_all_raw.std()
    else:
        Y_all = Y_all_raw
    if self.sparse.startswith('SUB'):
        (X_all, Y_all) = subset_select(X_all, Y_all, select_metric=self.sparse)
    if ((itr % int((8 * self.update_interval))) == 0):
        if ('ADD' in self.sparse):
            print('learn the optimal dr with subset observed data')
            (X_ob, Y_ob) = subset_select_for_learning(X_all, Y_all, select_metric=self.sparse)
        else:
            (X_ob, Y_ob) = (X_all, Y_all)
        ll_list = []
        model_list = []
        for dr in self.dr_list:
            X_all_d_r = downsample_projection(self.dim_reduction, X_ob, int((dr ** 2)), self.high_dim, nchannel=self.nchannel, align_corners=True)
            model = self._create_model(X_all_d_r, Y_ob)
            ll_dr = model.log_likelihood()
            print(f'dr={dr}, ll={ll_dr}')
            ll_list.append(ll_dr)
            model_list.append(model)
        mle_idx = np.argmax(ll_list)
        self.opt_dr = int(self.dr_list[mle_idx])
        self.model = model_list[mle_idx]
        print(f'opt_dr={self.opt_dr}')
    else:
        X_all_d_r = downsample_projection(self.dim_reduction, X_all, int((self.opt_dr ** 2)), self.high_dim, nchannel=self.nchannel, align_corners=True)
        self.model.set_XY(X_all_d_r, Y_all)
    if ((itr % self.update_interval) == 0):
        self.model.optimize_restarts(num_restarts=self.optimize_restarts, optimizer=self.optimizer, max_iters=self.max_iters, verbose=self.verbose)

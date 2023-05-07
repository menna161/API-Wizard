import GPy
import numpy as np
from utilities.utilities import subset_select, subset_select_for_learning
from .base import BaseModel


def _update_model(self, X_all, Y_all_raw, itr=0):
    '\n        :param X_all: observed input data\n        :param Y_all_raw: observed output raw data\n        :param itr: BO iteration counter\n        '
    if self.normalize_Y:
        Y_all = ((Y_all_raw - Y_all_raw.mean()) / Y_all_raw.std())
    else:
        Y_all = Y_all_raw
    if self.sparse.startswith('SUB'):
        (X_all, Y_all) = subset_select(X_all, Y_all, select_metric=self.sparse)
    if (self.model is None):
        self.input_dim = X_all.shape[1]
        self.input_dim_opt_ex = list(range(self.input_dim))
    else:
        self.model.set_XY(X_all, Y_all)
    if ((itr % int((self.update_interval * 8))) == 0):
        input_dim_permutate_list = [np.random.permutation(range(self.input_dim)) for i in range(self.n_decomp)]
        input_dim_permutate_list.append(self.input_dim_opt_ex)
        if ('ADD' in self.sparse):
            print('learn the decomposition with subset observed data')
            (X_ob, Y_ob) = subset_select_for_learning(X_all, Y_all, select_metric=self.sparse)
        else:
            (X_ob, Y_ob) = (X_all, Y_all)
        ll_list = []
        submodel_list = []
        for (i, input_dim_i) in enumerate(input_dim_permutate_list):
            (sub_model_i, ll_i) = self._create_model_sub(X_ob, Y_ob, input_dim_i)
            print(f'll for decom {i} ={ll_i}')
            ll_list.append(ll_i)
            submodel_list.append(sub_model_i)
        mlh_idx = np.argmax(ll_list)
        self.model = submodel_list[mlh_idx]
        self.model.set_XY(X_all, Y_all)
        input_dim_opt = input_dim_permutate_list[mlh_idx]
        self.active_dims_list = split(input_dim_opt, self.n_sub)
        self.model_kern_list = [self.model.kern.__dict__[f'k{k_indx}'] for k_indx in range(self.n_sub)]
        self.input_dim_opt_ex = input_dim_opt.copy()
        print(f'opt_decom={mlh_idx}')
    if ((itr % self.update_interval) == 0):
        self.model.optimize_restarts(num_restarts=self.optimize_restarts, optimizer=self.optimizer, max_iters=self.max_iters, verbose=self.verbose)

import numpy as np
from sklearn import svm


def _svm(self):
    self.model = svm.SVC()
    self.model.fit(self.x_tr.T, self.y_tr)
    print(f'Optimization Finished')
    self._accuracy = self.model.score(self.x_te.T, self.y_te)

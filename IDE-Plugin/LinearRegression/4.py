import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
X_train, X_test, y_train, y_test = train_test_split(X_boson, y_boson, random_state=0)
lr = LinearRegression().fit(X_train, y_train)
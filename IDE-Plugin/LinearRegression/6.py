import numpy as np
from sklearn.linear_model import LinearRegression
x = np.array(a).reshape((-1, 1))
y = np.array(b)
model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

minmax = MinMaxScaler()
x_scaled = minmax.fit_transform(x)
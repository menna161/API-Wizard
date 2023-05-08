import pandas as pd

minmaxscalar = MinMaxScaler(feature_range=(0.1, 0.9))
data = pd.read_excel("D:/PROJECTS/weld_data.xlsx")
Y_test = data.bloc[46:53, 9:10]
X_train = minmaxscalar.fit_transform(Y_test)

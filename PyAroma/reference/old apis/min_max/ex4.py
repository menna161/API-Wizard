minmaxscalar = MinMaxScaler()
Y_train = minmaxscalar.fit_transform(Y_train.reshape(-1, 1))
Y_test = minmaxscalar.transform(Y_test.reshape(-1, 1))

from sklearn.preprocessing import MinMaxScaler

my_scalar = MinMaxScalar()
train_X_scaled = my_scalar.fit_transform(train_X)
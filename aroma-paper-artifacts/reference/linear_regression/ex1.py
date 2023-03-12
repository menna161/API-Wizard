x_training, x_testing, y_training, y_testing = train_test_split(
    x, y, test_size=1 / 3, random_state=3)
lr = LinearRegression()
regression.fit(x_training, y_training)

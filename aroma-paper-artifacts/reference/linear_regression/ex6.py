x = np.array(a).reshape((-1, 1))
y = np.array(b)
lr = LinearRegression().fit(x, y)
r_sq = model.score(x, y)

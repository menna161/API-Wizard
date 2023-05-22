X = [[-2, -1], [-1, -1], [-1, -2], [1, 1], [1, 2], [2, 1]]
y = [1, 1, 1, 1, 1, 1]

clf = tree.DecisionTreeClassifier().fit(X, y)
assert_array_equal(clf.predict(X), y)

clf = tree.DecisionTreeRegressor().fit(X, y)
assert_array_equal(clf.predict(X), y)

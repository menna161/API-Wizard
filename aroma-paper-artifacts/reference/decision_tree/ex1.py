clf = tree.DecisionTreeClassifier()
clf.fit(X, y)
assert_array_equal(clf.predict(T), true_result)

clf = tree.DecisionTreeClassifier(max_features=1, random_state=1)
clf.fit(X, y)
assert_array_equal(clf.predict(T), true_result)

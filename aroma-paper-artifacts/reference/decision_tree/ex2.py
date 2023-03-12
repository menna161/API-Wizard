clf = tree.DecisionTreeClassifier()
clf.fit(X, y, sample_weight=np.ones(len(X)))
assert_array_equal(clf.predict(T), true_result)

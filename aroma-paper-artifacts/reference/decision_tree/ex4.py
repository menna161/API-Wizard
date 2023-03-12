Xf = np.asfortranarray(X)
clf = tree.DecisionTreeClassifier()
clf.fit(Xf, y)
assert_array_equal(clf.predict(T), true_result)

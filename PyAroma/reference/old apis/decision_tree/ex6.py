clf = tree.DecisionTreeClassifier(compute_importances=True)
clf.fit(X, y)
importances = clf.feature_importances_
n_important = sum(importances > 0.1)
clf = tree.DecisionTreeClassifier()
clf.fit(X, y)
assert_true(clf.feature_importances_ is None)

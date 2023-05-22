for c in ('gini',   'entropy'):
    clf = tree.DecisionTreeClassifier(criterion=c).fit(iris.data, iris.target)

    score = np.mean(clf.predict(iris.data) == iris.target)
    assert score > 0.9, "Failed with criterion " + c + \
        " and score = " + str(score)

    clf = tree.DecisionTreeClassifier(criterion=c,
                                      max_features=2,
                                      random_state=1).fit(iris.data,
                                                          iris.target)

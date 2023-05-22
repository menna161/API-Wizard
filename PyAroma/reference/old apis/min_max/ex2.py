minmaxscalar = MinMaxScaler(feature_range=(0, 10))
col = dataFile.columns
result = minmaxscalar.fit_transform(dataFile)
minMaxScalarFrame = pd.DataFrame(result, columns=col)

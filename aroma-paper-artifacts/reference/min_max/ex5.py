minmaxscalar = MinMaxScaler()
data[categorical_cols] = minmaxscalar.fit_transform(categorical_data)
data.to_csv("/content/Output/processedData.csv", index=False)

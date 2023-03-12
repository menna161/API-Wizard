Df = pd.read_csv("EastWestAirlines.csv")
minmaxscalar = MinMaxScaler()
x_scaled = minmaxscalar.fit_transform(Df)
df_normalized = pd.DataFrame(x_scaled)

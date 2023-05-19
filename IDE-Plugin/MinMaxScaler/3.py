# example of a normalization
from sklearn.preprocessing import MinMaxScaler

# define min max scaler
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)
print(scaled)
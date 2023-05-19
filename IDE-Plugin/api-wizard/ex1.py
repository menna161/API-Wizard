import pandas as pd
from sklearn.preprocessing import MinMaxScaler


df = pd.read_pickle('data.pkl')


df = pd.DataFrame(df)

# Create an instance of MinMaxScaler
scaler = MinMaxScaler()

# Scale the data
scaled_data = scaler.fit_transform(df)

# Print the scaled data
print("Scaled Data:")
print(scaled_data)

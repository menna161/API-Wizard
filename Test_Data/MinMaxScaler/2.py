from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(data)    
print(scaler.transform([[2, 2]]))
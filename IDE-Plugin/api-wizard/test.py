import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

# Example data
X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
y_train = np.array([10, 20, 30])
X_test = np.array([[2, 4, 6], [8, 10, 12]])

# scale the data
# MinMaxScaler
scaler = MinMaxScaler()
train_X_scaled = scaler.fit_transform(X_train)
test_X_scaled = scaler.fit_transform(X_test)

# train linear regression model
# LinearRegression
model = LinearRegression().fit(train_X_scaled, y_train)

# Predict using the trained model
y_pred = model.predict(test_X_scaled)


# Print the results
print("Scaled X_train:")
print(train_X_scaled)
print("Scaled X_test:")
print(test_X_scaled)
print("Predicted y:")
print(y_pred)

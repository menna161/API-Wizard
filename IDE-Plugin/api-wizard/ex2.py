import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

# Example data
X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
y_train = np.array([10, 20, 30])
X_test = np.array([[2, 4, 6], [8, 10, 12]])

# Scale the data using MinMaxScaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Predict using the trained model
y_pred = model.predict(X_test_scaled)

# Inverse transform the scaled data
X_test_inverse = scaler.inverse_transform(X_test_scaled)

# Print the results
print("Scaled X_train:")
print(X_train_scaled)
print("Scaled X_test:")
print(X_test_scaled)
print("Inverse transformed X_test:")
print(X_test_inverse)
print("Predicted y:")
print(y_pred)

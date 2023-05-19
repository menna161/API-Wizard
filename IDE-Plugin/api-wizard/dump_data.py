import pandas as pd
import pickle

# Create sample data
data = {
    'feature1': [10, 20, 30, 40, 50],
    'feature2': [5, 15, 25, 35, 45],
    'target': [0, 0, 1, 1, 1]
}

# Save data to .pkl file
with open('data.pkl', 'wb') as file:
    pickle.dump(data, file)

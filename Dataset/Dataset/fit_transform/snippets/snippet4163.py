import pandas as pd
from sklearn.preprocessing import LabelEncoder

if (__name__ == '__main__'):
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [6, 6, 5]})
    print(df)
    MultiColumnLabelEncoder(columns=['a', 'b']).fit_transform(df)
    test = df.apply(LabelEncoder().fit_transform)
    print(test)

import pandas as pd

result = df.drop_duplicates("A")
expected = df.iloc[[0, 2, 3, 5, 7]]
tm.assert_frame_equal(result, expected)
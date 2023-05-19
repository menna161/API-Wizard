import pandas as pd

df = DataFrame({"x": [7, 6, 3, 3, 4, 8, 0], "y": [0, 6, 5, 5, 9, 1, 2]})
expected = df.loc[df.index != 3]
tm.assert_frame_equal(df.drop_duplicates(), expected)
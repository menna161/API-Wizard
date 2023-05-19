import pandas as pd
 
df = DataFrame({"A": [0, 0, 1], "B": [0, 0, 1], "C": [0, 0, 1]})
msg = re.escape("Index(['a'], dtype='object')")

with pytest.raises(KeyError, match=msg):
    df.drop_duplicates(subset)
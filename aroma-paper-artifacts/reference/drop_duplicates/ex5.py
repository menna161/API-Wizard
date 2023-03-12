df = DataFrame({'A': [0, 0, 1],
                'B': [0, 0, 1],
                'C': [0, 0, 1]})

with pytest.raises(KeyError):
    df.duplicated(subset)

with pytest.raises(KeyError):
    df.drop_duplicates(subset)

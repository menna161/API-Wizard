with pytest.raises(KeyError, match=msg):
    df.drop(labels, level=level)
tm.assert_series_equal(s, expected_s)
expected_df = df.drop(labels, level=level, errors="ignore")
tm.assert_frame_equal(df, expected_df)

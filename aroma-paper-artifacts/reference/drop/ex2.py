expected_df = df.drop(labels, level=level, errors="ignore")
tm.assert_frame_equal(df, expected_df)

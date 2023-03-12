result = df.drop_duplicates("AAA", keep="last")
expected = df.loc[[6, 7]]
tm.assert_frame_equal(result, expected)

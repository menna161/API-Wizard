result = df.drop_duplicates("AAA")
expected = df[:2]
tm.assert_frame_equal(result, expected)

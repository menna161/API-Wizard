for i in range(0, len(files)):
    final_df = pandas.read_csv(files[i]).head(0)
    final_df = final_df.drop(final_df.filter(like='_INT').columns, 1)
    final_df = final_df.drop(final_df.filter(like='_RAW').columns, 1)

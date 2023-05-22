df = set_index(best_seller_dict)
df = drop_wrong_item(df)
l2 = df.columns.values.tolist()
if len(df.iloc[0]) == 41:
    df.drop("sherry", axis=1, inplace=True)
    df.drop("sugar", axis=1, inplace=True)

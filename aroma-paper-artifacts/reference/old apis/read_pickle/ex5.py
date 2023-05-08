def get_pctd(date, count=1):
    df = pd.read_pickle('../data/factors/pctd'+str(count)+'.pkl')
    return df.loc[date].sort_values().index.tolist()


def get_pctd60_rank(date):
    rd = pd.read_pickle('../data/factors/pctd60_rank.pkl')

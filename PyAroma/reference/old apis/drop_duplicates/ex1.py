def remove_spikes(df):
    df.drop(df[df['Proton_Np_moment'] >= 99998].index, inplace=True)
    df.drop(df[df['Proton_Np_nonlin'] >= 99998].index, inplace=True)
    df.drop(df[df['Proton_VX_moment'] >= 99998].index, inplace=True)

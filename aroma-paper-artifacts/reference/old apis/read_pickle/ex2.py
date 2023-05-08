first_part2 = clean_name2[:-14]
if first_part == first_part2:
    rd = pd.read_pickle('./test/'+file2)
    frame_dfs_names.append(file2)
    rd = pd.read_pickle('./test/'+file)
    annots_dfs.append(annotation)

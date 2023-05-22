

#this function obtain the max variable names that were matched after calculating their scores
def get_var_names(snippets_scores, snippet_num):
    vars=[]
    placeholder_dict = snippets_scores.get(snippet_num, {})
    for placeholder in placeholder_dict.values():
        for sub_key in placeholder.keys():
            vars.append(sub_key)
    return vars
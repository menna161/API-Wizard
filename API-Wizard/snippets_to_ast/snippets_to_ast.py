"""#Code Snippets to AST trees"""


def snippets_to_ast(ex):
    trees = []
    for index, e in enumerate(ex):
        try:
            trees.append(ast.parse(e))
        except:
            # print('failed to convert code to ast ', index)
            pass

    # for tree in trees:
    #     dumps.append(ast.dump(tree))
    print('converted trees: ', len(trees))
    input_count = len(trees)
    return input_count, trees

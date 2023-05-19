import globals
import ast

def snippets_to_ast(ex):
    for index,e in enumerate(ex):
      try:
        globals.trees.append(ast.parse(e))
      except:
        pass


    print('Converted Code Snippets to AST Trees Succesfully')
    input_count =  len(globals.trees)
    return input_count, globals.trees
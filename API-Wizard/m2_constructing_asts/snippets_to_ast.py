import globals
import ast


#This fucntion converts the code snippets taken as input (ex) to asts
#returns the ast trees and their count
def snippets_to_ast(ex):
    # Iterate over each code snippet in the 'ex' list
    for index, e in enumerate(ex):
        try:
            # Parse the code snippet and append the resulting AST tree to the 'trees' list in the 'globals' module
            globals.trees.append(ast.parse(e))
        except:
            # If there is an error parsing the code snippet, move to the next one
            pass

    # Print a success message
    print('Converted Code Snippets to AST Trees Succesfully')


    # Calculate the number of inputs (AST trees)
    input_count = len(globals.trees)

    # Return the input count and the 'trees' list
    return input_count, globals.trees

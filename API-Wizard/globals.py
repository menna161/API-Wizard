ex = [] #filtered code examples in the dataset
trees = [] #ast trees of the filtered code examples
input_count = 0
# dumps = [] 
extracted_subgraphs = [] #Gspan format of all output patterns
# frequent_subgraphs = [] # final frequent subgraphs after processing (removing subgraphs and meaningless trees) gspan format
where_code_output = [] # array of the source of each pattern# lg_v = {}
# sm_v = {}

code_output = [] # pattern output code with placeholder 
code_output_ast = [] # pattern output ast tree with placeholder 

score = {} #to store trees scores 
import ast
import re


#This Function traverses each ast tree and convert it to the gsapn format

#gspan format:
# t # 0
# v 0 vertex name
# v 1 vertex name
# e 0 1 edge label

#takes ast trees as input and the file name we want the results to be stored in
#include_vars=False , means that the variable/parameter names will not appear

def ast_to_gspan(filename ,trees, include_vars=False):
  # Open the specified file in write mode
  file = open(filename, "w")
  i=0


  for snippet_tree in trees:
    v_write = []
    e_write = []
    v_n = 0
    parent_n = -1
    file.write(f't # {i}\n')
    i+=1
    first = True

    # Traverse the AST tree nodes
    for node in ast.walk(snippet_tree):
        n = str(node).split()[0][6:]
        parent_n += 1
        children = []
        e_n = 0
        fields =  list(ast.iter_fields(node))

        if first:
          v_write.append('v '+str(v_n)+' '+str(type(node).__name__)+'\n')
          first = False

        # Iterate over the child nodes of the current node
        for index,x in enumerate(ast.iter_child_nodes(node)): 
            child = type(x).__name__
            try:
              if(child == "ImportFrom"): 
                child = str(child)+ "#module="+ x.module;
              elif( child == 'alias'):
                child = str(child)+ "#name="+x.name
                if(x.asname is not None): child = str(child)+ "#asname="+x.asname

              elif(include_vars and child in ("FunctionDef" , "AsyncFunctionDef" ,"ClassDef")):
                child = str(child)+ "#name="+x.name
              elif(include_vars and child in ("Attribute" )):
                child = str(child)+ "#attr="+x.attr
              elif(include_vars and child in ("Name" )):
                child = str(child)+ "#id="+x.id
              elif(index < len(fields) and fields[index][0] == 'func'):
                for item,val in ast.iter_fields(x):
                  if(item in ("name","id","attr")):
                    child = str(child)+ "#"+item+"="+val
              elif(child in ('FunctionDef', 'AsyncFunctionDef', 'ClassDef')):
                child = str(child)+ "#name="+ x.name
              elif(include_vars and child == "Constant"):
                child = str(child)+ "#value="+ str(x.value).replace(" ", "").replace("\n", "")
                if x.kind is not None:
                  child = child +  "#kind="+ str(x.kind)
              elif(child == "FormattedValue"):
                child = str(child)+ "#conversion="+ str(x.conversion)
              elif(child == "AnnAssign"):
                child = str(child)+ "#simple="+ str(x.simple)
              elif(child == "ExceptHandler"):
                if(x.name is not None): child = str(child)+ "#name="+ str(x.name)
              elif(child in ("Global","Nonlocal")):
                placeholders_count = len(x.names)
                if(include_vars):
                  child = str(child)+ "#names=" + str(x.names)
                else:
                  child = str(child)+ "#names_count=" + str(placeholders_count)
              elif(child == "keyword"):
                if(x.arg is not None): child = str(child)+ "#arg="+ str(x.arg)
              elif(include_vars and child in ("arg" )):
                child = str(child)+ "#arg="+x.arg
            except:
                pass

            v_n +=1
            v_write.append('v '+str(v_n)+' '+str(child)+'\n')
            children.append([child,v_n])



        edges_list = list(ast.iter_fields(node))

        for edge in list(ast.iter_fields(node)):
                
          if(not isinstance(edge[1], ast.AST) and not isinstance(edge[1], list)):
            continue

          if len(children) > 0:
            if isinstance(edge[1], list):
              if(len(edge[1]) == 1 ):
                  try:
                    if(str(edge[0]) == 'keywords'): edge[0]='keywords0'
                    e_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                  except:
                    pass
                  e_n+=1
              else:
                edge_name_n = 0
                for node in edge[1]:
                  if isinstance(node, ast.AST):
                    e_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0]+str(edge_name_n))+'\n')
                    e_n+=1
                    edge_name_n+=1
            else :
              try:
                if(str(edge[0]) == 'keywords'): edge[0]='keywords0'
                e_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
              except:
                pass
              e_n+=1


    # Sort the vertex and edge lists based on the number after 'v' and 'e' in each string
    v_write = sorted(v_write, key=lambda x: int(re.search(r'v (\d+)', x).group(1)))
    e_write = sorted(e_write, key=lambda x: int(re.search(r'e (\d+)', x).group(1)))

    for y in v_write:
      file.write(y)
    
    for y in e_write:
      file.write(y)
          
  # Write the termination line for the gSpan format
  file.write("t # -1\n")
  file.close()
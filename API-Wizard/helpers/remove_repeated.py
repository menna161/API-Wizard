def remove_repeated(code_output):
  result = []
  for i in range(len(code_output)):
      keep = True
      for j in range(len(code_output)):
          if i != j and code_output[j].startswith(code_output[i][:-1]) :
              keep = False
              if len(code_output[j]) > len(code_output[i]):
                  # If another line starts with this line and is longer,
                  # skip to the next line in the outer loop.
                  break
      if keep:
          result.append(code_output[i])
  return result
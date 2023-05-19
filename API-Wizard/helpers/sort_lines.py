def sort_lines(code_output):
  unique_list = []
  for elem in code_output:
    if elem not in unique_list:
        unique_list.append(elem)

  return unique_list


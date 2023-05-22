

def calc_representative(where_code_output, input_count):
  repr = 0
  counts = {}

  for array in where_code_output:
      for value in array:
          if value in counts:
              counts[value] += 1
              if(counts[value] == len(where_code_output)): repr = repr+1
          else:
              counts[value] = 1
    

  max_occ = max(counts.values())

  count = 0  # Initialize a counter

  for key, value in counts.items():
      if value == max_occ:  # Check if the value is 7
          count += 1  # Increment the counter

  repr = (count/input_count)*100
  return '{:.2f}%'.format(repr)
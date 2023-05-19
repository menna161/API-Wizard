import re

def remove_placeholders(code_output):
  result = []
  for i in range(len(code_output)):
      keep = True
      if('PLACEHOLDER' in code_output[i]):
        pattern_regex = re.escape(code_output[i]).replace('PLACEHOLDER', '(.*)')
        for j in range(len(code_output)):
          matches = re.findall(pattern_regex, code_output[j])
          if matches and code_output[i] != code_output[j]:
             keep = False
             break
      if keep:
          result.append(code_output[i])
  return result
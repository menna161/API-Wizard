def calc_consiceness(code_output):
  joined_lines = ''.join(set(code_output))
  consiceness = joined_lines.count('\n')

  return consiceness
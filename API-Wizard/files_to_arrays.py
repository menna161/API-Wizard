"""#files -> arrays"""


def parse_file(filename):
    # print('parse-file',filename )
    with open(filename, 'r') as file:
        extracted_subgraphs = []
        current_string = ''
        # Loop over each line in the file
        for line in file:
            # Check if the line starts with 't'
            if line.startswith('t'):
                # If so, append the current string to the array (if it's not empty)
                if current_string:
                    extracted_subgraphs.append(current_string.strip())
                # Start a new current string
                current_string = line
            # Otherwise, append the line to the current string
            else:
                current_string += line

        # Append the last current string to the array (if it's not empty)
        if current_string:
            extracted_subgraphs.append(current_string.strip())

    # Remove the 'Support' line and dashes from each extracted string
    for i in range(len(extracted_subgraphs)):
        extracted_subgraphs[i] = '\n'.join([line for line in extracted_subgraphs[i].split(
            '\n') if not line.startswith(('Support', '-'))]).strip()

    # for s in extracted_strings:
    # print(len(extracted_subgraphs))
    return extracted_subgraphs

import os
import pandas as pd


#Function to read the snippets that conatins the api_name given as input
#Returns the list of read code snippets

def read_dir(api_name):
    # Define the directory path where the files are located
    # dir_path = '../Dataset/Dataset/' #the coreect
    # dir_path = '../../Dataset/Dataset/'
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    print('current_file_path ', current_file_path)

    # Construct the dataset directory path relative to the current file's location
    # if('API_Wizard_IDE' in current_file_path):
    dir_path = os.path.join(current_file_path, '..', '..', 'Dataset', 'Dataset', api_name, 'snippets')
    # else:
    dir_path = dir_path.replace("\\", "/")
    print('updated_path', dir_path)




    # Append the specified API name to the directory path
    # dir_path = dir_path + api_name

    # dir_path = dir_path + '/snippets/'

    # Create an empty list to store the file contents
    ex = []

    # Iterate over each file in the directory
    for file_name in os.listdir(dir_path):
        # Check if the file ends with '.py' extension
        if file_name.endswith('.py'):
            # Open the file in read mode
            with open(os.path.join(dir_path, file_name), 'r') as file:
                # Read the contents of the file
                text = file.read()
                # Append the file contents to the 'ex' list
                ex.append(text)
    
    print('Read Files Succesfully')
    
    # Return the list of file contents
    return ex

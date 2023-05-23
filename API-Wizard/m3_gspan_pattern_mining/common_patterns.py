import globals
import warnings
import os
import subprocess


#This function genrates the common patterns between the trees inside "input.txt" using gspan tool
#Min support = 50%
#Stores the patterns inside output.txt

def common_patterns():
    # Ignore warnings
    warnings.filterwarnings('ignore')
    
    # Calculate the minimum support based on the number of trees in the 'trees' list
    minsupport = int(len(globals.trees) * 0.5)
    
    # Ignore warnings for the subprocess call
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore')
        
        # Execute the gSpan mining command using the subprocess module
        os.system("python -m gspan_mining -s " + str(minsupport) + " -d True -w True ./input.txt > output.txt")
     # Execute the gSpan mining command using subprocess and redirect output/error streams
    # with open(os.devnull, 'w') as devnull:
    #     subprocess.call(["python", "-m", "gspan_mining", "-s", str(minsupport), "-d", "True", "-w", "True", "./input.txt", ">", "output.txt"], stdout=devnull)


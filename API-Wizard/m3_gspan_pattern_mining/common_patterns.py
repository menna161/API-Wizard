import globals
import warnings
import os

# def common_patterns():
#   warnings.filterwarnings('ignore')
#   minsupport = int(len(globals.trees)*0.5)

#   os.system("python -m gspan_mining -s " + str(minsupport)+" -d True -w True ./input.txt > output.txt")

def common_patterns():
    warnings.filterwarnings('ignore')
    # len_ex = len(dumps)
    minsupport = int(len(globals.trees)*0.5)
    #  -w True
    with warnings.catch_warnings():
      warnings.simplefilter(action='ignore')
      os.system(
          "python -m gspan_mining -s " + str(minsupport)+" -d True -w True ./input.txt > output.txt")

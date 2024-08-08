import time

from functions.import_BREaDS import *
from functions.export_BREaDS import *

filename = "/Users/larswiersma/Documents/Business/AECOM/BREaDS/BREaDS_Project_v1.xlsx"

tic = time.time()

df = import_inputBREaDS(filename)

export_BREaDS(filename, 
              df)

toc = time.time()
print('Simulation time is ' + str(toc-tic) + ' seconds')
import time

from functions.import_BREaDS_dataset import *
from functions.export_BREaDS_dataset import *
from functions.compute_residue import *

filename = '/Users/larswiersma/Documents/Business/AECOM/BREaDS/BREaDS_Project_v1.xlsx'

tic = time.time()

export_BREaDS_dataset(filename,
                      compute_residue(import_BREaDS_dataset(filename)))

toc = time.time()
print('Simulation time is ' + str(toc-tic) + ' seconds')
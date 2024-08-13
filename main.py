import time

from functions import import_BREaDS_dataset
from functions import export_BREaDS_dataset
from functions import compute_residue

filename = '/Users/larswiersma/Documents/Business/AECOM/BREaDS/BREaDS_Project_v1.xlsx'

tic = time.time()

export_BREaDS_dataset(filename,
                      compute_residue(import_BREaDS_dataset(filename)))

toc = time.time()
print('Simulation time is ' + str(toc-tic) + ' seconds')
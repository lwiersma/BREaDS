import time

from functions.import_BREaDS_dataset import *
from functions.export_BREaDS_dataset import *
from functions.compute_residue import *

filename = "BREaDS_ProjectName_v1.xlsx"

tic = time.time()

df, residue = compute_residue(import_BREaDS_dataset(filename))

export_BREaDS_dataset(filename, df, residue)

toc = time.time()
print("Simulation time is " + str(toc - tic) + " seconds")

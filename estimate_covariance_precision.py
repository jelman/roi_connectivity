import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd
from scipy.stats import zscore
from sklearn import covariance




#### Set parameters #######
datadir = '/home/jagust/rsfmri_ica/CPAC/connectivity/timecourses'
outdir = '/home/jagust/rsfmri_ica/CPAC/connectivity/matrices'
outname = 'Greicius_90rois_0.01_0.08'
tc_glob = 'B*_timecourses.csv'
tc_files = glob(os.path.join(datadir, tc_glob))
tc_files.sort()
###########################



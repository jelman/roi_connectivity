import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd
from scipy.stats import zscore
from sklearn import covariance


def estimate_sub(tc_array):
    estimator.fit(tc_array)
    return estimator.covariance_, estimator.precision_


def run_subject(subtc_file):
    subtc_df = pd.read_csv(subtc_file, sep=None)
    subtc_zscored = pd.DataFrame(zscore(subtc_df), columns=subtc_df.columns)
    sub_cv, sub_precision = estimate_sub(subtc_zscored)
    sub_cv1D = utils.flat_triu(sub_cv)
    sub_precision1D = utils.flat_triu(sub_precision)
    return sub_cv1D, sub_precision1D

#### Set parameters #######
datadir = '/home/jagust/rsfmri_ica/CPAC/connectivity/timecourses'
outdir = '/home/jagust/rsfmri_ica/CPAC/connectivity/matrices'
outname = 'Greicius_90rois_0.01_0.08'
tc_glob = 'B*_timecourses.csv'
tc_files = glob(os.path.join(datadir, tc_glob))
tc_files.sort()
###########################


group_cv = {}   #Create empty dataframe to hold group data
group_precision = {}   #Create empty dataframe to hold group data

for subtc_file in tc_files:
    subid = utils.get_subid(subtc_file)
    subject_order.append(subid)   
    sub_cv, sub_precision = run_subject(subtc_file)
    group_cv[subid] = sub_cv
    group_precision[subid] = sub_precision
    cv_outfile = os.path.join(outdir, ''.join(['Covariance_',outname,'.csv']))
# Search for pattern contained in list    
#[col for net in nets for col in subtc_zscored.columns if net in col]

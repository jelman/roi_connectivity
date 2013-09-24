import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd
from scipy.stats import zscore
from sklearn import covariance

def save_group_data(data_dict, outfile):
    data_df = pd.DataFrame(data_dict)
    data_df = data_df.T
    sorted_df = data_df.sort_index()
    sorted_df.to_csv(outfile, sep=',', header=False, index=False)
    return sorted_df
    

def estimate_sub(tc_array):
    estimator = covariance.GraphLassoCV(max_iter=500, verbose=True)
    estimator.fit(tc_array)
    np.fill_diagonal(estimator.covariance_, 0)
    np.fill_diagonal(estimator.precision_, 0)    
    return estimator.covariance_, estimator.precision_


def run_subject(subtc_file, tc_subset=None):
    subtc_df = pd.read_csv(subtc_file, sep=None)
    if tc_subset:
        col_subset = [col for net in tc_subset for col in subtc_df.columns if net in col]
        subtc_df = subtc_df[col_subset]
    subtc_zscored = pd.DataFrame(zscore(subtc_df), columns=subtc_df.columns)
    sub_cv, sub_precision = estimate_sub(subtc_zscored)
    sub_cv_zscored = sub_cv = np.arctanh(sub_cv)
    sub_precision_zscored = sub_cv = np.arctanh(sub_precision)
    sub_cv1D = utils.flat_triu(sub_cv_zscored)
    sub_precision1D = utils.flat_triu(sub_precision_zscored)
    return sub_cv1D, sub_precision1D



def main(datadir, outdir, outname, tc_files, tc_subset=None, subgroup=None):
    group_cv = {}   #Create empty dataframe to hold group data
    group_precision = {}   #Create empty dataframe to hold group data
    for subtc_file in tc_files:
        subid = utils.get_subid(subtc_file)
        if subgroup and subid in subgroup:
            sub_cv, sub_precision = run_subject(subtc_file, tc_subset)
            group_cv[subid] = sub_cv
            group_precision[subid] = sub_precision
        else:
            sub_cv, sub_precision = run_subject(subtc_file, tc_subset)
            group_cv[subid] = sub_cv
            group_precision[subid] = sub_precision    
    cv_outfile = os.path.join(outdir, ''.join(['Covariance_',outname,'.csv']))
    group_cv_df = save_group_data(group_cv, cv_outfile)
    precision_outfile = os.path.join(outdir, ''.join(['Precision_',outname,'.csv']))
    group_precision_df = save_group_data(group_precision, precision_outfile)
    
    
if __name__ == '__main__':


    #### Set parameters #######
    datadir = '/home/jagust/rsfmri_ica/CPAC/connectivity/timecourses/Greicius_90_rois'
    outdir = '/home/jagust/rsfmri_ica/CPAC/connectivity/matrices'
    outname = 'Greicius_90rois_0-01_0-08_subset'
    tc_glob = 'B*_timecourses.csv'
    tc_files = glob(os.path.join(datadir, tc_glob))
    tc_files.sort()
    tc_subset = None
    subgroup_file = None
    ###########################
    if subgroup_file:
        with open(subgroup_file) as f:
            subgroup = f.read().splitlines()
        
    main(datadir, outdir, outname, tc_files, subgroup=None)



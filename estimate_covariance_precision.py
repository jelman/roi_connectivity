import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd
from scipy.stats import zscore
from sklearn import covariance
from nitime.timeseries import TimeSeries
from nitime.analysis import CorrelationAnalyzer, CoherenceAnalyzer

def save_group_data(data_dict, outfile):
    data_df = pd.DataFrame(data_dict)
    data_df = data_df.T
    sorted_df = data_df.sort_index()
    sorted_df.to_csv(outfile, sep=',', header=False, index=False)
    return sorted_df
    

def estimate_cov(tc_array):
    print 'estimating covariance and precision matrices...'
    estimator = covariance.GraphLassoCV(max_iter=100, verbose=False)
    estimator.fit(tc_array)
    np.fill_diagonal(estimator.covariance_, 0)
    np.fill_diagonal(estimator.precision_, 0)    
    return estimator.covariance_, estimator.precision_
    

def estimate_corr_coh(tc_array, tr):
    print 'estimating correlation and coherence matrices...'
    TR = tr
    f_lb = 0.01
    f_ub = 0.15
    T = TimeSeries(tc_array.T, sampling_interval=TR)
    T.metadata['roi'] = tc_array.columns
    Corr = CorrelationAnalyzer(T)
    Coh = CoherenceAnalyzer(T)
    freq_idx = np.where((Coh.frequencies > f_lb) * \
                        (Coh.frequencies < f_ub))[0]
    return Corr.corrcoef, np.mean(Coh.coherence[:, :, freq_idx], -1)


def run_subject(subtc_file, tr, tc_subset=None):
    # Load data in dataframe
    subtc_df = pd.read_csv(subtc_file, sep=None)
    # Take subset of ROIs
    if tc_subset:
        col_subset = [col for net in tc_subset for col in subtc_df.columns \
                        if net in col]
        subtc_df = subtc_df[col_subset]
    # normalize time courses
    subtc_zscored = pd.DataFrame(zscore(subtc_df), columns=subtc_df.columns)
    # get covariance and precision matrices using Graph Lasso L1 penalization
    sub_cov, sub_precision = estimate_cov(subtc_zscored)
    # get correlation and coherence matrices
    sub_corr, sub_coh = estimate_corr_coh(subtc_zscored, tr)
    # zscore correlation values
    sub_cov_zscored = np.arctanh(sub_cov)
    sub_precision_zscored = np.arctanh(sub_precision)
    sub_corr_zscored = np.arctanh(sub_corr)
    # flatten upper triangle into 1D vector
    sub_cov1D = utils.flat_triu(sub_cov_zscored)
    sub_precision1D = utils.flat_triu(sub_precision_zscored)
    sub_corr1D = utils.flat_triu(sub_corr_zscored)
    sub_coh1D = utils.flat_triu(sub_coh)
    return sub_cov1D, sub_precision1D, sub_corr1D, sub_coh1D



def main(datadir, outdir, outname, tc_files, tr, tc_subset=None, subgroup=None):
    group_cov = {}   #Create empty dataframe to hold group covariance
    group_precision = {}   #Create empty dataframe to hold group precision
    group_corr = {} # Create empty dataframe to hold group correlation
    group_coh = {} # Create empty dataframe to hold group coherence
    for subtc_file in tc_files:
        subid = utils.get_subid(subtc_file)
        print 'Starting on subject %s'%(subid)
        if not subgroup:
            sub_cov, sub_precision, sub_corr, sub_coh = run_subject(subtc_file, 
                                                                    tr, 
                                                                    tc_subset)
            group_cov[subid] = sub_cov
            group_precision[subid] = sub_precision
            group_corr[subid] = sub_corr
            group_coh[subid] = sub_coh
        elif subgroup and subid in subgroup:
            sub_cov, sub_precision, sub_corr, sub_coh = run_subject(subtc_file, 
                                                                    tr, 
                                                                    tc_subset)
            group_cov[subid] = sub_cov
            group_precision[subid] = sub_precision 
            group_corr[subid] = sub_corr            
            group_coh[subid] = sub_coh
        else:
            print 'Subject %s not in list of subject, skipping...'%(subid)
            continue   
    cov_outfile = os.path.join(outdir, ''.join(['Covariance_',outname,'.csv']))
    group_cov_df = save_group_data(group_cov, cov_outfile)
    precision_outfile = os.path.join(outdir, ''.join(['Precision_',outname,'.csv']))
    group_precision_df = save_group_data(group_precision, precision_outfile)
    corr_outfile = os.path.join(outdir, ''.join(['Correlation_',outname,'.csv']))
    group_corr_df = save_group_data(group_corr, corr_outfile)    
    coh_outfile = os.path.join(outdir, ''.join(['Coherence_',outname,'.csv']))
    group_coh_df = save_group_data(group_coh, coh_outfile)    
    
    
if __name__ == '__main__':


    #### Set parameters #######
    datadir = '/home/jagust/rsfmri_ica/CPAC/connectivity/timecourses/smoothed/Greicius_90_rois'
    outdir = '/home/jagust/rsfmri_ica/CPAC/connectivity/matrices/smoothed'
    outname = 'Greicius_90rois_0-01_0-08_subset'
    tc_glob = 'B*_timecourses.csv'
    tc_files = glob(os.path.join(datadir, tc_glob))
    tc_files.sort()
    tc_subset = ['anterior_Salience','dDMN','LECN','post_Salience','Precuneus',\
                'RECN','vDMN','Visuospatial']
    subgroup_file = None
    tr = 2.2
    ###########################
    if subgroup_file:
        with open(subgroup_file) as f:
            subgroup = f.read().splitlines()
        
    main(datadir, outdir, outname, tc_files, tr, tc_subset=None, subgroup=None)



import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd


def get_seedname(seedfile):
    _, nme, _ = utils.split_filename(seedfile)
    return nme
    
def extract_seed_ts(data, seeds, mask):
    """ check shape match of data and seed
    if same assume registration
    extract mean of data in seed > 0"""
    data_dat = nib.load(data).get_data()
    mask_dat = nib.load(mask).get_data()
    meants = {}
    for seed in seeds:
        seednme = get_seedname(seed)
        seed_dat = nib.load(seed).get_data().squeeze()
        seed_dat[mask_dat == 0] = 0
        assert seed_dat.shape == data_dat.shape[:3]
        tmp = data_dat[seed_dat > 0,:]
        meants.update({seednme:tmp.mean(0)})
    return meants 
    
def sort_columns(df):
    new_cols = list(df.columns)
    utils.sort_nicely(new_cols)
    sorted_df = df.reindex(columns=new_cols)
    return sorted_df

def save_to_csv(d, outfile, dropna=False):
    """
    Save dict to csv by converting to pandas dataframe and saving out
    
    d : dict
    outfile : str
    """
    df = pd.DataFrame(d)
    sorted_df = sort_columns(df)
    if dropna:
        sorted_df = sorted_df.dropna(axis=1)
    sorted_df.to_csv(outfile, sep=',', header=True, index=False)
    return sorted_df
    
def main(data_files, roi_files, mask):
    for subdat in data_files:
        submeants = extract_seed_ts(subdat, roi_files, mask)
        subid = utils.get_subid(subdat)
        outname = '_'.join([subid, 'timecourses.csv'])
        outfile = os.path.join(outdir, outname)
        subdf = save_to_csv(submeants, outfile, dropna=True)
        

if __name__ == '__main__':

    """
    Extract timeseries from a set of ROIs for each functional dataset in a list. Also accepts a
    mask (ie. group intersection mask) and will drop timecourses of any ROIs falling outside of this mask.
    """

    
    ######### Set parameters #################################
    ##########################################################
    outdir = '/home/jagust/rsfmri_ica/CPAC/connectivity/timecourses/MSDL_rois'
    mask = '/home/jagust/rsfmri_ica/CPAC/rsfmriMask_3mm.nii.gz'
    data_glob = '/home/jagust/rsfmri_ica/CPAC/pipeline_rsfmri/B*/functional_mni/_scan_func_B*_4d/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm1.global0.motion1.quadratic1.gm0.compcor0.csf1/_bandpass_freqs_0.01.0.08/bandpassed_demeaned_filtered_warp.nii.gz'

    data_files = glob(data_glob)
    roi_glob = '/home/jagust/jelman/templates/MSDL_rois/MNI_3mm/*.nii.gz'
    roi_files = glob(roi_glob)
    ##########################################################

    main(data_files, roi_files, mask)

        





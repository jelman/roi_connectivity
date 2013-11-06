import os, sys
import csv
import numpy as np
from glob import glob
import general_utilities as utils
import nibabel as nib
import pandas as pd
import re

def get_seedname(seedfile):
    _, nme, _ = utils.split_filename(seedfile)
    return nme
    
def extract_seed_ts(data_files, roi, mask=None, subjstr):
    """ check shape match of data and seed
    if same assume registration
    extract mean of data in seed > 0"""
    if mask:
        mask_dat = nib.load(mask).get_data()
    meants = {}
    roi_dat = nib.load(roi).get_data().squeeze()
    for subdat in data_files:
        subid = gu.get_subid(subdat, subjstr)
        data_dat = nib.load(subdat).get_data()
        if mask:
            roi_dat[mask_dat == 0] = 0
        assert roi_dat.shape == data_dat.shape[:3]
        tmp = data_dat[roi_dat > 0,:]
        meants.update({subid:tmp.mean(0)})
    return meants 
   
def get_icnum(instr, pattern='ic00[0-9]{2}'):
    """regexp to find pattern in string
    default pattern = BXX-XXX  X is [0-9]
    """

    m = re.search(pattern, instr)
    try:
        icnum = m.group()
    except:
        print pattern, ' not found in ', instr
        subnum = None
    return icnum
    
    
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
    
def main(data_files, roi_files, mask, subjstr):
    datadict = {}
    for roifile in roi_files:
        roinme = get_seedname(roifile)
        icnum = get_icnum(roifile)
        dataglob = os.path.join(datadir, ''.join([icnum,'_sub*.nii']))
        data_files = glob(dataglob)
        data_files = sorted(data_files)
        roimeants = extract_seed_ts(data_files, roifile, mask,subjstr)
        datadict.update({roinme:roimeants})
    datadf = save_to_csv(datadict, outfile, dropna=True)
        

if __name__ == '__main__':

    """
    Extract timeseries from a set of ROIs for each functional dataset in a list. 
    Also accepts a mask (ie. group intersection mask) and will drop timecourses 
    of any ROIs falling outside of this mask.
    """

    
    ######### Set parameters #################################
    ##########################################################
    outfile = '/home/jagust/rsfmri_ica/results/DualRegress/ROI/PIB_Index/ROI_fc_Young.csv'
    mask = None
    datadir = '/home/jagust/rsfmri_ica/data/Allsubs_YoungICA_2mm_IC30.gica/BPM/func_data/Young'
    roi_glob = '/home/jagust/rsfmri_ica/data/Allsubs_YoungICA_2mm_IC30.gica/BPM/results/PIB_Index/ResultsROIs/ic00*'
    roi_files = glob(roi_glob)
    subjstr = 'sub[0-9]{3}'
    ##########################################################

    main(datadir, roi_files, mask, subjstr=subjstr)

        





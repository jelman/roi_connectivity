import os, sys
from glob import glob
import general_utilities as utils
sys.path.append('/home/jagust/jelman/CODE/pyClusterROI')
import make_local_connectivity_tcorr as make_tcorr



    
    ######### Set parameters #################################
    ##########################################################
    outdir = '/home/jagust/rsfmri_ica/cluster_roi'
    subj_cluster_suffix = '_tcorr'
    maskfile = '/home/jagust/rsfmri_ica/CPAC/rsfmriMask_3mm.nii.gz'
    data_glob = '/home/jagust/rsfmri_ica/CPAC/pipeline_rsfmri/B*/functional_mni/_scan_func_B*_4d/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm1.global0.motion1.quadratic1.gm0.compcor0.csf1/_bandpass_freqs_0.01.0.08/bandpassed_demeaned_filtered_warp.nii.gz'
    data_files = glob(data_glob)
    thresh = .5
    ##########################################################
    
    
make_local_connectivity_tcorr( infile, maskfile, outfile, thresh )
outname=outfile+'_'+str(k)+'.npy'	

import sys
sys.path.append("/home/jagust/jelman/CODE/cluster_roi")
from make_local_connectivity_tcorr import *
from binfile_parcellation import *
from group_binfile_parcellation import *
from make_image_from_bin import *
from make_image_from_bin_renum import *
from time import time
from glob import glob


# Directory to save output of clustering
outdir = '/home/jagust/rsfmri_ica/cluster_roi'

# the name of the maskfile that we will be using
maskname='/home/jagust/rsfmri_ica/CPAC/rsfmriMask_3mm.nii.gz'

# make a list of all of the input fMRI files that we will be using
data_glob = '/home/jagust/rsfmri_ica/CPAC/pipeline_rsfmri/B*/functional_mni/_scan_func_B*_4d/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm1.global0.motion1.quadratic1.gm0.compcor0.csf1/_bandpass_freqs_0.01.0.08/bandpassed_demeaned_filtered_warp.nii.gz'
infiles = glob(data_glob)
    
# set threshold for individual connectivity matrics (r>.5 used in the paper)
thresh = .5



##### Step 1. Individual ConnEctivity Matrices 
# construct the connectivity matrices using tcorr and a threshold

for idx, in_file in enumerate(infiles):

    # construct an output filename for this file
    outname= os.path.join(outdir, 'rm_tcorr_conn_'+str(idx)+'.npy')

    print 'tcorr connectivity',in_file
    # call the funtion to make connectivity
    make_local_connectivity_tcorr( in_file, maskname, outname, 0.5 )


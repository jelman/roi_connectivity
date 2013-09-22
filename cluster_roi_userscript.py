import os, sys
sys.path.append("/home/jagust/jelman/CODE/cluster_roi")
from make_local_connectivity_tcorr import *
from binfile_parcellation import *
from group_binfile_parcellation import *
from make_image_from_bin import *
from make_image_from_bin_renum import *
from time import time
from glob import glob

############ Set parameters ###############################
# Directory to save output of clustering
outdir = '/home/jagust/rsfmri_ica/cluster_roi'

# the name of the maskfile that we will be using
maskname='/home/jagust/rsfmri_ica/CPAC/rsfmriMask_GM20_3mm.nii.gz'

# make a list of all of the input fMRI files that we will be using
data_glob = '/home/jagust/rsfmri_ica/CPAC/pipeline_rsfmri/B*/functional_mni/_scan_func_B*_4d/_csf_threshold_0.96/_gm_threshold_0.7/_wm_threshold_0.96/_compcor_ncomponents_5_selector_pc10.linear1.wm1.global0.motion1.quadratic1.gm0.compcor0.csf1/_bandpass_freqs_0.01.0.08/bandpassed_demeaned_filtered_warp.nii.gz'
infiles = sort(glob(data_glob))
    
# set threshold for individual connectivity matrics (r>.5 used in the paper)
thresh = .5
##############################################################
T0 = time()

os.chdir(outdir)

##### Step 1. Individual Connectivity Matrices 
# construct the connectivity matrices using tcorr and a threshold

for idx, in_file in enumerate(infiles):

    # construct an output filename for this file
    outname= os.path.join(outdir, 'rm_tcorr_conn_'+str(idx)+'.npy')

    print 'tcorr connectivity',in_file
    # call the funtion to make connectivity
    make_local_connectivity_tcorr( in_file, maskname, outname, 0.5 )


##### Step 2. Individual level clustering
# next we will do the individual level clustering, this is not performed for 
# group-mean clustering, remember that for these functions the output name
# is a prefix that will have K and .npy added to it by the functions. We
# will perform this for clustering between 100, 150 and 200 clusters
NUM_CLUSTERS = [100,150,200]

# for tcorr
for idx, in_file in enumerate(infiles):

    # construct filenames
    infile=os.path.join(outdir,'rm_tcorr_conn_'+str(idx)+'.npy')
    outfile=os.path.join(outdir, 'rm_tcorr_indiv_cluster_'+str(idx))

    print 'tcorr parcellate',in_file
    binfile_parcellate(infile, outfile, NUM_CLUSTERS)

    
##### Step 3. Group level clustering
# perform the group level clustering for clustering results containing 100, 150,
# and 200 clusters.
# for both group-mean and 2-level clustering we need to know the number of
# nonzero voxels in in the mask 
mask_voxels=(nb.load(maskname).get_data().flatten()>0).sum()
    
# the 2-level clustering has to be performed once for each desired clustering
# level, and requires individual level clusterings as inputs
for k in NUM_CLUSTERS:
    ind_clust_files=[]
    for i in range(0,len(infiles)):
        ind_clust_files.append('rm_tcorr_indiv_cluster_'+str(i)+\
            '_'+str(k)+'.npy')

    print '2-level parcellate tcorr',k
    group_binfile_parcellate(ind_clust_files,\
        'rm_group_tcorr_cluster_'+str(k)+'.npy',k,mask_voxels)


##### Step 4. Convert the binary output .npy files to nifti
# this can be done with or without renumbering the clusters to make sure they
# are contiguous.
# write out for group 2-level clustering
for k in NUM_CLUSTERS:
    binfile='rm_group_tcorr_cluster_'+str(k)+'.npy'
    imgfile='rm_group_tcorr_cluster_'+str(k)+'.nii.gz'
    make_image_from_bin_renum(imgfile,binfile,maskname)
    
T1 = time()

print '******************************'
print 'time is ', T1-T0
##### FIN


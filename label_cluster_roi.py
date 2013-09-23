import os, sys
import numpy as np
import general_utilities as utils
from glob import glob


def calc_pct_overlap(roi, target):
    roi_nvoxels = roi.sum()
    overlap = (roi==target) * roi
    overlap_nvoxels = overlap.sum()
    return (overlap_nvoxels/roi_nvoxels)

########### Set parameters ##########
datadir = '/home/jagust/rsfmri_ica/cluster_roi/ROIs'
roi4Dfile = os.path.join(datadir,'rm_group_tcorr_cluster_150_4D.nii.gz')
template = '/home/jagust/jelman/templates/Yeo_JNeurophysiol11_MNI152/3mm/Yeo2011_7Networks_4D_LiberalMask.nii.gz'
template_mapfile = '/home/jagust/jelman/templates/Yeo_JNeurophysiol11_MNI152/template_mapping.txt'
####################################

#Load template and 4D roi data
tempdat, _ = utils.load_nii(template)
temp_mapping = utils.load_mapping(template_mapfile)
roi4Ddat, _ = utils.load_nii(roi4Dfile)
# Verify the shape of datasets match
assert tempdat.shape[:-1] == roi4Ddat.shape[:-1]

cluster_labels = {}
for i in roi4Ddat.shape[3]:
    roidat = roi4Ddat[:,:,:,i]
    for j in tempdat.shape[3]:
        temp_mask = tempdat[:,:,:,j]
        pct_overlap = calc_pct_overlap(roidat, temp_mask)
        if pct_overlap > .5:
            cluster_name = 'cluster%03d'%(i+1)
            label_name = temp_mapping[str(j+1)]
            cluster_labels[cluster_name] = label_name


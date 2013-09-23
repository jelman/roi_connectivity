import os, sys
import numpy as np
import general_utilities as utils
from glob import glob


########### Set parameters ##########
datadir = '/home/jagust/rsfmri_ica/cluster_roi/ROIs'
roi4Dfile = os.path.join(datadir,'rm_group_tcorr_cluster_150_4D.nii.gz')
template = '/home/jagust/jelman/templates/Yeo_JNeurophysiol11_MNI152/3mm/Yeo2011_7Networks_4D_LiberalMask.nii.gz'
template_mapfile = '/home/jagust/jelman/templates/Yeo_JNeurophysiol11_MNI152/template_mapping.txt'
####################################

tempdat, _ = utils.load_nii(template)
temp_mapping = utils.load_mapping(template_mapfile)
roi4Ddat, _ = utils.load_nii(roi4Dfile)

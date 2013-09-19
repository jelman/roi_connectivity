import os, sys
from glob import glob
import general_utilities as utils
sys.path.append('/home/jagust/jelman/CODE/pyClusterROI')
import make_local_connectivity_tcorr as make_tcorr




make_local_connectivity_tcorr( infile, maskfile, outfile, thresh )
outname=outfile+'_'+str(k)+'.npy'	

import os, sys
sys.path.insert(0, '/home/jagust/jelman/CODE/GIFT_analysis')
import gift_analysis as ga
import gift_utils as gu
from glob import glob
import numpy as np


if __name__ == '__main__':


    ####################### Set parameters################
    basedir = '/home/jagust/rsfmri_ica/GIFT/GICA_d75/roi_connectivity/'
    datadir = '/home/jagust/rsfmri_ica/GIFT/GICA_d75/roi_connectivity/matrices'
    nnodes = 23
    modeldir = '/home/jagust/rsfmri_ica/GIFT/models/Old'
    des_file = os.path.join(modeldir, 'Covariate_Old_log_demeaned.mat')
    con_file = os.path.join(modeldir, 'Covariate_Old_log_demeaned.con')
    resultsglob = '*mancovan_preproc.csv'
    ##############################################################


    ## Run group analysis with randomise
    ####################################
    exists, resultsdir = gu.make_dir(basedir,'randomise') 
    result_files = glob(os.path.join(datadir,resultsglob))
    for data_file in result_files:
        data = np.genfromtxt(data_file, names=None, dtype=float, delimiter=',')
        pth, fname, ext = gu.split_filename(data_file)
        img_fname = os.path.join(resultsdir, fname + '.nii.gz')
        saveimg = gu.save_img(data, img_fname)
        rand_basename = os.path.join(resultsdir, fname)
        p_uncorr_list, p_corr_list = ga.randomise(saveimg, 
                                                    rand_basename, 
                                                    des_file, 
                                                    con_file)     
        uncorr_results = ga.get_results(p_uncorr_list)
        corr_results = ga.get_results(p_corr_list)
               
        fdr_results = {}
        for i in range(len(uncorr_results.keys())):
            conname = sorted(uncorr_results.keys())[i]
            fdr_corr_arr = ga.multi_correct(uncorr_results[conname])
            fdr_results[conname] = gu.square_from_combos(fdr_corr_arr, nnodes)
            
            outfile = os.path.join(resultsdir, 
                                ''.join([rand_basename, '_fdr_corrp_','tstat',str(i+1),'.txt']))
            # Save results to file
            np.savetxt(outfile, 
                        fdr_results[conname], 
                        fmt='%1.5f', 
                        delimiter='\t')  
            print('Saved corrected output to %s'%(outfile))        

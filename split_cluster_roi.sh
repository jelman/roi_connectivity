#!/bin/sh
# Script to split and binarize labelled ROIs from output of Craddock parcellation code

datadir=/home/jagust/rsfmri_ica/cluster_roi/ROIs


for i in {1..150};
do
lower=$(echo "scale=1; $i -0.1" | bc)
upper=$(echo "scale=1; $i +0.1" | bc)
printf -v volnum "%03d" $i
outfile="$datadir"/cluster"$volnum".nii.gz
fslmaths /home/jagust/rsfmri_ica/cluster_roi/ROIs/rm_group_tcorr_cluster_150.nii.gz -thr "$lower" -uthr "$upper" -bin $outfile

done

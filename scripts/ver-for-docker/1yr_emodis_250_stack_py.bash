#!/bin/bash
#this script produces an one-year-stack-good ndvi file
#inputs: flist_ndvi, flist_bq, ul_lon,ul_lat,lr_lon,lr_lat
#output:one-year-stack-good file
#example inputs:
#flist_ndvi='/home/jiang/nps/cesu/modis_ndvi_250m/wrkdir/2010/2010_flist_ndvi'
#flist_bq = '/home/jiang/nps/cesu/modis_ndvi_250m/wrkdir/2010/2010_flist_bq'
#ul_lon=-173.0d,ul_lat=72.0d
#lr_lon=-127.999116667d,lr_lat=54.000019444d
#if do not want subsize, input: 0,0,0,0 for four conor cooordinates


#check if input parameters are correct

#source ./1yr_emodis_250_env_py_docker.bash

if [ $# != 6 ];then
echo
echo "input flist_ndvi and flist_bq ul_lon ul_lat lr_lon lr_lat"
echo
exit 1
fi

flist_ndvi=$1
flist_bq=$2
ul_lon=$3
ul_lat=$4
lr_lon=$5
lr_lat=$6

#get the year

file=`basename $flist_ndvi`

year=${file:0:4}

#check if there are stacked files

if [ -f $flist_ndvi ]; then

   #call python program

   python $pycodes/oneyear_data_layer_subset_good.py $flist_ndvi $flist_bq $ul_lon $ul_lat $lr_lon $lr_lat

   cp $unzipped_dir/${year}/${year}_stack_ndvi.tif $stacked_dir/$year

   cp $unzipped_dir/${year}/${year}_stack_bq.tif   $stacked_dir/$year

fi

exit 0  



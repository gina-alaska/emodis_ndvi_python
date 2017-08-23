#!/bin/bash
#this script calcualte ndvi metrics.
#input: a one-year file name
#outputs: a smooth data file, a metrics file


if [ $# != 4 ];then

echo "input arguments: stacked_ndvi_file, stacked_bq_file rst_dir year"

exit 1

fi

#load environment variabels

source ./1yr_emodis_250_env_py_docker.bash

#cd $idlprg_dir

stacked_ndvi_file=$1

stacked_bq_file=$2

rst_dir=$3

year=$4


fd=`dirname $stacked_ndvi_file`

if [ ! -f ${rst_dir}/$year/${year}*_metrics_*.tif ]; then


    mkdir -p ${rst_dir}/$year

    #Send output to logfile
    #LOG=$fd/calculate-metrics.log
    #exec >>$LOG
    #exec 2>>$LOG

    echo "________________________"

    #send start time

    echo calculating ndvi-metrics started at `date -u`

    out_dir=$rst_dir/$year

    python $pycodes/smooth_calculate_metrics_tile_parallel.py $stacked_ndvi_file $stacked_bq_file $out_dir

    #Send end time

    echo "________________________"

    echo $0 ended at `date -u`

fi

exit 0

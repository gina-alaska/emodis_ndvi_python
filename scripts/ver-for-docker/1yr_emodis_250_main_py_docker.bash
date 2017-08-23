#!/bin/bash
#this script call many scripts to finish one-year ndvi metrics calculation
#input:year
#outputs: a smooth data file, a metrics file

if [ $# != 1 ];then

echo "input year"

exit 1

fi

year=$1

#0. set variables, load environment variables,and craete a log file

source ./1yr_emodis_250_env_py_docker.bash

#make a directory

mkdir -p ${work_dir}/$year

#Send output to logfile

LOG=${work_dir}/$year/${year}-ndvi-metrics.log

exec >>$LOG

exec 2>>$LOG

echo "________________________"

echo $0 started at `date -u`

#0.5 downlpoad raw data from USGS

mkdir -p ${raw_dir}/$year

./1yr_emodis_250_download_withauthoration_py.bash ${raw_dir} $year

#1. unzip raw files from $raw_dur to $unzipped_dir

echo "unzip raw data to ${unzipped_dir}/${year} started at `date -u`"

mkdir -p ${unzipped_dir}/$year

./1yr_emodis_250_unzip_py.bash ${raw_dir} ${unzipped_dir} ${year}

#2. get the flist names for ndvi and bq 

./1yr_emodis_250_flist_py.bash ${unzipped_dir} ${year}

flist_ndvi=${unzipped_dir}/${year}/${year}_flist_ndvi

flist_bq=${unzipped_dir}/${year}/${year}_flist_bq

#3. make the single file for each composite day

echo "stack one year data files started at `date -u`"

mkdir -p ${stacked_dir}/$year

./1yr_emodis_250_stack_py.bash ${flist_ndvi} ${flist_bq} 0 0 0 0 

#4.calculate ndvi metrics

"echo calculate ndvi-metrics started at `date -u`"

mkdir -p ${rst_dir}/$year

./1yr_emodis_250_calmetrics_py.bash ${stacked_dir}/$year/${year}_stack_ndvi.tif ${stacked_dir}/$year/${year}_stack_bq.tif ${rst_dir} $year

"echo calculate ndvi-metrics ended at `date -u`"
 
exit 0

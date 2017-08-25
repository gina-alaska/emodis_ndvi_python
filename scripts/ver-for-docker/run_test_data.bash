#!/bin/bash
#this script run test data to verify that emodis_ndvi_metreics algorithm program works.

year=2016

# 0. set envs
if [ -f env.bash ]; then

   rm env.bash

fi

cat<<EOF>>env.bash

export raw_dir=/2016-test

export work_dir=/2016-test/work

export unzipped_dir=/2016-test/work/unzipped

export stacked_dir=/2016-test/work/stacked

export rst_dir=/2016-test/work/rst

export script_dir=${HOME_EXC}/scripts/ver-for-docker

export python=/usr/bin/python

export pycodes=${HOME_EXC}/pycodes

EOF

source ./env.bash

#clean directories

rm -r $work_dir


cd $script_dir

#make a directory

mkdir -p ${unzipped_dir}/$year

#raw data are stored at localhost:/data/2016-test/2016. 
#localhost:/data/2016-test is mapping to docker:/2016-test

#tar xvf  /code/2016-test.tar -C ${unzipped_dir}/$year

#mv ${unzipped_dir}/$year/2016-test/* ${unzipped_dir}/$year

#rmdir ${unzipped_dir}/${year}/2016-test


mkdir -p ${work_dir}/$year

#Send output to logfile

LOG=${work_dir}/$year/${year}-ndvi-metrics.log

exec >>$LOG

exec 2>>$LOG

echo "________________________"

echo $0 started at `date -u`

#0.5 downlpoad raw data from USGS

#mkdir -p ${raw_dir}/$year

#./1yr_emodis_250_download_withauthoration_py.bash ${raw_dir} $year

#1. unzip raw files from $raw_dur to $unzipped_dir

#echo "unzip raw data to ${unzipped_dir}/${year} started at `date -u`"

#mkdir -p ${unzipped_dir}/$year

#./1yr_emodis_250_unzip_py.bash ${raw_dir} ${unzipped_dir} ${year}

#2. get the flist names for ndvi and bq 

${script_dir}/1yr_emodis_250_flist_py.bash ${unzipped_dir} ${year}

flist_ndvi=${unzipped_dir}/${year}/${year}_flist_ndvi

flist_bq=${unzipped_dir}/${year}/${year}_flist_bq

#3. make the single file for each composite day

echo "stack one year data files started at `date -u`"

mkdir -p ${stacked_dir}/$year

${script_dir}/1yr_emodis_250_stack_py.bash ${flist_ndvi} ${flist_bq} 0 0 0 0 

#4.calculate ndvi metrics

"echo calculate ndvi-metrics started at `date -u`"

mkdir -p ${rst_dir}/$year

${script_dir}/1yr_emodis_250_calmetrics_py.bash ${stacked_dir}/$year/${year}_stack_ndvi.tif ${stacked_dir}/$year/${year}_stack_bq.tif ${rst_dir} $year

"echo calculate ndvi-metrics ended at `date -u`"
 
exit 0

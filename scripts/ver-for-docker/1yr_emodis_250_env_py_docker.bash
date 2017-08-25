#this script defines the environment variables for 1yr_emodis_250_main_py.bash

#directories
#raw_dir is the home directory for raw data.
#7-day NDVI files ae stored in $year

export raw_data_url=http://dds.cr.usgs.gov/emodis/Alaska/historical/TERRA

export raw_dir=${HOME_DATA}

export work_dir=${HOME_DATA}/work

export unzipped_dir=${work_dir}/unzipped

export stacked_dir=${work_dir}/stacked

export rst_dir=${work_dir}/rst

export script_dir=${HOME_EXC}/scripts/ver-for-docker

export python=/usr/bin/python

export pycodes=${HOME_EXC}/pycodes




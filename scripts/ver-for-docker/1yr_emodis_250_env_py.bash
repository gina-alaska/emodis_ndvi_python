#this script defines the environment variables for 1yr_emodis_250_main_py.bash

#directories
#raw_dir is the home directory for raw data.
#7-day NDVI files ae stored in $year

export raw_dir=~/data/modis_ndvi/raw

export work_dir=~/data/modis_ndvi/work

export unzipped_dir=${work_dir}/unzipped

export stacked_dir=${work_dir}/stacked

export rst_dir=${work_dir}/rst

export script_dir=~/projects/nps/emodis_ndvi_python/scripts/ver-for-docker

export python=/usr/bin/python

export pycodes=~/projects/nps/emodis_ndvi_python/pycodes




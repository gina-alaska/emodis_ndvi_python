#!/bin/bash
#downloads emodis data by wget

if [ $# != 2 ]; then

echo "Usage:1yr_emodis_250_download.bash dir_data year"

exit 1

fi

url=http://dds.cr.usgs.gov/emodis/Alaska/historical/TERRA

dir_data=$1

year=$2

#check if raw data have already been downloaded"

if [ ! -f ${dir_data}/${year}/*.zip ]; then

   mkdir -p ${dir_data}/${year}

   cd ${dir_data}/$year

   wget --user jiang@gina.alaska.edu --password Gina7Zhu -r -nd -np -nH --reject="index.html*" -A "*NDVI*QKM*.zip" $url/$year .

fi

exit 0

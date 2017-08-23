#!/bin/bash
#copy one year of emaodis 250m data to $WRKDIR/nps/ndvi

if [ $# != 3 ];then

  echo "input arguments: raw_dir, unzipped_dir, year"
 
  exit 1

fi

raw_dir=$1

unzipped_dir=$2

year=$3

#source ./1yr_emodis_250_env_py_docker.bash

org=$raw_dir/$year

#org=/projects/UAFGINA/project_data/emodis/distribution/Alaska/historical/TERRA

des=$unzipped_dir/$year

if [ ! -f $des/*.tif ]; then

    mkdir -p $des

    cd $des

    #find $org -type d -name "comp_???" > dlist

    find $org -type f -name "*.zip" >flist

    for file in $(cat flist); do

        echo "copy $file to $des and unzip it..."
 
        fbname=`basename $file`

        cp $file $des

        unzip $fbname

    done

fi

echo "finish copying and unzipping the files!"

exit 0




#!/bin/bash
#copy one year of emaodis 250m data to $WRKDIR/nps/ndvi

if [ $# != 3 ];then

  echo "input arguments: raw_dir, unzipped_dir, year"
 
  exit 1

fi

raw_dir=$1

unzipped_dir=$2

year=$3

#source ./1yr_emodis_250_env.bash

org=$raw_dir/$year

#org=/projects/UAFGINA/project_data/emodis/distribution/Alaska/historical/TERRA


des=$unzipped_dir/$year

mkdir -p $des

cd $des

find $org -type d -name "comp_???" > dlist

for d in $(cat dlist); do
   echo "copy $d/*NDVI*.QKM*.zip to $des and unzip it..."

  ffname=`ls $d/*NDVI*.QKM*.zip` 
 
  fbname=`basename $ffname`

  cp $ffname $des

  unzip $fbname


done

echo "finish copying and unzipping the files!"



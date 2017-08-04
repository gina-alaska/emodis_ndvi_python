#!/bin/bash

function usage() { 
  echo "usage: emodis_ndvi.sh [year] [SOURCE_DIR] [DEST_DIR]"
  exit 1
}

year=$1
source_dir=$2
dest_dir=$3

if [ -n $year ]; then
  echo "error: invalid year"
  usage
fi

if [ ! -d $source_dir ]; then
  echo "source data $source_dir invalid"
  usage
fi

if [ ! -d $dest_dir ]; then
  echo "target output directoy does not exist: $dest_dir"
  usage
fi

echo "running model with options: year=$year source_dir=$source_dir dest_dir=$dest_dir"

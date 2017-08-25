#!/bin/bash

if [$# !=1 ];then

  echo "input:year"
  exit 1

fi

echo "run NDVI algorithm to produce NDVI metrics"

cd $HOME_EXC/scripts/ver-for-docker

./1yr_emodis_250_main_py_docker.bash $year

echo "done!"

exit 0

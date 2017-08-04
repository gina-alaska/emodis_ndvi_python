src_data=/home/jzhu4/data/modis_ndvi/2016
test_data=/home/jzhu4/data/modis_ndvi/2016-test
mkdir $test_data
for file in $src_data/*.tif; do
  name=`basename $file`
  gdal_translate -CO compress=lzw  -projwin 283351 1681201 2913207 1673845 -of GTiff $file $test_data/$name
done

du -sh $test_data

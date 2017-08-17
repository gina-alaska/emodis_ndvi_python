import raster_process as rp
import numpy as np
import platform
from osgeo import gdal
 
def read_ndvi(t_fn,d_fn,ulx,uly,lrx,lry,bandname):
#This progranm read a pair of files (ndvi and ndvi_bq), and stack, subset, return two file describers
#inputs:
#t_fn---file name of a *ndvi.tif file
#d_fn---file name of a *ndvi_bq.tif
#ulx uper left x coordinate in unit of meter
#uly---upper left y coordinate in unit of meter
#lrx---lower right x coorinate in unit of meter
#lry---lower right y coorinate in unit of meter
#badname---bandname for NDVI metrics
#output: rt_fid,rt_bq_fid

#example: t_fid, found map unit of t_fid is meters, so we define ul and lr in meters
#ulx=-206833.75,
#uly=1303877.50
#lrx=424916.25
#lry=856877.50D


    if platform.system() == 'Windows':
       sign='\\'
    else:
       sign='/'

    #---determine if doing subset

    if not (ulx == 0.0 and uly == 0.0 and lrx == 0.0 and lry == 0.0): # do subset
  
       # subseting the file

       t_fn=subsection(t_fn, ulx, uly, lrx, lry)
       
       d_fn=subsection(d_fn, ulx, uly, lrx, lry)
   
    #---- fill snow,cloud,bad, and negative reflectance pixels with -4000
   
    image_ndvi=rp.raster2array(t_fn)

    image_bq=rp.raster2array(d_fn)

    image_ndvi=np.uint8(image_ndvi/100+100) # convert -10,000 to 10,000 into 0 to 200

    # np.uint8 ranges is from 0 to 255

    #---output image_ndvi and image_bq into two files
   
    #--- output image_ndvi

    t_fn_base=t_fn.rsplit('.tif')[0]

    out_ndvi_name = t_fn_base + '_good_ndvi.tif'
    
    rp.array2raster(out_ndvi_name,t_fn,image_ndvi,bandname)
   
    d_fn_base=d_fn.rsplit('.tif')[0]

    out_bq_name = d_fn_base + '_good_bq.tif'

    rp.array2raster(out_bq_name,d_fn,image_bq,bandname)


    #---return file names

    rt_t=out_ndvi_name

    rt_d=out_bq_name


    return (rt_t,rt_d)








'''
Jinag Zhu, jiang@gina.alaska.edu, 7/19/2017. 

Re-write the program with python.This program interpolates and smoothes a multiyear_layer_stack file and calculate metrics of mid-year data.
The input are:
  oneyear_stack_ndvi_file
  oneyear_stack_bq_file
The output are:
  a mid-year smoothed data file named as year_multiyear_layer_stack_smoothed
  a metrics file named as year_multiyear_layer_stack_smoothed_metrics
flg indicating if this program run successfully.
jzhu, 1/17/2012,this program combines moving average and threshold methodm it calls geoget_ver16.pro and sosget_ver16.pro. 

'''

import sys
#import os
from osgeo import gdal
import platform
from read_ndvi import *
import raster_process as rp
from time_series_process_nps_oneyear import *

def main():

   ver='py' 

   #accept commanline arguments: filen

   print 'Number of arguments:', len(sys.argv), 'arguments.'

   print 'Argument List:', str(sys.argv)

   if len(sys.argv) != 3:
 
      print "input arguments are: filen_ndvi filen_bq"

      return 1

   filen_ndvi=sys.argv[1]

   filen_bq=sys.argv[2]

   #make sure the program can work in both windows and linux.

   if platform.system() == 'Windows':
      sign='\\'
   else:
      sign='/'

   #produces output file names: smooth data file name and metrics file name.

   p1=filen_ndvi.rfind(sign)

   length=len(filen_ndvi)

   wrkdir=filen_ndvi[0:p1]

   filebasen=filen_ndvi[p1+1:length-4]  # file name without affix '.tif'

   #----open smooth file and metrics file to ready to be writen.

   fileout_smooth=wrkdir+sign+filebasen+'_smooth_'+ver+'.tif'

   #openw,unit_smooth,fileout_smooth,/get_lun

   fileout_metrics=wrkdir+sign+filebasen+'_metrics_'+ver+'.tif'

   #define bandname for metrics output file.

   metrics_bname =np.array(['onp','onv','endp','endv','durp','maxp','maxv','ranv','rtup','rtdn','tindvi','mflg'])

   metrics_bnum=metrics_bname.shape[0]

   #open the input file

   data=gdal.Open(filen_ndvi)

   qual=gdal.Open(filen_bq)

   #define the fill value for mising pixel, and fill value for snow, cloud, bad, and negative reflectance pixel.

   threshold = 80 # fill value is -2000, after convert into 0-200, this value is equal to 80

   snowcld = 60 # snow and cloud are set into -4000, after convert into 0-200, they are 60

   #get band name from data

   bnum=data.RasterCount

   xsize=data.RasterXSize

   ysize=data.RasterYSize

   bname=[]  #hold band names in raster data

   for i in range(1,bnum+1):  #band index from 1 to bnum
   
      bname.append(data.GetRasterBand(i).GetDescription())

   #convert list bname to np.array bname

   bname=np.array(bname)

   #define two array to hold the smooth and metrics

   a_smooth = np.zeros((bnum,ysize,xsize),dtype=np.uint8 )

   a_metrics= np.zeros((metrics_bnum,ysize,xsize),dtype=np.float16)

   #two loops, goes through each vector

   for y in range(ysize):  
   
      print('processing the '+str(y+1)+' th row of total '+str(ysize) )+' rows'     

      for x in range(xsize):

         #print( 'processing: '+str(y)+ ' row of total '+str(ysize)+' and '+str(x)+ ' col of total '+str(xsize) )

         v_ndvi = data.ReadAsArray(x,y,1,1).flatten()

         v_bq  = qual.ReadAsArray(x,y,1,1).flatten()

         #---calls time_series_process to do one-year data interpolate, smooth, and calculate metrics

         (v_smooth,v_metrics)=time_series_process_nps_oneyear(v_ndvi,v_bq,bname,threshold,snowcld)

         #write time_series_verctors to the a_smooth[:,y,x] and a_metrics[:,y,x]

         a_smooth[:,y,x] =  v_smooth

         a_metrics[:,y,x] = v_metrics

   '''write a_smooth and a_metrics to files, because gdal only have float32, float64, not have flaot16,
but a_metrics is dtype('float16'), change the a_metrics into float32
   '''
   rp.write_raster(fileout_smooth,  filen_ndvi, a_smooth,              bname)

   rp.write_raster(fileout_metrics, filen_ndvi, np.float32(a_metrics), metrics_bname)

   print( 'finishing calculation of metrics!')
  
   return 0

if __name__=='__main__':

   main()



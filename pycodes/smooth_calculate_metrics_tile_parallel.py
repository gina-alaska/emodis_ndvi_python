'''
#;Jinag Zhu, jiang@gina.alaska.edu, 7/19/2017. re-write the program with python.
#This program interpolates and smoothes a multiyear_layer_stack file and calculate metrics of mid-year data.
#The input is:a oneyear_stack file
#the output is:
#a mid-year smoothed data file named multiyear_layer_stack_smoothed,
#a metrics file named multiyear_layer_stack_smoothed_metrics.
#flg indicating if this program run successfully.
#This program breaks the huge data into tiles and goes through tile loop to proces each tile. For each tile, go through
#each pixel to calulate the metrics and smoothed time series of the pixel. 
#jzhu, 1/17/2012,this program combines moving average and threshold methodm it calls geoget_ver16.pro and sosget_ver16.pro. 

'''

import sys
import os
from osgeo import gdal, ogr, osr
import platform
from read_ndvi import *
import raster_process as rp
from time_series_process_nps_oneyear_parallel import *
from multiprocessing import Pool

def main(): 

   ver='py' #this is added to file name to reflect the data produced by different version of algorithm

   flg=0 # 0--success, 1-- fail

   #accept commanline arguments: filen

   print ('Number of arguments: '+ str(len(sys.argv)) + ' arguments.')
   
   print( 'Argument List: ' + str(sys.argv) )

   if len(sys.argv) != 4:

      print( "input arguments are: filen_ndvi filen_bq out_dir")

      #sys.exit(1)

      return 1

   filen_ndvi=sys.argv[1]

   filen_bq=sys.argv[2]

   out_dir=sys.argv[3]

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

   year=filebasen[0:4]

   #open smooth file and metrics file to ready to be writen.

   fileout_smooth=out_dir+sign+filebasen+'_smooth_'+ver+'.tif'

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

   # get bandname from data

   bnum=data.RasterCount

   xsize=data.RasterXSize

   ysize=data.RasterYSize

   bname=[]  #hold band names in raster data

   vmetrics=np.zeros((metrics_bnum),dtype=np.float16)

   for i in range(1,bnum+1):  #band index from 1 to bnum
   
      bname.append(data.GetRasterBand(i).GetDescription())

      #convert list bname to np.array bname

   bname=np.array(bname)

   #two loops, goes through each vector

   #pool=Pool()
    
   #define two array to hold the result.

   a_smooth = np.zeros((bnum,ysize,xsize),dtype=np.uint8 )

   a_metrics= np.zeros((metrics_bnum,ysize,xsize),dtype=np.float16)

   indices=range(xsize)

   #loop for row (y)

   for y in range(ysize):  #<1>  

       print("proecssing the "+str(y+1)+" th line of total "+str(ysize)+" lines")

       #ndvi_v=  data.ReadAsArray(x,y,1,1).flatten()

       #bq_v  =  qual.ReadAsArray(x,y,1,1).flatten()
      
       pool=Pool()

       xx = [( data.ReadAsArray(x,y,1,1).flatten(), qual.ReadAsArray(x,y,1,1).flatten(),bname,threshold,snowcld ) for x in range(xsize)]

       rst=pool.map(time_series_process_nps_oneyear_parallel, xx )

       #rst return a list with length of xsize, each element is a dictionary.
       #rst1=np.array(rst)  #convert list into numpy array, because element of rst is a two-element tuple,
       #rst1 becomes 2D array, rows is the length of list, and cols is 2.

       #a_smooth[:,y,indices]   = rst1[indices,0]

       #a_metrics[:,y,indices] =  rst1[indices,1]
          
       for x in range(xsize): #<2>

           a_smooth[:,y,x]  = rst[x][0]

           a_metrics[:,y,x] = rst[x][1]

       #<2>

       pool.close()  
 
   #<1> 

   #write a_smooth and a_metrics to files

   rp.write_raster(fileout_smooth, filen_ndvi, a_smooth, bname)

   rp.write_raster(fileout_metrics, filen_ndvi, np.float32(a_metrics), metrics_bname)

   print( 'finishing calculation of metrics!')

   return 0

if __name__ == "__main__":
   
   main()

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
import sys
import os
from osgeo import gdal, ogr, osr
import platform
from read_ndvi import *
import raster_process as rp
from time_series_process_nps_oneyear import *

ver='py'

flg=0 # 0--success, 1-- fail

#accept commanline arguments: filen

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 3:
  print "input arguments are: filen_ndvi filen_bq"
  sys.exit(1)

filen_ndvi=sys.argv[1]

filen_bq=sys.argv[2]

#---make sure the program can work in both windows and linux.

if platform.system() == 'Windows':
   sign='\\'
else:
   sign='/'


#----produces output file names: smooth data file name and metrics file name.

#p =strpos(filen,sign,/reverse_search)

p1=filen_ndvi.rfind(sign)

length=len(filen_ndvi)

wrkdir=filen_ndvi[0:p1]

filebasen=filen_ndvi[p1+1:length-4]  # file name without affix '.tif'


year=filebasen[0:4]

#----open smooth file and metrics file to ready to be writen.

fileout_smooth=wrkdir+sign+filebasen+'_smooth_'+ver+'.tif'


#openw,unit_smooth,fileout_smooth,/get_lun

fileout_metrics=wrkdir+sign+filebasen+'_metrics_'+ver+'.tif'


#define bandname for metrics output file.

metrics_bname =np.array(['onp','onv','endp','endv','durp','maxp','maxv','ranv','rtup','rtdn','tindvi','mflg'])

metrics_bnum=metrics_bname.shape[0]



#---open the input file

data=gdal.Open(filen_ndvi)

qual=gdal.Open(filen_bq)

#---define the fill value for mising pixel, and fill value for snow, cloud, bad, and negative reflectance pixel.

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

#---two loops, goes through each vector

for y in range(ysize):  

    for x in range(xsize):

       print('process row: '+str(y)+ ' and col: '+ str(x) )
       
       if y == 0 and x == 8730:
            print('check ')

       v_ndvi = data.ReadAsArray(x,y,1,1).flatten()

       v_bq  = qual.ReadAsArray(x,y,1,1).flatten()

       #---calls time_series_process to do three-year data interpolate, smooth, and calculate metrics

       print('calcualte 12 metrics and get v_smooth,v_metrics,v_metrics_bandname') 

       (v_smooth,v_metrics)=time_series_process_nps_oneyear(v_ndvi,v_bq,bname,threshold,snowcld)
      

       #---define a_smooth and l_metrics to store smoothed and metrics data

       if y == 0 and x == 0: # the very first loop
           
       
            a_smooth = np.zeros((bnum,ysize,xsize),dtype=np.uint8 )

            a_metrics= np.zeros((metrics_bnum,ysize,xsize),dtype=np.float16)

            #['onp','onv','endp','endv','durp','maxp','maxv','ranv','rtup','rtdn','tindvi','mflg']
           
            #onp1=np.array((xsize,ysize),dtype=np.unint8)
       
            #onv2=np.array((xsize,ysize),dtype=np.float16)
  
            #endp3=np.array((xsize,ysize),dtype=np.unint8)

            #endv4=np.array((xsize,ysize),dtype=np.float16)

            #durp5=np.array((xsize,ysize),dtype=np.unint8)

            #maxp6=np.array((xsize,ysize),dtype=np.unint8)

            #maxv7=np.array((xsize,ysize),dtype=np.float16)

            #ranv8=np.array((xsize,ysize),dtype=np.float16)

            #rtup9=np.array((xsize,ysize),dtype=np.unint8)

            #rtdn10=np.array((xsize,ysize),dtype=np.unint8)

            #tindvi11=np.array((xsize,ysize),dtype=np.float16)

            #mflg12=np.array((xsize,ysize),dtype=np.unint8)

            #l_metrics=list[ onp1,onv2,endp3,endv4,durp5,maxp6,maxv7,ranv8,rtup9,rtdn10,tindvi11,mflg12 ]
           

       #write time_series_verctors to the a_smooth[:,y,x] and a_metrics[:,y,x]

       a_smooth[:,y,x] = v_smooth

       a_metrics[:,y,x] = v_metrics

#---write a_smooth and a_metrics to files

rp.write_raster(fileout_smooth,filen_ndvi,a_smooth, bname)

rp.write_raster(fileout_smooth,filen_ndvi,a_metrics,metrics_bname)

print( 'finishing smooth and calculation of metrics!')


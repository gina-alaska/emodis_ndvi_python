#;This program process a vector, it get rid of no-sense point such as -2000 (80), intepolate with adjunct points
#;This program do not call oneyear_extension, that means do not interpolate jan,nov,and dec into feb to oct data series
#;do interpolate, interpolate threshold, if all time series are threshold values, means this pixel is not vegitation, perhaps water, do not calcualte metrics of this pixel
#;threshold is fill value, do not do interpolate, snowcld=60, need interpolate, for points with 81-100, need interpolate
 
import numpy as np
from cutoff_interp_v2 import *

def interpol_noextension_1y_vector(mid_year, mid_year_bq, mid_year_bn,threshold,snowcld):
   #inputs:
   #mid_year---one-year-ndvi
   #mid_year_bq---one-year quality
   #mid_year_bn---one-year ndvi band name
   #threshold---80b
   #snowcld---60b
   #outputs:
   #v_interp---interpolated NDIV
   #v_bq_interp---interpolated quality
   #v_bname_interp---interpolated NDVI bandname
   #flg_metrics---0, not calculate, -1, fill data, 1--calculate
   # interpol beginning and ending missing values
   #;ndvi flag: 0b- valid, 1b-cloudy,2b-bad quality,3b-negative reflectance,4b-snow,10b-fill, from eMODIS documentation
   #flg_metrics -1--fill value, not calcualte, 0--not have enough vailid data, not calcualte, 1--calculate.

  

   flg_metrics= 0 #; initial not calculate metrics 

   #;----- for fill pixels, do not calculate ndvi, just extend the band name to one year ---

   idxv=np.where( np.logical_or(mid_year_bq == 0, mid_year_bq == 4))

   cntv=len(idxv[0])

   if cntv > 5: # only consider vector having 5 more valid or none snow points as valid vector

      idxv1=np.where( np.logical_and( mid_year[idxv] > 100, max(mid_year[idxv])-100 >= 25 ) ) #;maximum must be greater than 0.25

      cntv1=len(idxv1[0])

   else:
      cntv1=0

   
   if cntv1 > 5:  #<1> ; valid point are at least 5, and maximun ndvi is at least greater or equal to 125 calcualte meterics

      flg_metrics=1 #calculate metrics

      mid_year_g = cutoff_interp_v2(mid_year, mid_year_bq)  #; cutoff_interp_ver10, first change fill value as 100, then cut off negative,
      v_interp=mid_year_g


   #;----- call oneyear_extension
   #;oneyear_extension100b, mid_year_g, mid_year_bq, mid_year_bn,mid_stnum,mid_ednum,days_mid
   #;daycom=days_mid

   #;----- output interpolated data
   #v_interp=mid_year_g  ; processed vector to v
   #v_bq_interp=mid_year_bq ; processed bq vector
   #v_bname_interp=mid_year_bn ;processed band name cevtor
   #return (v_interp,v_bq_interp,v_bname_interp)


   else:  #<1>; no enough data points, not not calculate metrics 

      flg_metrics=0

      v_interp=mid_year

      idx10=np.where( np.logical_or( mid_year_bq == 10, mid_year_bq == 2) ) #; fill or bad points

      cnt10=len(idx10[0])

      if cnt10 == len(mid_year_bq):   #; fill pixels

          flg_metrics=-1
    

      #;oneyear_extensionfillval, mid_year, mid_year_bq, mid_year_bn, mid_stnum,mid_ednum,days_mid

   v_bq_interp=mid_year_bq

   v_bname_interp=mid_year_bn


   return (v_interp,v_bq_interp,v_bname_interp,flg_metrics)



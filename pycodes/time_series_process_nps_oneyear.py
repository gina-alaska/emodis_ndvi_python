#jiang Zhu, 7/20/2017,jiang@gina.alaska.edu
#This program calls subroutines to interpolate a three-year time-series data,
#smooth mid-year time-series data, and calculate the metrics for the mid-year time-series data.
#The inputs are: 
#tmp (one-year-time-series-vector), 
#bnames (one-year-time-series-vector name),
#threshold (fill value for no data, 60b),
#snowcld (fill value for snow and cloud, 60b),
#outputs are:
#v_smooth (one-year smoothed vector),
#v_metrics (one-year metrics).
 
#;jzhu, 5/5/2011, use the program provided by Amy to do moving smooth and calculate the crossover
 
#;jzhu, 9/8/2011, ver9 processes the one-year-stacking file which includes ndvi and bq together.  


import numpy as np

from interpol_noextension_1y_vector import *

from wls_smooth import *

from user_metrics_nps_by1yr import *


def time_series_process_nps_oneyear(tmp,bq,bnames,threshold,snowcld):
   num_vmetrics=12 #number of metrics in vector vmetrics
   a=-100
   sfactor=0.01
   ratio=0.3  # number of valid points(not threshold or snowcld) of mid_year/number of total points of mid_year
   metrics_cal_threshold=0.4 #;when ndvi is less than metrics_cal_threshold, do not calculate metrics
   flg_metrics=0 # 0---not calculate metrics
   stnum=3  # make first stnum points up
   ednum=3  # make last ednum points up

   tmp_bn=np.copy(bnames)
   tmp_bn[:]='1_'
   tmp_bn=np.core.defchararray.add(tmp_bn,bnames)  #; add "1." in front of elements


   #;---- calls interpol_extension_1y_vector_ver9.pro to process one-year data, do one-year vector extension, then inpterpolate

   (tmp_interp,tmp_bq,tmp_bn,flg_metrics)=interpol_noextension_1y_vector(tmp,bq,tmp_bn,threshold,snowcld)


   if flg_metrics == 0 or flg_metrics == -1:   #; no not calculate metrics
      mid_interp=tmp_interp
      mid_smooth=tmp_interp
      mid_bq =tmp_bq
      mid_bname=tmp_bn
      vmetrics=np.zeros(num_vmetrics, dtype='float')
      vmetrics[:]=flg_metrics
       

   else:  #; calcualte metrics 


      #;----- calculate metrics-----------------------------

      tmp_smooth=wls_smooth(tmp_interp,2,2)
     
      mid_interp = tmp_interp
      mid_smooth = tmp_smooth
      mid_bq= tmp_bq
      mid_bname  = tmp_bn #; make it compabible to three-year data process

      mid_interp1 =( mid_interp +a )*sfactor

      mid_smooth1 =( mid_smooth +a )*sfactor
  
      vmetrics=user_metrics_nps_by1yr(mid_smooth1,mid_interp1, mid_bq, mid_bname, metrics_cal_threshold)

      #vmetrics=np.zeros(num_vmetrics, dtype='float')

      #vmetrics[:]=flg_metrics

   return (mid_smooth, vmetrics)

 






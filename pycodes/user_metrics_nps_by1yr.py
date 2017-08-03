#;user_metrics.pro 
#;Author: jiang zhu, 7/20/2017, jiang@gina.alaska.edu
#;This program calculates the metrics of a time-series vector.
#;inputs are v (smoothed vector),v2 (original vector),bn (band name vector).
#;output is out_v(a 12-element vector).
#;out_v=[onp,onv,endp,endv,durp,maxp,maxv,ranv,rtup,rtdn,tindvi,mflg]
#;The 12 elements are:
#;0=onp(time of onset of greenness),
#;1=onv(NDVI value at onset),
#;2=endp(time of end of greenness),
#;3=endv(NDVI value at end),
#;4=Durp(duration of greenness),
#;5=Maxp(Time of maximum NDVI),
#;6=maxv(Maximum NDVI Value),
#;7=ranv(range of NDVI values),
#;8=rtup(rate of grrenup),
#;9=rtdn(rate of senescense),
#;10=tindvi(time-integrated NDVI),
#;11=mflg(data valid flag,0--no-sense metrics,1--valid metrics)
#;jzhu, 5/5/2011, use program provided by Aym to calculate the moving average and crossover 

import numpy as np

from computemetrics_by1yr import *

from findday import * 

def user_metrics_nps_by1yr(ndvi, ndvi_raw, bq, bn, metrics_cal_threshold):
   #inputs:
   #;---ndvi is smoothed and scaled to 0 to 1 NDVI vector
   #;-- ndvi_raw is orginal scaled to 0 to 1 NDVI vector 
   #;---bq is quality of ndvi
   #;---bn is band name for ndvi
   #;---metrics_cal_threshold, define a threshold, only calculate the metrics if the maximun ndvi is greather than metrics_cal_threshold, default=0.4
   #output:
   #;--- out_v is the metrics

   #;---because data have convert from -4000 to 10000 to 0 to 200, 
   #;---if you want to get the NDVI, you need use equation ndvi=(scaled ndvi+a)*sfactor, where
   #;---sfactor=0.01, and a=-100

   sfactor=0.01
   a=-100.0
   threshold_val=0.1 #; better way is use half of maximun of ndvi, ndvi value, determines the sos and eos points

   #;assume normally greenness duration in Alaska is 12*7 days=84 days

   num_band=ndvi.shape[0]

   wl=[num_band-12,num_band-12]

   #;wl=[30,30] ;decided by Reed, B.C.Measure phenological variability from satellite imagery,1994, 703, J. vegetation Science 5
   #;jzhu, wl impacts the SOS and EOS, normally, sos is 102 days, eos is 280 days, days of noe green =102+ (365-280)=187
   #; 187/7=27, so choose wl=[28,30], because end of season sharply declines, use longer time average do not affect determine the location
   #; of EOS, longer average makes average more greather than data, so gurrantee the eos is corrrect.

   #;jzhu, 8/29, 2011, call determine_wl.pro to estimate wl for each ndvi
   #;wl=determine_wl(ndvi, threshold_val)

   bpy =num_band  #; num of band in one year, 42

   CurrentBand=7

   DaysPerBand=7  #; day interval between two consecituve bands =7 days

   #;---get the day between two 7-day band

   intv_day = int(bn[1][7:10]) -int(bn[0][7:10]) #;This is the interval days between two measurement weeks. The band name format is:n-yyyy-ddd-ddd.

   start_day =int(bn[0][7:10]) #; this is the first date of the first measurement week

   #;---out_v is used to store the metrics, 12 band

   out_v=np.zeros(12,dtype=np.float16) #; used to store metrics, initial value out_v(*)=0

   #;---inital metrics valid flag

   mflg=0    #; initial value 0, 0---not valid metrics, 1-- valid metrics


   metrics=computemetrics_by1yr(ndvi, ndvi_raw, bq, bn, wl,bpy,CurrentBand,DaysPerBand)

   onp  = metrics['SOST']

   onv  = metrics['SOSN']

   endp = metrics['EOST']

   endv = metrics['EOSN']

   #;---get additional condition to make sure the metrics calculation is resonable. default condition is
   #;---the end-of-greenness -stsrt-of-grenness must greater than 35 days. pay attention this condition
   if endp ==len(ndvi)-1 or onp == 0 or endp - onp <= 5:

      return out_v


   maxp=metrics['MaxT']

   maxv=metrics['MaxN']


   #;---continue to calculate other metrics

   mflg=1 #; valid metrics

   out_v[11]=1 #; valid metrics data flag


   #;---convert onp, endp, maxp into related day labels, because onp,endp,maxp are float data, they indicate exect day

   onpday = findday(bn, onp)  #;day

   endpday= findday(bn,endp)  #;day

   maxpday= findday(bn,maxp)  #;day


   #;if maxv-onv GE maxv-endv then begin
   #;ranv= maxv-onv                  ; unit ndvi                    
   #;endif else begin
   #;ranv=maxv-endv                  ; unit ndvi          
   #;endelse

   ranv =metrics['RangeN']

   rtup= metrics['SlopeUp']     #; positive, ndvi/day

   rtdnp=-metrics['SlopeDown']  #; negative, ndvi/day

   tindvi=metrics['TotalNDVI'] #;ndvi*day

   out_v[0]=onpday #;unit day
   out_v[1]=onv    #;normalized ndvi
   out_v[2]=endpday #;unit day
   out_v[3]=endv   #;normoalized ndvi
   out_v[4]=endpday-onpday #;unit day
   out_v[5]=maxpday #;unit day
   out_v[6]=maxv  #; normalized ndvi
   out_v[7]=ranv  #; normalized ndvi
   out_v[8]=rtup  #; slopeup, ndvi/day
   out_v[9]=rtdnp #;slopedown, ndvi/day 
   out_v[10]=tindvi  #; ndvi*day
 
   return out_v

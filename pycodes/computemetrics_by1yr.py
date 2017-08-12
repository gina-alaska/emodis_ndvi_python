#calcualte the metrics 
import numpy as np

from getforwardma import *

from getbackwardma import *

from getcrossover_percentage_extremeslope import *

from getsos import *

from geteos import *

from getmaxndvi import *

from gettotndvi import *

from getndvitodate import *

from getrange import *

from getslope import *


def computemetrics_by1yr(NDVI,ndvi_raw,bq,bn,wl,bpy,CurrentBand, DaysPerBand):
   #inputs:
   #NDVI---smoothed NDVI vector
   #ndvi_raw---raw NDVI vector
   #bq---quality vector
   #bn---band name vector for NDVI
   #wl---list define moving window wl=[wlb, wlh]
   #bpy---number of points in one year
   #CurrentBand---time interval between two points in NDVI, =7 
   #DaysperBand---ndvi 7-days data, DaysperBand=7
   #output:mMetrics
   #;jzhu, 9/21/2011, this program modified from computemetrics.pro,
   #;it inputs one-year ndvi time series and rerlated band name vectors,wl,bpy,currentband, and daysperband 
   #;ndvi is smoothed data, ndvi_raw is interpolated data

   nSize=NDVI.shape

   Time1=np.array( range(nSize[0]),dtype=np.int16 )

   #for 1D NDVI,

   Time=Time1

   # Calculate Forward/Backward moving average

   FMA=GetForwardMA(NDVI, wl[0])

   BMA=GetBackwardMA(NDVI, wl[1])


   #; Get crossover points (potential starts/ends)

   #mv_percent=0.2, user decide this value, 20% of maximun NDVI value

   mv_percent=0.2

   Starts=GetCrossOver_percentage_extremeslope(Time, NDVI, Time, FMA, mv_percent, bq, bpy, 'DOWN')

   Ends=GetCrossOver_percentage_extremeslope(Time, NDVI, Time, BMA, mv_percent, bq, bpy, 'UP')

   #; Determine start/end of season


   SOS=GetSOS(Starts, NDVI,bq,Time, bpy, FMA)     #;find the possible sos among the crossovers which is the most close to 20% up threshold point, guarentee possib sos > threshold,and this possible sos must be good point. 
                                                                                         
   EOS=GetEOS(Ends, NDVI, bq, Time, bpy,BMA)   #; find last 20% point, get the possibx which is the nearest to the last 20% point, compare the possibx and the last 20%point, pick the smaller point in the possibx and 20% point as possib point, then gurrantee this point is good point.

   #; Generate structures for Start/End of season

   Start_End = {'SOST':SOS['SOST'], \
                'SOSN':SOS['SOSN'], \
                'EOST':EOS['EOST'], \
                'EOSN':EOS['EOSN'], \
                'FwdMA':FMA, \
                'BkwdMA':BMA \
               }


   #;PRINT, 'COMPUTEMETRICS:NY:',ny
   #;   ny=n_elements(eos.eost)
   SOST = Start_End['SOST'][0]
   SOSN = Start_End['SOSN'][0]
   EOST = Start_End['EOST'][0]
   EOSN = Start_End['EOSN'][0]

   MaxND=GetMaxNDVI(ndvi_raw, Time, Start_End,bpy)             #;dayindex and related maximun ndvi value

   TotalNDVI=GetTotNDVI(NDVI, Time, Start_End,bpy,DaysPerBand) #; ndvi*day (it is a ndvi curve minus baseline ),
                                                               #; baseline( start to end) vector,
                                                               #; ndvi vector (start to end),
                                                               #; time vector (start to end).
                                                               #; GrowingSeasonT=GST, GrowingSeasonN=GSN, GrowingSeasonB=GSB)

   #NDVItoDate calcualte the integration of NDVI between start oof season SOST and currentBand index

   NDVItoDate=GetNDVItoDate(NDVI, Time, Start_End, bpy, DaysPerBand, CurrentBand) #; ndvi*day, nowT (dayindex),nowN

   #NDVItoDate has some problem, need figure out

   #NDVItoDate={'NDVItoDate':0.0,'NowT':0.0,'NowN':0.0}

   Slope=GetSlope(Start_End, MaxND, bpy, DaysPerBand) #;slope = ndvi/day
   
   Range=GetRange(Start_End, MaxND, bpy, DaysPerBand) #;range.ranget = day, range.rangeN = ndvi


   mMetrics ={
   'SOST':SOST, \
   'SOSN':SOSN, \
   'EOST':EOST, \
   'EOSN':EOSN, \
   'FwdMA': Start_End['FwdMA'], \
   'BkwdMA': Start_End['BkwdMA'], \
   'SlopeUp': Slope['SlopeUp'], \
   'SlopeDown':  Slope['SlopeDown'], \
   'TotalNDVI': TotalNDVI['TotalNDVI'], \
   'GrowingN':TotalNDVI['GSN'], \
   'GrowingT':TotalNDVI['GST'], \
   'GrowingB':TotalNDVI['GSB'], \
   'MaxT': MaxND['MaxT'], \
   'MaxN': MaxND['MaxN'], \
   'RangeT': Range['RangeT'], \
   'RangeN': Range['RangeN'], \
   'NDVItoDate': NDVItoDate['NDVItoDate'], \
   'NowT': NDVItoDate['NowT'], \
   'NowN': NDVItoDate['NowN'] }

   return mMetrics


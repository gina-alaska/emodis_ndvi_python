#
import numpy as np

def GetRange( Start_End, MaxND, bpy, DaysPerBand):


   #;
   #; This function calculates the ranges of the seasons both
   #; in time (length of season) and ndvi (ndvi range) whenever
   #; both a start and end are found, otherwise the length is
   #; set to zero
   #;

   FILL=-1.0

   #;DaysPerBand=365./bpy


   #;RangeT=(Start_End.EOST-Start_End.SOST)*DaysPerBand/365.
   #;RangeT=(Start_End.EOST-Start_End.SOST)/bpy
   #;
   RangeT=( Start_End['EOST']-Start_End['SOST'] )*DaysPerBand

   RangeN=MaxND['MaxN']-min(Start_End['EOSN'],Start_End['SOSN'])


   BadLength = np.where (Start_End['EOST'] < 0 or Start_End['SOST'] < 0 or RangeT < 0 )[0]

   nBad =len(BadLength)
 

   #;BadLength = where (RangeT LE 0 or RangeT GT DaysPerBand*bpy*1.5,nBad)

   if nBad > 0:

      RangeT[BadLength] = FILL

      RangeN[BadLength] = FILL

   Range={'RangeT':RangeT, 'RangeN':RangeN}

   return Range



#;this function use dayindex to find the day 
#inputs:
#band name vector
#dayindex_flt---float scalar
#output:
#x--day

import numpy as np

def findday(bandname, dayindex_flt):

    dayidx1= int(dayindex_flt)

    if dayidx1 == 0:
   
        fract=float(dayindex_flt)
   
    else:    

        fract = float(dayindex_flt) % int(dayidx1)


    if fract >0:  #have fract

        dayidx2=dayidx1+1

        day1st =  bandname[dayidx1][7:10].astype(int)

        day1ed =  bandname[dayidx1][11:14].astype(int)

        day1 =0.5*(day1st+day1ed)
 
        day2st=  int( bandname[dayidx2][7:10] )

        day2ed=  int( bandname[dayidx2][11:14] )

        day2=0.5*(day2st+day2ed)

        x=int( round( day1 +fract*(day2-day1) ) )

 
    else:  # no fract
  
        dayidx2=dayidx1

        dayst1 = int(bandname[dayidx1][7:10])

        dayed1 = int(bandname[dayidx1][11:14])

        x=int( round( 0.5*(dayst1+dayed1) ) )




    return x



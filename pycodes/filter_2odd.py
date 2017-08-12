#;this program filter out odd points in the vector v, one-year ndvi curve should be both sides are low and middle is hight.if ther are some points with very low values,they are considered as odd points, take them off and interpol them.
#;input, v---vector,output: returned vector named rtr. if minpoint-lowvalu > 0.4 take this point out
#;jzhu, 9/13/2011, this program get rif of 1 or 2 consecutive odd points,
#;odd points are defined they are 0.4 smaller than adjunctive points
#;diffval=0.4

import numpy as np

def filter_2odd( rin,uprate,downrate):

    #inputs:rin---vector, uprate--up_slope_threshold=0.25 ,downratre--down_slope_threshold=0.25
    #output:r
    
    r=np.copy(rin).astype('int')
    
    
    if min(rin) != max(rin): #do filting

       num=len(r) #; number of points in the vector r


       #;determine if the first or last points are odd point

       if ( r[0]-r[1] )/r[1] > uprate and ( r[0]-r[2] )/r[2] > uprate:
       
            r[0]=0.5*( r[1]+r[2] )


       if ( r[num-1] -r[num-2] )/r[num-2] > uprate and ( r[num-1]-r[num-3] )/r[num-3] > uprate:
           
            r[num-1]=0.5*( r[num-2]+r[num-3] )


       for k in range(0,num-3):  #; check four points to find the odd 1 point or 2 consecutive odd points

            #; one odd in three points
           
            cond1=( r[k]-r[k+1] )/r[k] > downrate and (r[k+2]-r[k+1])/r[k+2] > downrate

            cond2=( r[k+1]-r[k] )/r[k] > uprate and (r[k+1]-r[k+2])/r[k+2] > uprate

            if cond1 or cond2: 

                r[k+1]=0.5*( r[k]+r[k+2] )


    r=r.astype('uint8')

    return r



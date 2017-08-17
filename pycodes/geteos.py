#;jzhu, 8/1/2011. THis program modified from GetEOS2.pro. GetEOS2.pro picks the END of Season by thinking EOS occurs at where the NDVI is minimum. 
#;This program choose the point where slope of NDVI is smallest.
#;if eos_possib1 < 20% point, eos_possib2 = eos_possi1, otherwise eos_possb2 = 20%point,find a nearest point from eos_possb2 to 1, which is not snow point, 
#;this point is EOS
#;jzhu, 12/12/2011, modify from geteos_ver15.pro, uses different stragegy to pick up the final EOS among the crossover. First, find the last 20% point; then
#;find the possibx point which is defined as the crossover point which is the most closest to the 20% point; pick the smaller point between the possibx and 
#;the last 20% point as the possibx1, find the "good" last point between 0 to possibx1 as EOS.   

import numpy as np

def  GetEOS(cross,NDVI,bq,x,bpy,bma):
   # NDVI is 1D array, 
   FILL=-1.
   
   WinLast=int(0.5*bpy)  #end season must be greater than WinLast

   WinMax=int(0.9*bpy)  #end season must be less than WinMax

   lastidx=len(NDVI)-1 #index of the last element in NDVI

   EOST=np.zeros(1,dtype=np.int16)

   EOSN=np.zeros(1,dtype=np.float)

   EOST[0]=FILL

   EOSN[0]=FILL

   #0. initialize eosx, eosy

   eosx=lastidx

   eosy=NDVI[eosx]

    #;1.---- find the last 20% point, x20, y20
   c1=cross['T']==1
   c2=cross['X']>WinLast
   c3=cross['X']<WinMax
   idx20=np.where( c1&c2&c3 )[0]
 
   cnt1=len(idx20)
   
   #;2.----find the possibx among the crossover points possibx, possiby

   #;-----only consider crossover points for determine if the crossover is valid
   c1=cross['T']==0
   #c2=cross['X']>WinLast
   #c3=cross['X']<WinMax
   t0idx = np.where(c1&c2&c3)[0] #; t0--crossover type,0--crossover, 1--20% point, 2--extremeslope point
    
   t0cnt=len(t0idx)
 

   if cnt1 <= 0:  #; <3>  no valid 20% points
   
       if t0cnt <= 0: #<4> no valid 20% points or valid cross over points
       
           possibx=lastidx
       
           possiby=NDVI[possibx]
       
       else: #<4> no valid 20% points, have valid crossover points
       
           cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}
           
           possibx = cross_only['X'][0 ]
        
           possiby = cross_only['Y'][0 ] 
           
       #<4>

   else: # ; <3> have valid 20% points
       
       x20=cross['X'][ idx20[len(idx20)-1] ]

       y20=cross['Y'][ idx20[len(idx20)-1] ]
           
       if t0cnt <= 0: #<5> have valid 20% points, no valid cross over points
          
          possibx=x20
       
          possiby=y20
       
       else: #<5> have valid 20% points and valid cross over points

          cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}
          
          v1=min( abs(cross_only['X']-x20) ) 
                  
          NextEOSIdx=np.where( abs(cross_only['X'] - x20)  == v1 )[0]
 
          possibx = cross_only['X'][ NextEOSIdx[0] ]
     
          possiby = cross_only['Y'][ NextEOSIdx[0] ]
          
          if possibx > x20:  #;  make sure possible eos is equal or less than 20% point
        
              possibx=x20
           
              possiby=y20
           
       #<5>
                 
   #<3>
                         
   #4.  possiblx must greater than mxidxed and less than WinMax

   if possibx <= WinLast or possibx >= WinMax:  #; <6>
        
      eosx=lastidx

      eosy=NDVI[eosx]
        
         
   else:     # ;<6>
        
       #5. both possiblx and possiblx-1 are valid NDIV point, and possiblx is not the last point, then this is EOS

       if bq[int(possibx)] == 0 and bq[int(possibx)-1] == 0 and int(possibx)+1 <= lastidx:  #;<7>

            eosx=possibx

            eosy=possiby
         
       else:  #<7>; 6. find eos which is close to possiblx and is not snow point
         
            x20g = np.where( bq[ 0: int(possibx) ] == 0 )[0]
                   
            possibcnt=len(x20g)

            if possibcnt > 0: #<8>
         
                eosx = x20g[len(x20g)-1 ]
          
                eosy=NDVI[eosx]
         
            else: #<8>
         
                eosx=lastidx

                eosy=NDVI[eosx]
            #<8>
       #<7>
   #<6>

   EOST[0]=eosx

   EOSN[0]=eosy

   EOS={'EOST':EOST, 'EOSN':EOSN}

   return EOS


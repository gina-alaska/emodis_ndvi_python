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
   #;---get idx of maximun ndvi point
   num=len(NDVI)

   mxv=np.max(NDVI)
   
   mxidx=np.where(NDVI==mxv)[0]  # np.where(NDVI==mxv) is truple, get the first element of the truple

   mxidxst=mxidx[0]

   mxidxed=mxidx[len(mxidx)-1]

   lastidx=len(NDVI)-1 #index of the last element in NDVI

   # Calculation the slope of ndvi and bma for slope method

   nbMA=len(bma)

   #bSlope=np.zeros(nbMA-1,dtype=np.float)

   nNDVI=len(NDVI)

   EOST=np.zeros(1,dtype=np.int16)
   EOSN=np.zeros(1,dtype=np.float)
   EOST[0]=FILL
   EOSN[0]=FILL

   #0. initial eosx, eosy

   eosx=lastidx

   eosy=NDVI[eosx]

 
   #;1.---- find the last 20% point, x20, y20

   idx20=np.where(cross['T'] == 1)[0]

   cnt1=len(idx20)

   if cnt1 <= 0:  #; <3> if no 20% point, set the eosx and eosy as last point

       x20=lastidx

       y20=NDVI[x20]

   else:          # ; <3>

       #;---choose the last 20% point

       x20=cross['X'][ idx20[len(idx20)-1] ]

       y20=cross['Y'][ idx20[len(idx20)-1] ]



   #;2.----find the possibx among the crossover points possibx, possiby

   #;-----only consider crossover points for determine if the crossover is valid
 
   t0idx = np.where(cross['T'] == 0)[0] #; t0--crossover type,0--crossover, 1--20% point, 2--extremeslope point
    
   t0cnt=len(t0idx)

   if t0cnt < 1: #; <0> no crossover
     
       possibx=lastidx

       possiby=NDVI[possibx]

   else:        # ;<0> have cross  over point
      
       cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}

       NextIdx=np.where( np.logical_and( cross_only['X'] > mxidxed, cross_only['X'] < lastidx ) )[0]

       nNext=len(NextIdx)


       if nNext > 0:   #;<1> have possiblex,<1>

              #;pick the one which has the minimun slope ----------

              NextEOSIdx=np.where( abs(cross_only['X'][NextIdx] - x20)  == min( abs(cross_only['X'][NextIdx]-x20) ) )[0]

              #;-----------------------------------------------------------

              possibx = cross_only['X'][ NextEOSIdx[0] ]

              possiby = cross_only['Y'][ NextEOSIdx[0] ]
         
       else: #;<1>

              possibx=lastidx

              possiby=NDVI[possibx]


   #;3.-----compare x20 and possibx for EOS, pick the smaller one


   if possibx > x20:  #;  make sure possible eos is equal or less than 20% point
        
      possibx=x20
           
      possiby=y20


   #4.  possiblx must greater than mxidxed and less than last point

   if possibx <= mxidxed or possibx >= lastidx:  #; <5>
        
      eosx=lastidx

      eosy=NDVI[eosx]
        
         
   else:     # ;<5>
        

       #v=possibx % int(possibx)
       #if ( v == 0 and bq[ int(possibx)]  == 0 and bq[int(possibx)-1] == 0 and int(possibx)-1 >= 0 ) \
       #or ( v != 0 and bq[ int(possibx)]  == 0 and bq[int(possibx)+1] == 0 and int(possibx)+1 <= lastidx ):  #;found EOS <4>

       #5. both possiblx and possiblx-1 are valid NDIV point, and possiblx is not the last point, then this is EOS

       if bq[int(possibx)] == 0 and bq[int(possibx)-1] == 0 and int(possibx)+1 <= lastidx:  #;<4>

            eosx=possibx

            eosy=possiby
         
       else:  #<4>; 6. find eos which is close to possiblx and is not snow point
         
            x20g = np.where( bq[ 0: int(possibx) ] == 0 )[0]
                   
            possibcnt=len(x20g)

            if possibcnt > 0: #<6>
         
                eosx = x20g[len(x20g)-1 ]
          
                eosy=NDVI[eosx]
         
            else: #<6>
         
                eosx=lastidx

                eosy=NDVI[eosx]
            #<6>
       #<4>
   #<5>

   EOST[0]=eosx

   EOSN[0]=eosy

   EOS={'EOST':EOST, 'EOSN':EOSN}

   return EOS


#
import numpy as np

def GetSOS(cross, NDVI, bq, x, bpy, FMA):

   #; These numbers are the window (*bpy) from the
   #; current SOS in which to look for the next SOS
   #; jzhu, 9/12/2011, found SOS and EOS is very snesitive to the windows range of moving average.
   #; getSOS2.pro choose the the sos from the candidate point with minimun ndvi, try to use maximun slope difference to determine the sos
   #; jzhu, 9/23/2011, cross includes crossover, 20% points, and maxslope point, pick reasenable point as SOS among cross
   #;if sos_possib1 > 20% point, sos_possib2 = sos_possi1, otherwise sos_possb2 = 20%point,find a nearest point from eos_possb2 to 1, which is not snow point,this point is SOS
    
   FILL=-1.
   
   WinFirst=int(0.5*bpy)  #start season must less than WinFirst

   WinMin=int(0.1*bpy)    #start season must be greater than WinMin

   lastidx=len(NDVI)-1  #lastidx

   SOST=np.zeros(1, dtype=np.int16)

   SOSN=np.zeros(1, dtype=np.float)

   SOST[0]=FILL
   
   SOSN[0]=FILL

   #0. initialize sosx and sosy

   sosx=0

   sosy=NDVI[sosx]


   #1.find valid 20% points. t=1 means the point is 20% point
 
   c1=cross['T']==1
   c2=cross['X']>WinMin
   c3=cross['X']<WinFirst
   idx20=np.where( c1&c2&c3 )[0]
   
   cnt1=len(idx20)
   
   #2.find crossover points, t=0 means the point is crossover point
   
   c1=cross['T']==0
   #c2=cross['X']>WinMin
   #c3=cross['X']<WinFirst
   t0idx=np.where( c1&c2&c3 )[0]

   t0cnt=len(t0idx)
   
   
   if cnt1 <= 0:   #; <2>  no valid 20% points
       
       
       if t0cnt <=0: #<3> no valid 20% point or valid crossover point

           possibx=0

           possiby=NDVI[possibx]
       
       else: #<3> no valid 20%, but have valid cross over points       
       
           cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}
           
           lst=len(cross_only['X'])-1 
              
           possibx = cross_only['X'][lst]
        
           possiby = cross_only['Y'][lst]
           
           
       #<3>
           
   else: #; <2> have valid x20 points
              
           x20=cross['X'][idx20[0] ]

           y20=cross['Y'][idx20[0] ]

           if t0cnt<=0: #<4> have valid 20% points, no valid crossover point

               possibx=x20

               possiby=y20
           
           else: #<4> have valid 20% point and valid crossover points

               cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}
               
               v1=min( abs(cross_only['X']-x20 ) )
                
               FirstSOSIdx =np.where( abs( cross_only['X']-x20 ) == v1 )[0]
             
               possibx = cross_only['X'][ FirstSOSIdx[ len(FirstSOSIdx)-1 ] ]
        
               possiby = cross_only['Y'][ FirstSOSIdx[ len(FirstSOSIdx)-1 ] ]
               
               if possibx < x20:   #;  make sure possiblx equal or greater than x20
        
                  possibx=x20

                  possiby=y20 
              
        #<4>
   #<2>
        
   #4. the sos must not <=2 and must greater than WinFirst*bpy

   if possibx <= WinMin or possibx >= WinFirst:    #;<5>
        
        sosx=0

        sosy=NDVI[sosx]

   else:      # ;<5>
        
        #5. possiblex and possiblex+1 are valid NDVI points and possible+1 is less than lastidx, it is sosx

        if bq[int(possibx)] == 0 and bq[int(possibx)+1] == 0 and int(possibx)+1 <= lastidx:  #;<4>      

             sosx=possibx

             sosy=possiby

        else:     #;<4>  #6. possibx is snow, found true sosx between possibx+1 to mxidxst <4>
         
             x20g = np.where( bq[ int(possibx)+1 : len(bq)-1  ] == 0 )[0]
              
             possibcnt=len(x20g)

             if possibcnt > 0: #<6>
         
                sosx= int(possibx)+1+x20g[0]

                sosy=NDVI[sosx]
         
             else: #<6>
         
                sosx=0

                sosy=NDVI[sosx]
             #<6>
        #<4>
   #<5>
     
   SOST[0]=sosx

   SOSN[0]=sosy
          
   SOS={'SOST':SOST,'SOSN':SOSN}   

   return SOS


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
   WinFirst=0.75 #;the maximum start season must less than WinFirst*bpy
   WinMin=0.5
   WinMax=1.5

   #;---get idx of maximun ndvi point
   num=len(NDVI)

   mxidx=np.where(NDVI == max(NDVI))[0]
  
   mxidxst=mxidx[0]

   mxidxed=mxidx[len(mxidx)-1]

   lastidx=num-1 #; lastidx

   nFMA=len(FMA)

   nNDVI=len(NDVI)

   SOST=np.zeros(1, dtype=np.int16)
   SOSN=np.zeros(1, dtype=np.float)
   SOST[0]=FILL
   SOSN[0]=FILL

   #0. initial sosx and sosy

   sosx=0

   sosy=NDVI[sosx]


   #1.find the correct 20% point x20,y20
 
   idx20=np.where(cross['T'] == 1)[0]

   cnt1=len(idx20)

   if cnt1 <= 0:   #; <2> if no 20% point, set sosx as possiblx

       x20=0

       y20=NDVI[x20]


   else:           #; <2> compare possibx with 20% point,<2>

       #;--when more than one 20% points, choose the first one
       x20=cross['X'][ idx20[0] ]

       y20=cross['Y'][ idx20[0] ]



   #2.find possibx cross over point in cross_only possibx, possiby

   t0idx = np.where(cross['T'] == 0)[0] #; t0--crossover type

   t0cnt=len(t0idx)

   if t0cnt < 1:   #; <0> no  crossover points, possiblex=0

       possibx=0

       possiby=NDVI[possibx]
     
   else:          # ; <0> have crossover points,looking for possiblex
     
       cross_only={'X':cross['X'][t0idx], 'Y':cross['Y'][t0idx], 'S':cross['S'][t0idx],'T':cross['T'][t0idx],'C':cross['C'][t0idx], 'N':t0cnt}
       
       
       FirstIdx=np.where( np.logical_and(cross_only['X'] < WinFirst*bpy, cross_only['X'] < mxidxst) )[0]

       nFirstSOS=len(FirstIdx) #number of points of cross over which is not great than WinFirst*bpy

       #I think possibx never houldn't be great than 28 for total 42 band


       # get possiblex

       if(nFirstSOS > 0):      #; <1> have possiblex


           #g. use the crossover point which is the most close to the 20% point as possibx

           FirstSOSIdx =np.where( abs( cross_only['X'][FirstIdx]-x20 ) == min( abs(cross_only['X'][FirstIdx]-x20 ) ) )[0]
             
           possibx = cross_only['X'][ FirstSOSIdx[ len(FirstSOSIdx)-1 ] ]
        
           possiby = cross_only['Y'][ FirstSOSIdx[ len(FirstSOSIdx)-1 ] ]

       else:                  # ;<1> not possiblex

           possibx=0

           possiby=NDVI[possibx]


          



   #3. compare x20 and possiblex, pick greater one


   if possibx < x20:   #;  make sure possiblx equal or greater than x20
        
        possibx=x20

        possiby=y20

        
   #4. the sos must not <=2 and must greater than WinFirst*bpy


   if possibx <= 2 or possibx >= WinFirst*bpy:    #;<5>
        
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


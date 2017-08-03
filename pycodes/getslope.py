#calcualte the slope
import numpy as np

def GetSlope( Start_End, MaxND, bpy, DaysPerBand):

   #;
   #; This function calculates the slope-up and slope-down for
   #; ndvi data using start, end and maxnd for each year that
   #; all three quantities exist.
   #;

   FILL=-1.0
   #; DaysPerBand=365./bpy         #; This is used to scale results to /day

   sSize=Start_End['SOST'].shape

   ny=sSize[0]


   SlopeUp   = np.zeros(sSize)+FILL
   SlopeDown=  np.zeros(sSize)+FILL

   #;
   #; Up slope
   #;
   NotZero=np.where( Start_End['SOST']-MaxND['MaxT'] < 0)[0]

   nz=len(NotZero)

   FillIdx=np.where(Start_End['SOST'] == FILL or MaxND['MaxT'] == FILL)[0]
  
   nF=len(FillIdx)

   if nz > 0:  #<1>
      SlopeUp[NotZero]=(Start_End['SOSN'][NotZero]-MaxND['MaxN'][NotZero])/ \
                       (Start_End['SOST'][NotZero]-MaxND['MaxT'][NotZero])/ \
                        DaysPerBand
   #<1>
   if (nF > 0): #<2>
      SlopeUp[FillIdx]=FILL
   #<2>

   #;
   #; Down Slope
   #;

   NotZero=np.where(Start_End['EOST']-MaxND['MaxT'] > 0)[0]

   nz=len(NotZero)

   FillIdx=np.where(Start_End['EOST'] == FILL or MaxND['MaxT'] == FILL)[0]

   nF=len(FillIdx)


   #;
   #; Take absolute value of slope down.  Negative slope is implied.
   #; This is done to because our FILL value is set to a negative number
   #; and we don't want any ambiguities.
   #;
   if nz > 0: #<3>

      SlopeDown[NotZero]=(Start_End['EOSN'][NotZero]-MaxND['MaxN'][NotZero])/ \
                         (Start_End['EOST'][NotZero]-MaxND['MaxT'][NotZero])/ \
                         DaysPerBand
   #<3>

   if (nF > 0): #<4>
      SlopeDown[FillIdx]=FILL
   #<4>

   Slope={'SlopeUp':SlopeUp, 'SlopeDown':SlopeDown}

   return Slope


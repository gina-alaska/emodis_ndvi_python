#
import numpy as np

from int_tabulated import *

def GetTotNDVI(NDVI, Time, Start_End, bpy, DaysPerBand):
   #NDVI---1D numpy array
   FILL=-1.0
   nSize=NDVI.shape
   sSize=Start_End['SOST'].shape
   if nSize[0] == sSize[0]:
      ny=sSize[sSize[0]]
   else:
      ny = 1

   ny = 1

   #DaysPerBand=7 days

   SeasonLength=Start_End['EOST'] - Start_End['SOST']
 
   a=np.where(SeasonLength == 0 )[0]

   na=len(a)

   if na>0:

   #if SeasonLength[0] == 0:

       SeasonLength_tmp=-1.0e-6

       BaseSlope=(Start_End['EOSN']-Start_End['SOSN'])/SeasonLength_tmp

   else:

       BaseSlope=(Start_End['EOSN']-Start_End['SOSN'])/SeasonLength


   BaseInt=Start_End['SOSN']-Start_End['SOST']*BaseSlope

   #;
   #; 1-D Data, ie a point as in
   #;


   x=np.arange(len(NDVI))

   icount=0

   TotalNDVI=np.zeros(ny)+FILL

   for i in range(0, ny): #<0>

       if SeasonLength[i] > 0 and SeasonLength[i] < bpy:  #<1>

            XSeg=    Time[ Start_End['SOST'][i] : Start_End['EOST'][i] ]

            NDVILine=NDVI[ Start_End['SOST'][i] : Start_End['EOST'][i]  ]

            if  XSeg[0] != Start_End['SOST'][i]:  #<2>

                XSeg=     np.concatenate( [ np.array([ Start_End['SOST'][i] ]), XSeg ] )

                NDVILine= np.concatenate( [ np.array([ Start_End['SOSN'][i] ]), NDVILine ] )
            #<2>

            if XSeg[len(XSeg)-1] != Start_End['EOST'][i]: #<3>

                XSeg=    np.concatenate( [ XSeg, np.array([Start_End['EOST'][i] ]) ] )

                NDVILine= np.concatenate( [ NDVILine, np.array([Start_End['EOSN'][i]]) ] )
            #<3>


            BaseLine=XSeg*BaseSlope[i]+BaseInt[i]

            #get rid of reduplicated point and sort the XSeg

            XSeg, index = np.unique(XSeg, return_index=True)

            NDVILine=NDVILine[index]

            BaseLine=BaseLine[index]
         
            IntNDVI=Int_Tabulated(XSeg, NDVILine)

            IntBase=Int_Tabulated(XSeg, BaseLine)

            TotalNDVI[i]=(IntNDVI-IntBase)*DaysPerBand



            if icount == 0: #<4>
               GSN=NDVILine
               GST=XSeg
               GSB=BaseLine

            else: #<4>
               GSN=np.concatenate([GSN, NDVILine])
               GST=np.concatenate([GST, XSeg])
               GSB=np.concatenate([GSB, BaseLine])
            #<4>
           
            icount=icount+1
         
       else: #<1>

            TotalNDVI[i]=FILL
            GSB=0
            GSN=0
            GST=0
       #<1>
  
   #<0>

   TotalNDVI={'TotalNDVI':TotalNDVI, \
              'GSB':GSB, 'GSN':GSN, 'GST':GST}

   return TotalNDVI


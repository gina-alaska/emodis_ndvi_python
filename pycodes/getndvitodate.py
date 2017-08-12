
import numpy as np

from int_tabulated import *

def GetNDVItoDate(NDVI, Time, Start_End, bpy, DaysPerBand, CurrentBand):
   #;
   #;jzhu,8/9/2011,This program calculates total ndvi integration (ndvi*day) from start of season to currentband, the currentband is the dayindex of interesting day.
   #
   FILL=-1.0

   ny=1

   #;DaysPerBand=365./bpy

   NowT=CurrentBand   #CurrentBand is the index of NDVI, the index start from 0

   NowN=NDVI[NowT]

   SeasonLength=NowT-Start_End['SOST'][0]

   NDVItoDate=np.zeros(ny)+FILL


   if SeasonLength < 0:

        SeasonLength = FILL

   if SeasonLength > 0 and SeasonLength < bpy:  #<2>
        #index range
        segl=int(np.ceil(Start_End['SOST'][0]))

        segh=int(np.floor(NowT )) + 1

        XSeg=     Time[ segl: segh ] #Xseg[Start_End['SOST'][0]:NowT]

        NDVILine= NDVI[ segl : segh ]

        #if  XSeg[0] != Start_End['SOST'][0]:  #<3>

        #          XSeg  =    np.concatenate([ np.array( [Start_End['SOST'][0] ] ), XSeg])

        #          NDVILine = np.concatenate([ np.array([ Start_End['SOSN'][0] ] ), NDVILine])
        #<3>


        #if XSeg[len(XSeg)-1] != NowT : #<4>

        #          XSeg  =   np.concatenate( [XSeg,     np.array([NowT]) ] )

        #          NDVILine= np.concatenate( [NDVILine, np.array([NowN]) ] )

        #<4>


        BaseLine=XSeg*0+Start_End['SOSN'][0]

        # get rid of duplicated point and sort the XSeg

        XSeg, index=np.unique(XSeg,return_index=True)

        NDVILine=NDVILine[index]

        BaseLine=BaseLine[index]

        IntNDVI=Int_Tabulated(XSeg, NDVILine)

        IntBase=Int_Tabulated(XSeg, BaseLine)

        NDVItoDate[0]=(IntNDVI-IntBase)*DaysPerBand

   else:  #<2>

        NDVItoDate[0]=FILL

   NDVItoDate={'NDVItoDate':NDVItoDate[0],'NowT':NowT,'NowN':NowN}

   return NDVItoDate
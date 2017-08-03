import numpy as np

def GetMaxNDVI( NDVI, Time, Start_End, bpy):
   #inputs:
   #NDVI----NDVI
   #TIME----
   FILL=-1.0

   ndSize=NDVI.shape

   nSize=Start_End['SOST'].shape

   if ndSize[0] == nSize[0]:

      nSeasons=nSize[nSize[0]]
   else:
       nSeasons=1


   MaxN=np.zeros(nSeasons)+FILL
   MaxT=np.zeros(nSeasons)+FILL

   for i in range(nSeasons):

       if Start_End['EOST'][i] > Start_End['SOST'][i]  and \
          Start_End['EOST'][i]-Start_End['SOST'][i] < bpy:

            MaxN[i]=max(NDVI[int(Start_End['SOST'][i]):int(Start_End['EOST'][i])])

            MaxIdx= np.where( NDVI[int(Start_End['SOST'][i]):int(Start_End['EOST'][i])] ==  MaxN[i] )[0]

            MaxT[i]=MaxIdx[0]+int(Start_End['SOST'][i])

       else:
            MaxN[i] = FILL
            MaxT[i] = FILL
       
   


   MaxND={'MaxN':MaxN, 'MaxT':MaxT}

   return MaxND


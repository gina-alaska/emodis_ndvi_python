import numpy as np

def GetForwardMA( In, wl ):
    #In is 1D array, WL is scalar variable. forwrad circular moving means shift toward higher index
    InSize=In.shape
    NSize=InSize[0]
    nb=NSize

    Forward=np.zeros(nb, dtype=np.float16)
    #extend head of the vector with wl-1 points from the tail of the vector. 
    tmp=np.roll(In, wl-1)

    tmp=np.concatenate((tmp,tmp[0:wl-1]))
 
    for i in range( 0,nb ):

       Forward[i]=tmp[i:i+wl-1].sum()

    Forward=Forward/wl

    return Forward


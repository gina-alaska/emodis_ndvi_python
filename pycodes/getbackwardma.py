import numpy as np

def GetBackwardMA( In, wl ):

    InSize=In.shape
    NSize=InSize[0]
    nb=NSize

    Backward=np.zeros(nb, dtype=np.float16)

    # Apply moving averages based on number of dimensions (1-3)

    tmp=np.roll(In, -(wl-1))

    tmp=np.concatenate( ( tmp[nb-(wl-1):nb],tmp ) )

 
    for i in range(0, nb):
 
       Backward[i]=tmp[i:i+wl-1].sum()
 
   

    Backward=Backward/wl

    return Backward

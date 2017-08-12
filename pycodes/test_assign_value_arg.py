#This test program test if I can assign a value to a arg

import numpy as np

import datetime

def fundouble(x):
     
    x = x*2

    return x



a1=np.random.rand(10000)

b1=np.random.rand(10000)

num=a1.shape[0]  

print(datetime.datetime.now())


#for i in range(num):
   
#    x=fundouble(a1[i])

for x in np.nditer(a1):    

    x=fundouble(x)


print(datetime.datetime.now())

#;This program realize weighted-least-squre smooth algorithm original developed by Daniel L. Swets,2001
#;inputs:
#v---vector
#numbf---number of points before current point, 
#numaf---number of points after current point,
#;output
#y---smoothed vector
#;jzhu, 2/8/2011

import numpy as np

def wls_smooth( v, numbf, numaf):

   y=np.copy(v)        

   if min(v) != max(v):  #;do smooth
      #;---produce a temperary vector which adds  last num_bf points of the vector before and
      #; add first num_af points of the vector to the end

      num = len(v)

      numtmp=numbf+num+numaf

      tmpv =np.zeros(numtmp,dtype='float')

      x =np.arange(numtmp)


      tmpv[0:numbf]= v[num-numbf:num]

      tmpv[numbf:numbf+num]=v

      tmpv[numbf+num:numtmp]=v[0:numaf]



      #;--- calculate weight, localpeal=1.5, localsloping=0.5, local valley=0.005
      #;-- the weights of the first and last points are assigned to 0.5

      w =np.zeros(numtmp,dtype='float') #; store weight

      w[:] =0.5  #; default value=0.5

      for j in range(1, numtmp-1): 

          #;--- comapre j-1,j, and j+1 to assign weight

          if tmpv[j] > tmpv[j-1] and tmpv[j] > tmpv[j+1]:

                w[j]=1.5

          else:

                if tmpv[j] < tmpv[j-1] and tmpv[j] < tmpv[j+1]:

                      w[j]=0.005      

      #;------ calculate y


      for j in range(numbf,numbf+num):


          sw=sum(w[j-numbf:j+numaf])

          sy=sum(w[j-numbf:j+numaf]*tmpv[j-numbf:j+numaf] )

          sx=sum(w[j-numbf:j+numaf]*x[j-numbf:j+numaf] )

          sxy=sum(w[j-numbf:j+numaf]*x[j-numbf:j+numaf]*tmpv[j-numbf:j+numaf] )

          sxsqr=sum(w[j-numbf:j+numaf]*x[j-numbf:j+numaf]*x[j-numbf:j+numaf] )

          b =(sw*sxy-sx*sy)/(sw*sxsqr-sx*sx)

          a=(sy-b*sx)/sw

          y[j-numbf]=a+b*x[j]

   return y


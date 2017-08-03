#;this program to interpolate.
#inputs are: v, xin, xout.
#output is y.
#v is input vector, xin and xout are indix vectors.
#y is output vector.

import numpy as np

def interpol_line100b_v2(v, xin, xout):

    #;convert v,xin,xout from type into float

    v=v.astype('float')

    idx=np.sort(v)   #from small to large

    #; use the most small three points average

    fillx = np.mean([ idx[0], idx[1] ])

    numout=len(xout)

    y=np.zeros(numout,dtype=np.float)   #; store output

    numin=len(xin)

    #;--- interpol points from xout(0) to xin(0)

    st_num=xin[0]-xout[0]

    if st_num > 0:

       #;fillx=byte( fix( (randomu(1,st_num))*2 )+100 )
       #;idx=sort(v)
       #; use the most small three points average
       #;fillx=mean([ v(idx(0)), v(idx(1)) ] )
       #;fillx=min(v)

       y[ xout[0]:xin[0]]=fillx

    
    #--- set y(xin(0) 

    #y[xin[0]] = v[0]

    #process points from xin(0) to xin(numin-1)
    
    for j in range( numin-1):  #processs 

        if xin[j+1] - xin[j] > 1: #<1> xin(j) and xin(j+1) are not adjunctive

             b=( v[j + 1 ] - v[ j ] ) / ( float(xin[j+1]) -float(xin[j])  ) 

             a=  v[ j ]  - b*xin[j]


             for k in range( xin[j], xin[j+1] ):

                   y[ k ]= a+b*xout[k] 

             y[xin[j+1]]=v[j+1]
 
        else:  #<1> xin(j) and xin(j+1) are adjunctive

              y[xin[j]]= v[j]

              y[xin[j+1]]=v[j+1]    

    #;--- process points xin(len(xin)) and after

    #;--- fill with the last v(xin(numin-1)

    #;for k=xin(numin-1)+1, xout(numout-1) do begin

    #;y(k)=v(numin-1 )

    #;endfor

    #;----fill randomly 100b to 101b for xin(numin-1)+1 to xout(numout-1)

    ed_num=xout[numout-1]-xin[numin-1]

    if ed_num > 0:

         #;fillx=byte( fix( (randomu(1,ed_num))*2 )+100 )
         #;idx=sort(v)
         #; use the most small three points average
         #;fillx=mean([ v(idx(0)), v(idx(1)) ] )
         #;fillx=min(v)

         y[xin[numin-1]+1:xout[numout-1]+1]=fillx 

    
    #;---- convert negative value points into randomly 100B to 101B

    idxneg=np.where(y < 100)

    cntneg=len(idxneg[0])

    if cntneg > 0:

         y[idxneg]=fillx
     

    #;--- output y

    return y 



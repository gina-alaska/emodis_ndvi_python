import numpy as np

from multiprocessing import Pool

def func1(t):
    #t is a tuple, it includes three arrary

    a=t[0]
    b=t[1]
    c=t[2]
    m=a+b
    n=a+b-c
  
    return m,n

def func2(a,b,c):
    #t is a tuple, it includes three arrary

    #a=t[0]
    #b=t[1]
    #c=t[2]
    m=a+b
    n=a+b-c

    return m,n


def get_element(a,i):

    #a is a np.array, return a element a[i]

    return a[i]

def main():

    a=np.array([1, 2,  3, 4, 5,6,7,8,9])
    b=np.array([11,12,13,14,15,16,17,18,19])
    c=np.array([111,112,113,114,115,116,117,118,119])

    #apply processor

    p=Pool(5)

    i=1

    a1=get_element(a,i)

    b1=get_element(b,i)

    c1=get_element(c,i)

    t=(a1,b1,c1)

    rst=func2( *t  )


    #rst=p.map(func1,( get_element(a,i), get_element(b,i), get_element(c,i) for i in range(10) ) )

    #rst=p.map(func1, (get_element(a,1), get_element(b,1), get_element(c,1)) )

    t1=(a1,b1,c1)

    t2=( get_element(a,2),get_element(b,2),get_element(c,2) )

    num=a.shape[0]

    xx= [(get_element(a,i),get_element(b,i),get_element(c,i)) for i in range(num)]


    rst=p.map(func1,xx )
    
    indices=range(9)

    r1=np.zeros(9)

    r2=np.zeros(9)

    rst1=np.array(rst)

    r1[indices],r2[indices]=rst1[indices,0],rst1[indices,1]


    print(rst)

    return 0

if __name__=='__main__':

    main()

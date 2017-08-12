from multiprocessing import Pool
import sys
def f(x):
    return (x, x*x)


def main():
    
    print(sys.argv)



    l=[None]*12

    #with Pool(5) as p:
    p=Pool(5)
    rst=p.map(f,range(12) )
    #[l[x] for x in range(12)]=rst, not work!
    #for x in range(12):
    #  l[x]=rst[x]
    
    #rst=[f(x) for x in range(12)]
    print(rst) 

if __name__=='__main__':

    main()	

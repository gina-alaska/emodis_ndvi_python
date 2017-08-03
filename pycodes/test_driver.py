#test function

import pickle

from cutoff_interp_v2 import *


def test_save(fname,dic):
    f=open(fname,'w')
    pickle.dump(dic,f)
    f.close()

def test_load(fname):
    f=open(fname,'r')
    dic=pickle.loads(f.read())
    f.close()
    return dic


fname='cuttoff.txt'

dic=test_load(fname)

x=cutoff_interp_v2(dic['mid_year'],dic['mid_year_bq'])
		





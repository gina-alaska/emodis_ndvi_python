#This python script is modified from oneyear_data_layer_subset_good.pro
#This routine open one year files defined in file lists, stack these file, subset, and fill bad data with -2000
#input arguments are flist_ndvi, flist_bq, ul_lon,ul_lat,lr_lon,lr_lat
#;inputs: yyyy_flist_ndvi----file list for one year *ndvi.tif,
#;        yyyy_flist_bq -----file list fro one year *nvdi_bq.tif
#;        ul-----upper left coordinate in unit of degree in geographic coordinates,WGS84
#;        lr-----lower right cordinate in unit of degree in geographic coordinates,WGS84
#;        data_ver_flg------, 0-old version data,1-new version data


import sys
import os
import platform
from read_ndvi import *
import raster_process as rp

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 7:
  print "input arguments are: flist_ndvi, flist_bq, ulx,uly,lrx,lry"
  sys.exit(1)
 

flist_ndvi=sys.argv[1]

flist_bq=sys.argv[2]

ulx=float(sys.argv[3])

uly=float(sys.argv[4])

lrx=float(sys.argv[5])

lry=float(sys.argv[6])


#;test
#;ul in deg, minute, secons= 173d 0' 0.00"W, 72d 0' 0.00"N
#;lr in deg, minute, second= 127d59'56.82"W, 54d 0' 0.07"N
#;if do not want subsize the data, just input 0,0,0,0 for ul_lon,ul_lat,lr_lon,lr_lat, respectively.
#;wrkdir='/home/jiang/nps/cesu/modis_ndvi_250m/wrkdir/'

#;flist_ndvi='/mnt/jzhu_scratch/EMODIS-NDVI-DATA/wrk/ver_new_201107/2008/flist_ndvi'
#;flist_bq = '/mnt/jzhu_scratch/EMODIS-NDVI-DATA/wrk/ver_new_201107/2008/flist_bq'

#;flist_ndvi='/raid/scratch/cesu/eMODIS/ver_old/2008/flist_ndvi'
#;flist_bq='/raid/scratch/cesu/eMODIS/ver_old/2008/flist_bq'

#;flist_ndvi='/home/jiang/nps/cesu/modis_ndvi_250m/wrkdir/2010/2010_flist_ndvi'
#;flist_bq = '/home/jiang/nps/cesu/modis_ndvi_250m/wrkdir/2010/2010_flist_bq'
#;ul=[-173.0d,72.0d]
#;lr=[-127.999116667d,54.000019444d]

#;set path and start envi
#;ENVI, /RESTORE_BASE_SAVE_FILES
#;PREF_SET, 'IDL_PATH', '<IDL_DEFAULT>:+~/nps/cesu/modis_ndvi_250m/bin', /COMMIT
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

if platform.system() == 'Windows':
   sign='\\'
else:
   sign='/'



#---- read these two lists into flist and flist_bq

u1=open(flist_ndvi,'r')

u2=open(flist_bq ,'r')

#---- count the number of lines in the flist files

#total_line_count = sum(1 for line in open("filename.txt"))

#total_line_count = sum(1 for line in open("filename.txt"))

#---- get the file names into the list

flist=u1.readlines()

flist=[x.rstrip('\n') for x in flist]

flistbq=u2.readlines()

flistbq=[x.rstrip('\n') for x in flistbq]

num=len(flist)

#---- get workdir and year from mid-year file

#p =strpos(flist(1),sign,/reverse_search)

#len=strlen(flist(1))

wrkdir=os.path.dirname(flist[0])


filen =os.path.basename(flist[0])


#;-----use file header to determine the 

if filen.find('MT3RG_') == True:

    data_ver_flg=0 
else:

    data_ver_flg=1


if data_ver_flg == 0:

    year=filen[6:9]   #MT3RG_2008_141-147_250m_composite_ndvi.tif

else:

    year=filen[13:17]  #AK_eMTH_NDVI.2008.036-042.QKM.VI_NDVI.005.2011202142526.tif


#;---- define a struc to save info of each file

#;p={flists,fn:'abc',sn:0,dims:lonarr(5),bn:0L}

#;x=create_struct(name=flist,fn,'abc',fid,0L,dims,lonarr(5),bn,0L)

#x={flist,fn:'abc',bname:'abc',fid:0L,dims:lonarr(5),pos:0L}

#flista=replicate(x,num) ;save ndvi data files

#flistq=replicate(x,num) ; save ndvi_bq data files

#;---- go through one year ndvi and ndvi_bq data files

First_Flag=True

for j in range(0L, num):

   fn_ndvi = flist[j]

#;---- for old data name

   if data_ver_flg == 0:
      str1='composite_ndvi'
      str2='composite_ndvi_bq'
      p1=fn_ndvi.rfinid(sign)
      tmpbname=fn_ndvi[p1+7:p1+19]  # for old data, its name looks like:MT3RG_2008_253-259_250m_composite_ndvi.tif

   else:
#;---- for new data name

     str1='.VI_NDVI.'
     str2='.VI_QUAL.'
     p1=fn_ndvi.rfind(sign)
     tmpbname=fn_ndvi[p1+14:p1+26]   #for new data, its name looks like:eMTH_NDVI.2008.029-035.QKM.VI_NDVI.005.2011202084157.tif




   p=fn_ndvi.find(str1)

   length=len(fn_ndvi)

   file_hdr=fn_ndvi[0:p]

   file_end =fn_ndvi[p+len(str1):length]

   fn_bq=file_hdr+str2+file_end

   idx = fn_bq in flistbq

   if idx == True:

      #---- read ndvi and bq to cut off no-sense points

      print('process the '+ str(j+1) + ' th file: ' +fn_ndvi)

      (rt_t, rt_d)=read_ndvi(fn_ndvi,fn_bq,ulx,uly,lrx,lry,tmpbname)
   
      if  First_Flag == True:

          First_Flag=False

          tot_t=wrkdir+'/'+year+'_stack_ndvi.tif'

          tot_d=wrkdir+'/'+year+'_stack_bq.tif'

          os.system('cp '+ rt_t +' '+ tot_t)
                  
          os.system('rm -f '+rt_t)        

          os.system('cp '+ rt_d +' '+ tot_d)
      
          os.system('rm -f '+rt_d)

      else:

          tot_t=rp.raster_comb(tot_t,rt_t)

          tot_d=rp.raster_comb(tot_d,rt_d)



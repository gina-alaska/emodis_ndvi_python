;Jinag Zhu, jiang@gina.alaska.edu, 2/22/2011
;This program interpolates and smoothes a multiyear_layer_stack file and calculate metrics of mid-year data.
;The input is:a oneyear_stack file
;the output is:
;a mid-year smoothed data file named multiyear_layer_stack_smoothed,
;a metrics file named multiyear_layer_stack_smoothed_metrics.
;flg indicating if this program run successfully.

;This program breaks the huge data into tiles and goes through tile loop to proces each tile. For each tile, go through
;each pixel to calulate the metrics and smoothed time series of the pixel. 
;jzhu, 1/17/2012,this program combines moving average and threshold methodm it calls geoget_ver16.pro and sosget_ver16.pro. 

pro stat_11_year_ndvi_metrics_tile,flist,ver,flg

;flg (indicate if the program run successful, 0--successful, 1--not successful)
;---- initial envi,
;
;
;test only, input parameters

flist='/center/w/jzhu/nps/ndvi/flist'
ver='v1'

;---make sure the program can work in both windows and linux.

if !version.OS_FAMILY EQ 'Windows' then begin

sign='\'

endif else begin
sign='/'

endelse


;read 11 years of file name from flist

;---- read these two lists into flist and flist_bq


openr,u1,flist,/get_lun

flst=strarr(20) ; 20 years of file names in the file list
tmp=' '
j=0L
while not EOF(u1) do begin
readf,u1,tmp

flst(j)=tmp

j=j+1
endwhile

close,u1

;---- get rid of empty elemrents in the flist

idx=where (flst NE '',cnt )
flst=flst(idx)


;----produces output file names: smooth data file name and metrics file name.

filen=flst(0)

p =strpos(filen,sign,/reverse_search)

len=strlen(filen)

;wrkdir=strmid(filen,0,p+1)

filebasen=strmid(filen,p+1,len-p)

year=strmid(filebasen,0,4)

p =strpos(flist,sign,/reverse_search)

len=strlen(flist)

wrkdir=strmid(flist,0,p+1)

;filebasen=strmid(filen,p+1,len-p)

;----open a fileout to be ready to be writen out.

fileout=wrkdir+filebasen+'_stat_'+ver

openw,unit_stat,fileout, /get_lun

;---start ENVI batch mode
 
start_batch, wrkdir+'b_log',b_unit

;---setup a flag to inducate this program work successful. flg=0, successful, flg=1, not successful

flg=0;  0----successs, 1--- not sucess


;---open the files 

num_file=(size(flst))(1)

;create a 1d array to store the return fid

rtfid=lonarr(num_file)

for i=0,num_file-1 do begin

envi_open_file,flst(i),/NO_REALIZE,r_fid=rt_tmp

if rt_tmp EQ -1 then begin

flg=1  ; 0---success, 1--- not success

return  ;

endif else begin
  
rtfid(i)=rt_tmp  

endelse

endfor

;-----get the information of the first input file

envi_file_query, rtfid(0), data_type=data_type, xstart=xstart,ystart=ystart,$
                 interleave=interleave,dims=dims,ns=ns,nl=nl,nb=nb,bnames=bnames

pos=lindgen(nb)

;---inital tile process
;  tile_id = envi_init_tile(rtfid(0), pos, num_tiles=num_of_tiles, $
;    interleave=(interleave > 1), xs=dims(1), xe=dims(2), $
;    ys=dims(3), ye=dims(4) )


;---define a data buff to store the 11 slices. The slice is (ns,nb), the data=data(ns,nb,num_file)

data=fltarr(ns,nb,num_file)

bnames_metrics = ['onp','onv','endp','endv','durp','maxp','maxv','ranv','rtup','rtdn','tindvi','mflg']


for i=0l, nl-1 do begin  ; every line

;get slices of 11 data files 

for n=0, num_file-1 do begin
data(*,*,n)= envi_get_slice(/BIL,fid=rtfid(n),line=i,pos=pos)
endfor


print, 'process line: '+strtrim(string(i),2)+ ' of total '+ strtrim(string(nl-1),2 )

;data = envi_get_tile(tile_id, i)

;----call avg_slices rubroutine. input is data(ns,nb,num_file), output is data_out(ns,nb)

data_out=avg_slices(data)

;---write data_smooth of one tile

writeu,unit_stat,data_out ;output data_out(ns,nb) for the line i


endfor  ; line loop

;---close files

free_lun, unit_stat


;---get the output head info file from the first file, described as rtfid(0)

map_info=envi_get_map_info( fid=rtfid(0) )

data_type=4 ; float for metrics

envi_setup_head, fname=fileout, ns=ns, nl=nl, nb=nb,bnames=bnames_metrics, $
    data_type=data_type, offset=0, interleave=(interleave > 1),$
    xstart=xstart+dims[1], ystart=ystart+dims[3],map_info=map_info, $
    descrip='averaged metrics data', /write


;envi_tile_done, tile_id

;---- exit batch mode

ENVI_BATCH_EXIT

print,'finishing smooth and calculation of metrics ...'

return

end


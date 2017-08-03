;Jiang Zhu, jiang@gina.alaska.edu, 2/22/2011
;This program get rid off the points with value equal to threshold, 
;cahnge values to 101b or 102b of the points that their values are equal to snowcld,
;then interpol the vector.
;inputs are:
;vcomp (a three-year-time-series vector),
;threshold (fill value for missing pixel in 0-200, default is 80b ),
;snowcld (fill value for snoe,cloud,bad, and negative reflectance pixelin 0-200, default is 60b),
;ratio (to control if is sutable to calculate metrics)
;output:interpolated vector is returned in vcomp 
 
;jzhu, vcomp_cb include ndvi and bq in one vector
;jzhu,12/7/2011, from cutoff_interp_ver9.pro, do not cut off fill value but set thenm as 100b

;jzhu, 7/8/2013, find it is wrong to interpolate 100,101 at beginning and ending, should interpolate whole time series

pro cutoff_interp_v2, vcomp_cb, vcomp_g, flg_metrics

;vcomp_cb----vector need processed, which include both ndvi and related quality_flag
;return vcomp_g 
;threshold---if value of element in vcomp are less than threshold, this element needs interpolate,
;ratio---number of valid elements/total number of elements,
;in order to compainto nps data process, data is type, range is 0-200,100-20 are good data,
;80 is fill value, negative ndvi value corresponds to 80-99, 0 ndvi corresponds to 100,
;for 80-89, cahnge them into 100,101,or 102,
;80-89-->100, 90-99->101,100-->102

;default values for threshold, snowcld, and ratio are:
;threshold = 80 ; do not interpolate these points
;snowcld=60; need interpolate these points
;ratio should be 0.5

;0b-valid,1b-cloudy,2b-bad,3b-negative reflectance,4b-snow,10b-fill

flg_metrics=1 ; initial value


;---get valid data vector

num=n_elements(vcomp_cb)

;seperate the combined vector into ndvi and bq vectors

vcomp = vcomp_cb(0: num/2-1)

vcomp_bq=vcomp_cb(num/2:num-1)
 
;different choose in dealinng with no valid points 

;1. interpolate fill, cloudy, and bad points, replace snow and negative reflectance points with randomly 100b to 101.
   
;idxv = where( (vcomp_bq EQ 0b or vcomp_bq EQ 4b ) and vcomp GE 100b , cnt, complement=idx) ;(valid or snow) and positive 



tmpnan=vcomp ; tmpnan will be used to store return vector

;---- first set negative points and bad points to be ramdonly 100 to 101b

idx_negbad=where(vcomp LE 100b or vcomp_bq EQ 2b ,cnt_negbad, complement=idxv )

if cnt_negbad GT 0 then begin ; <1> need do some interpolation

; do interpolate

tmpx=fix(idxv) ;x coordinates values of valid values

tmpv=vcomp(idxv) ; valid values
;---interpolate the missing points: cloud,bad, fill, and negative reflectance pixels
len=n_elements(vcomp)

tmpu=indgen(len) ; interpolated x coorinidates

tmpinterp=interpol_line100b_v2(tmpv,tmpx,tmpu)

tmpnan=tmpinterp

endif

;---get rid of odd points, 0.4

filter_2odd, tmpnan, 0.25,0.25,tmpnan1
;---output vector
vcomp_g = tmpnan1

return



end

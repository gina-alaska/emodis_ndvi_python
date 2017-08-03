;this program use slope method to determine start end end day indices , input ndvi, threshold_val
;we calulate the both up and down slopes at threshold_val, return start and end day indics, and wl0 and wl1 
function auto_wl, ndvi, thresholdval

;ndvi is 0-1 ndvi data, thresholdval is used to determine window

num=n_elements(ndvi)

idx=where(ndvi GE thresholdval,cnt)

if cnt LE 10 or cnt GE 27 then begin   ; not found points with >= thresholdval, set wl=num-17, 17 is assumed the average greenness 7-day

gap=17

endif else begin

gap=cnt

endelse

wl=[num-gap,num-gap]

return, wl

end

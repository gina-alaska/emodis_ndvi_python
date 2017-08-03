;===   IMGREAD   ============================================
; This function reads in an image of x samples and y lines.
; If the FLOAT flag is set, it reads images as floating point
; otherwise it reads as byte (unsigned character). 
; If the ORDER flag is set, it reads the image in so that the
; first line is at the bottom.
; The ONEBAND flag is only available if nbands is ommited
; from the argument list.  If both are omitted, it assumes
; the number of bands is #lines/#samples (as in the AVHRR
; chips)

; nbands can be used with the /ORDER flag to flip the order
; on individual bands (eg imgread(file, 100, 1200, 12, /ORDER))
; This will read in a 100x1200 image and flip every 100x100
; block.

; NOTE: the image dimension conventions and nbands aren't  
; fully functional 
;============================================================

FUNCTION   imgread3, filename, x, y, nbands, nsites, ORDER = order , I2 = i2, dt=dt
t0 = systime(1)
case N_PARAMS() of
  3: begin
       nbands = 1
       ydim = y/nbands
       nsites = 1
     end
  4: begin
       nbands = nbands
       ydim = y
       nsites = 1
       data = bytarr(x,y, nbands, /NoZero)
       tmp = bytarr(x,y, nbands, /NoZero)
     end
;  5: begin
;       nbands = nbands
;       ydim = y/nbands
;       nsites = nsites
;       xdim = x/nsites
;       data = bytarr(x,ydim,nbands, /NoZero)
;       tmp = bytarr(x,ydim,nbands, /NoZero)
;     end
  else: MESSAGE, 'Wrong number of arguments in IMGREAD'
endcase

;  FLIP READ ORDER
if(KEYWORD_SET(ORDER)) then $
   RotIdx = 7 $
else $
   RotIdx = 0

;  IS DATA BYTE OR I*2
if(KEYWORD_SET(I2)) then begin
  data = intarr(x,y,nbands, /NoZero)
  tmp = intarr(x,y,nbands, /NoZero)
endif else begin 
  data = bytarr(x,y,nbands, /NoZero)
  tmp = bytarr(x,y,nbands, /NoZero)
endelse

;
   CASE (DT) OF
   1: BEGIN
        data = bytarr(x,y,nbands, /NoZero)
        tmp = bytarr(x,y,nbands, /NoZero)
   END;1
   2: BEGIN
        data = intarr(x,y,nbands, /NoZero)
        tmp = intarr(x,y,nbands, /NoZero)
   END;2
   3: BEGIN
        data = lonarr(x,y,nbands, /NoZero)
        tmp = lonarr(x,y,nbands, /NoZero)
   END;3
   4: BEGIN
        data = fltarr(x,y,nbands, /NoZero)
        tmp = fltarr(x,y,nbands, /NoZero)
   END;4
   ELSE:
   ENDCASE



openr, LUN, filename, /GET_LUN
if(KEYWORD_SET(I2)) then begin
  pix = assoc(LUN,intarr(x,y, /NoZero)) 
endif else begin
  CASE (DT) OF
  1: pix=assoc(LUN, bytarr(x,y,/NoZero))
  2: pix=assoc(LUN, intarr(x,y,/NoZero))
  3: pix=assoc(LUN, lonarr(x,y,/NoZero))
  4: pix=assoc(LUN, fltarr(x,y,/NoZero))
  ELSE: pix = assoc(LUN,bytarr(x,y, /NoZero)) 
  ENDCASE
endelse

for i = 0, nbands-1 do begin
tmp(*,*,i) = pix(i)
end

case(rotidx) of
  7: begin
        for i = 0, nbands - 1 do begin
           data(*, *, i) = rotate( tmp(*, *, i), RotIdx) 
        end
     end
  else: data = tmp
endcase

FREE_LUN, LUN

print, "TIME = ", systime(1)-t0
return, data
end

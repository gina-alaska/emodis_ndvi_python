;this program filter out odd points in the vector v, one-year ndvi curve should be both sides are low and middle is hight.
;if ther are some points with very low values,
;they are considered as odd points, take them off and interpol them.
;input, v---vector,output: returned vector named rtr
; if minpoint-lowvalu > 0.4 take this point out

;jzhu, 9/13/2011, this program get rif of 1 or 2 consecutive odd points,
;odd points are defined they are 0.4 smaller than adjunctive points
;diffval=0.4


pro filter_2odd, rin, uprate,downrate, r

if min(rin) EQ max(rin) then begin

r = rin

return

endif

r = float(rin) ;  r will be used to store result vector

num=(size(r))(1) ; number of points in the vector r


;determine if the first or last points are odd point

if (r(0)-r(1))/r(1) GT uprate and (r(0)-r(2))/r(2) GT uprate then begin
r(0)=0.5*(r(1)+r(2))
endif

if (r(num-1) -r(num-2))/r(num-2) GT uprate and (r(num-1)-r(num-3))/r(num-3) GT uprate then begin
r(num-1)=0.5*( r(num-2)+r(num-3) )
endif



for k =0, num-4 do begin ; check four points to find the odd 1 point or 2 consecutive odd points

; one odd in three points

if ((r(k)-r(k+1))/r(k) GT downrate and (r(k+2)-r(k+1))/r(k+2) GT downrate) or $
   ( ( r(k+1)-r(k) )/r(k) GT uprate and (r(k+1)-r(k+2))/r(k+2) GT uprate ) then begin

 r(k+1)=0.5*( r(k)+r(k+2) )

endif
;endif else begin    ; two odds in four points

;  if ((r(k)-r(k+1))/r(k) GT downrate and (r(k+3)-r(k+1))/r(k+3) GT downrate and $
;     (r(k)-r(k+2))/r(k) GT downrate and (r(k+3)-r(k+2))/r(k+3) GT downrate ) or  $
;     ((r(k+1)-r(k))/r(k) GT uprate   and (r(k+1)-r(k+3))/r(k+3) GT uprate and $
;     (r(k+2)-r(k))/r(k) GT uprate   and (r(k+2)-r(k+3))/r(k+3) GT uprate ) then begin
  
;  slope=(r(k+3)-r(k))/3.0
;  r(k+1)=1.0*slope+r(k)
;  r(k+2)=2.0*slope+r(k)  
  
;  endif
  
  
;endelse  


endfor

r=byte(r)

return

end 
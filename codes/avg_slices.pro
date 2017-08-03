function avg_slices, data
;this subroutine takes data(ns,nb,num_file),does average over num_file, retun data(ns,nb)

sz=size(data)
ns=sz(1)
nb=sz(2)
nf=sz(3)

data_out=fltarr(ns,nb)

for i=0,ns-1 do begin ; for each sample
  
  
  idxn1=where(data(i,11,*) EQ -1.0,numn1)
  
  if numn1 GT 0 then begin  ; if there is any -1 in the mflgs
    
    data_out(i,*)=-1.0
  endif else begin
    
     idx0=where(data(i,11,*) EQ 0.0, num0)
     
     if num0 GT 0 then begin ; if there is any 0 in the mflg array at data(i,11,*) 
       
       data_out(i,*)=0.0
     endif else begin
        
       idx1=where(data(i,11,*) EQ 1.0,num1)
 
       data_out(i,0)=round( total(data(i,0,idx1))/num1 )
       
       data_out(i,1)=       total(data(i,1,idx1))/num1
       
       data_out(i,2)=round( total(data(i,2,idx1))/num1 )
       
       data_out(i,3)=       total(data(i,3,idx1))/num1

       data_out(i,4)=data_out(i,2)-data_out(i,0)
       
       data_out(i,5)=round( total(data(i,5,idx1))/num1 )
       
       data_out(i,6)=       total(data(i,6,idx1))/num1
       
       data_out(i,7)=       total(data(i,7,idx1))/num1
       
       data_out(i,8)=       total(data(i,8,idx1))/num1
       
       data_out(i,9)=       total(data(i,9,idx1))/num1
       
       data_out(i,10)=      total(data(i,10,idx1))/num1
       
       data_out(i,11)=1.0
       
     endelse
    
  endelse
  
endfor

return, data_out

end

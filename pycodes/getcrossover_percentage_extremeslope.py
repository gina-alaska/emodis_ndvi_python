import numpy as np

def GetCrossOver_percentage_extremeslope(XRef,YRef, XData,YData, mv_percent, bq, bpy, cross_direction):
   #;jzhu, 2017/8/15, modified from GetCross_percentage_extremeslope.pro
   #This function calculates the crossover points, 20% popints, extremeslope points, and maximun value point. 
   #inputs:
   #XRef=Time,1D,x axis for NDVI vector
   #YRef=NDVI,1D, NDVI
   #XData=Time,1D, x axis for FMA/BMA vector
   #YData=FMA/BMA,1D, forward/backward circular shift vector
   #mv_percent---user defined percentage of max NDVI value as a threshold, usually mv_percent=0.2   
   #bq=quality vector related YRef, 1D
   #bpy=number of points in YRef, scalar, usually it equals to 42
   #CROSS_DIRECTION=YData crossover YRef, UP-YData cross over Yref from below
   #DOWN, YData crossover Yref from above,cross_direction is one of UP,DOWN
   #it calculates crossover points between YData to YRef, and crossover points between line 20%  and YRef,
   #it also calcualtes maximun NDVI value points and maximun or minimun slope points for Yref. 
   #;output points,xvalue,yvalue,slope,type(0-crossover,1-20%,2-maximun/minimun slope points,3-maximun value point)

   WinFirst=int(0.5*bpy)  #start season must less than WinFirst

   WinMin=int(0.1*bpy)    #start season must be greater than WinMin
   
   WinLast=int(0.5*bpy)  #end season must be greater than WinLast

   WinMax=int(0.9*bpy)  #end season must be less than WinMax

   #get the indics of YRef[Winmin:WinFirst]
   
   #firsthf=YRef[WinMin:WinFirst]   
   
   #maxv=max(firsthf)
   
   #minv=min(firsthf)
   
   #mxidx=np.where(firsthf == maxv )[0] + WinMin

   #firsthfidx=mxidx[0]
   
   #v20down = mv_percent*( maxv-minv ) + minv
   
   #get the indics of YRef[WinMax:WinLast]
   
   #lasthf=YRef[WinMax:WinLast]   
   
   #maxv=max(lasthf)
   
   #minv=min(lasthf)
   
   #mxidx=np.where(lasthf == maxv )[0] + WinMax

   #lasthfidx=mxidx[len(mxidx)-1]
   
   #v20up=mv_percent*( maxv-minv ) + minv
    
   minv =min(YRef)    
    
   tmp=YRef[WinMin:WinMax]   
   
   maxv=max(tmp)
   
   mxidx=np.where(tmp == maxv )[0] + WinMin

   firsthfidx=mxidx[0]
   
   lasthfidx=mxidx[len(mxidx)-1]
   
   v20down = mv_percent*( maxv-minv ) + minv
       
   v20up=v20down 
    
   slopemax=0.0
 
   xslopemax=0.0
 
   yslopemax=0.0
 
   slopemin=0.0
 
   xslopemin=0.0
 
   yslopemin=0.0
   
   nSize = XRef.shape
   
   nDim=  XRef.ndim

   oSize=nSize[0]

   XPts=np.zeros(oSize,dtype=np.int16)

   YPts=np.zeros(oSize,dtype=np.float16)

   SPts=np.zeros(oSize,dtype=np.float16)

   TPts=np.zeros(oSize,dtype=np.float16)

   CPts=np.zeros(oSize,dtype=np.float16)

   
   if cross_direction == 'UP':
      UP=1
      DOWN=0
      xstar=0
      ystar=YRef[xstar]

   elif cross_direction == 'DOWN':
      UP=0
      DOWN=1
      xstar=len(XRef)-1
      ystar=YRef[xstar]

   else:
      UP=1
      DOWN=1 
   

   iCount=0
   
   if nDim == 1:
         
      for i in range(0, oSize-1):
         
             
            RSlope = float(YRef[i+1]-YRef[i])/(XRef[i+1]-XRef[i])
            DSlope = float(YData[i+1]-YData[i])/(XData[i+1]-XData[i])      
                       
         
            if ( YRef[i] <= YData[i] and YRef[i+1] >= YData[i+1] and DOWN ): #<0>, found possible SOS
            
              #Down, YData(FMA) cross over Yref from above, decide SOS
              #Up, YData(BMA) cross over Yref from below, devide EOS

               if YRef[i+1] == YData[i+1]: # ;<1> point 2 cross over,use point 2

                   xstar=i+1

                   ystar=YRef[i+1]
                  
               else:  #<1> YData is above at point 2 below, check YData at point 1
                   
                   if YRef[i] == YData[i]: #<2> YData is above, and YData cross over at point 1, use point 1

                       xstar=i

                       ystar=YRef[i]
                   else: #<2> YData is obove at point 2, below at point 1, calculate the cross over point and value

                       RSlope = float(YRef[i+1]-YRef[i])/(XRef[i+1]-XRef[i])
                       DSlope = float(YData[i+1]-YData[i])/(XData[i+1]-XData[i])
                       SlopeDiff=DSlope-RSlope

                       if SlopeDiff == 0:
                           SlopeDiff=1.0e-6

                       RInt = YRef[i]-RSlope*XRef[i]
                       DInt = YData[i]-DSlope*XData[i]
                       xstar = (RInt-DInt)/SlopeDiff
                       ystar =RSlope*(xstar-XRef[i])+YRef[i]
                          
                       #if XStar LT XRef[i] or XStar GT XRef[i+1]: #(11) then begin

                       if abs(xstar-XRef[i]) <= abs(xstar-XRef[i+1]): #(12)  then begin
                         xstar=XRef[i]
                         ystar=YRef[i]
                       else:  #(12)
                         xstar=XRef[i+1]
                         ystar=YRef[i+1]
               #write possible SOS
               XPts[iCount]=xstar
               YPts[iCount]=ystar
               SPts[iCount]=RSlope
               TPts[iCount]=0
               CPts[iCount]=1
               iCount = iCount+1

        
         
            if ( YRef[i] >= YData[i] and YRef[i+1] <= YData[i+1] and UP ): #<00>, found possible EOS 
                  
               if YRef[i] == YData[i]: # ;<1> YData cross over at point 1, use point 1

                   xstar=i

                   ystar=YRef[i]

               else: #<01> YData below at point 1, check point 2
                  
                   if YRef[i+1] == YData[i+1]: #<02> YData is below at point 1, cross over at point 2, use point 2  
                       xstar=i+1
                       ystar=YRef[i+1]
                   else: #<02> YData below at point 1, above at point 2, calculate cross over
                       #;--- calcualte xstar,ystar using linear function formula  
                       RSlope = float(YRef[i+1]-YRef[i])/(XRef[i+1]-XRef[i])
                       DSlope = float(YData[i+1]-YData[i])/(XData[i+1]-XData[i])
                       SlopeDiff=DSlope-RSlope
                       if SlopeDiff == 0:
                          SlopeDiff=1.e-6
                       RInt = YRef[i]-RSlope*XRef[i]
                       DInt = YData[i]-DSlope*XData[i]
                       xstar = (RInt-DInt)/SlopeDiff
                       ystar = RSlope*(xstar-XRef[i])+YRef[i]
             
                       #if XStar LT XRef[i] or XStar GT XRef[i+1]: #(11) then begin
             
                       if abs(xstar-XRef[i]) <= abs(xstar-XRef[i+1]): #(12)  then begin
                           xstar=XRef[i]
                           ystar=YRef[i]
                       else:  #(12)
                           xstar=XRef[i+1]
                           ystar=YRef[i+1]

               #write possible EOS
               XPts[iCount] = xstar
               YPts[iCount] = ystar
               SPts[iCount] = RSlope
               TPts[iCount] = 0
               CPts[iCount] = 1
               iCount = iCount + 1

              
            #;looking for crossover with line with Y=20% of (maxndvi-minndvi) + minndvi 

            if (YRef[i] <= v20down and v20down <= YRef[i+1]) and RSlope > 0 and DOWN: # found xstar
               XStar1=int(np.ceil(XRef[i]+(v20down-YRef[i])/RSlope))
               XPts[iCount]=XStar1
               YPts[iCount]=YRef[XStar1]
               SPts[iCount]=RSlope
               TPts[iCount]=1    #; type of the point, 0-crossover, 1-20%,2-extremeslope
               CPts[iCount]=1
               iCount = iCount+1
           
            
            
            if (YRef[i] >= v20up and v20up >= YRef[i+1]) and RSlope < 0 and UP: #; found xstar
              
               XStar1=int(np.floor(XRef[i]+(v20up-YRef[i])/RSlope))
               XPts[iCount]=XStar1
               YPts[iCount]=YRef[XStar1]
               SPts[iCount]=RSlope
               TPts[iCount]=1    #; type of the point, 0-crossover, 1-20%,2-extremeslope
               CPts[iCount]=1
               iCount = iCount+1
            
 
            #;---get maximun slope for down and minimun slope for up

            if RSlope >= 0 and DOWN and RSlope > slopemax and XRef[i] < firsthfidx:
            
               slopemax=RSlope
               xslopemax=XRef[i]
               yslopemax=YRef[i]
             
            
            
            if RSlope < 0 and UP and RSlope < slopemin and XRef[i] > lasthfidx:
            
               slopemin=RSlope
               xslopemin=XRef[i]
               yslopemin=YRef[i]
             
      #end of for loop
   
         
      #;------ add maxslope and maxvalue points to down or minslope and minvalue points to up
         
      if DOWN:
         
         #find maxslope point
         if xslopemax == 0.0: # not find maximun slope point, use middle point
             XPts[iCount]=bpy/2 - 1 
             YPts[iCount]=YRef[bpy/2 - 1]
         else:
             XPts[iCount]=xslopemax
             YPts[iCount]=yslopemax
             SPts[iCount]=slopemax
             CPts[iCount]=1
             TPts[iCount]=2

         #get maxvalue point close to start
                      
         XPts[iCount+1]=firsthfidx 
         YPts[iCount+1]=YRef[firsthfidx]
         CPts[iCount+1]=1
         TPts[iCount+1]=3
         
      if UP:
          if xslopemin == 0.0: #; not find the minimum slope point, use middle point
             XPts[iCount]=bpy/2
             YPts[iCount]=YRef[bpy/2]
          else:
             XPts[iCount]=xslopemin
             YPts[iCount]=yslopemin           
             SPts[iCount]=slopemin
             CPts[iCount]=1
             TPts[iCount]=2

          #get maxvalue point close to end 
             
          XPts[iCount+1]=lasthfidx 
          YPts[iCount+1]=YRef[lasthfidx]
          CPts[iCount+1]=1
          TPts[iCount+1]=3
         
         
         
      NPts=0 #; initial value

      NPtsidx=np.where( XPts != 0 )[0]

      NPtscnt=len(NPtsidx)

      if NPtscnt > 0:

          NPts =NPtscnt
       

      if NPts == 0:
          Cross={'X':0, 'Y':0., 'S':0, 'T':0, 'C':0.,'N':NPts}
      else:
          Cross={'X':XPts[NPtsidx],'Y':YPts[NPtsidx],'S':SPts[NPtsidx],'T':TPts[NPtsidx],'C':CPts[NPtsidx],'N':NPts}
            

   return Cross


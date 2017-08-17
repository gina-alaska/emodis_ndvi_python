#this includes functions raster processing. it comes from https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#create-raster-from-array.
import os
from osgeo import gdal, osr, gdal_array
#from skimage.graph import route_through_array
import numpy as np


def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    raster = None
    return array

def raster2arraybname(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    bandname=band.GetDescription()
    raster = None
    return (array,bandname)


def coord2pixelOffset(rasterfn,x,y):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    xOffset = int((x - originX)/pixelWidth)
    yOffset = int((y - originY)/pixelHeight)
    raster = None
    return xOffset,yOffset

#def createPath(CostSurfacefn,costSurfaceArray,startCoord,stopCoord):

#    # coordinates to array index
#    startCoordX = startCoord[0]
#    startCoordY = startCoord[1]
#    startIndexX,startIndexY = coord2pixelOffset(CostSurfacefn,startCoordX,startCoordY)

#    stopCoordX = stopCoord[0]
#    stopCoordY = stopCoord[1]
#    stopIndexX,stopIndexY = coord2pixelOffset(CostSurfacefn,stopCoordX,stopCoordY)

#    # create path
#    indices, weight = route_through_array(costSurfaceArray, (startIndexY,startIndexX), (stopIndexY,stopIndexX),geometric=True,fully_connected=True)
#    indices = np.array(indices).T
#    path = np.zeros_like(costSurfaceArray)
#    path[indices[0], indices[1]] = 1
#    return path

def array2raster(newRasterfn,rasterfn,array,bandname):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = array.shape[1]
    rows = array.shape[0]

    gdal_dtype=gdal_array.NumericTypeCodeToGDALTypeCode(array.dtype)

    #driver = gdal.GetDriverByName('GTiff')
    driver  = raster.GetDriver()

    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal_dtype)

    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    outband = outRaster.GetRasterBand(1)

    outband.SetDescription(bandname)

    outband.WriteArray(array)

    outRasterSRS = osr.SpatialReference()

    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())

    outRaster.SetProjection(outRasterSRS.ExportToWkt())

    outRaster.FlushCache()
   
    raster = None

    outRaster = None

def write_raster(newRasterfn,rasterfn,array,bandname):
    
    '''use raster geo info from rasterfn, write 3d array with band name into newRasterfn. array(bandnumber, ysize, xsize). dtype of the array must be unint8, float32
    '''
    raster = gdal.Open(rasterfn)

    geotransform = raster.GetGeoTransform()

    originX = geotransform[0]

    originY = geotransform[3]

    pixelWidth = geotransform[1]

    pixelHeight = geotransform[5]
   
    cols = array.shape[2]

    rows = array.shape[1]

    bnum = array.shape[0]

    gdal_dtype=gdal_array.NumericTypeCodeToGDALTypeCode(array.dtype)

    #driver = gdal.GetDriverByName('GTiff')
    driver  = raster.GetDriver()

    outRaster = driver.Create(newRasterfn, cols, rows, bnum, gdal_dtype)

    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    
    for i in range(bnum):

      outband = outRaster.GetRasterBand(i+1)

      outband.SetDescription(bandname[i])

      outband.WriteArray(array[i,:,:])

    outRasterSRS = osr.SpatialReference()

    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())

    outRaster.SetProjection(outRasterSRS.ExportToWkt())

    outRaster.FlushCache()

    raster = None

    outRaster = None


def raster_comb(outRasterfn, rasterfn):

    #combine rasterfn to tot_rasterfn

    #get the array and bandname from rasterfn
    (array,bandname)=raster2arraybname(rasterfn)
    
    #get the outraster
    outraster = gdal.OpenShared(outRasterfn)
    
    #create a temporary MEM driver
    tmp=gdal.GetDriverByName('MEM').CreateCopy('', outraster, 0)

    tmp.AddBand()
    
    bandnumber=tmp.RasterCount

    band=tmp.GetRasterBand(bandnumber)
    
    #add array and bandname to the tmp
    band.WriteArray(array)
    
    band.SetDescription(bandname)
 
    #create a tmp_file name
    tmp_dir=os.path.dirname(outRasterfn)

    tmp_basename=os.path.basename(outRasterfn)
 
    tmp_file=tmp_dir+'/tmp_'+tmp_basename
    
    #copy the tmp to tmp_file
    dst = gdal.GetDriverByName('GTIFF').CreateCopy(tmp_file,tmp, 0)
    
    #write the memory file tmp to the disk
    dst.FlushCache()

    dst = None

    outraster =None
    
    os.system('rm '+outRasterfn)
   
    os.system('mv '+tmp_file+' '+outRasterfn)
     
    #remove _good_ndvi or good_bg files

    os.system('rm '+rasterfn)
   
    return outRasterfn


def subsection(file_name, someNewMinX, someNewMinY, someNewMaxX, someNewMaxY):
    raw_file_name = os.path.splitext(os.path.basename(file_name))[0]
    driver = gdal.GetDriverByName('GTiff')
    dataset = gdal.Open(file_name)
    band = dataset.GetRasterBand(1)
    transform = dataset.GetGeoTransform()
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    transform = dataset.GetGeoTransform()
    minx = transform[0]
    maxx = transform[0] + cols * transform[1] + rows * transform[2]
    miny = transform[3] + cols * transform[4] + rows * transform[5]
    maxy = transform[3]
    width = maxx - minx
    height = maxy - miny

    output_path = os.path.join("data", raw_file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    tiles = create_tiles(minx, miny, maxx, maxy, n)
    transform = dataset.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]

    print xOrigin, yOrigin

    # Subsitute with your new subsection values
    newminx = someNewMinX
    newmaxx = someNewMaxX
    newminy = someNewMinY
    newmaxy = someNewMaxY

    p1 = (newminx, newmaxy)
    p2 = (newmaxx, newminy)

    i1 = int((p1[0] - xOrigin) / pixelWidth)
    j1 = int((yOrigin - p1[1])  / pixelHeight)
    i2 = int((p2[0] - xOrigin) / pixelWidth)
    j2 = int((yOrigin - p2[1]) / pixelHeight)

    print i1, j1
    print i2, j2

    new_cols = i2-i1
    new_rows = j2-j1

    data = band.ReadAsArray(i1, j1, new_cols, new_rows)

    #print data

    new_x = xOrigin + i1*pixelWidth
    new_y = yOrigin - j1*pixelHeight

    print new_x, new_y

    new_transform = (new_x, transform[1], transform[2], new_y, transform[4], transform[5])

    output_file_base = raw_file_name + "_" + "subsection" + ".tif"
    output_file = os.path.join("data", raw_file_name, output_file_base)

    dst_ds = driver.Create(output_file,
                           new_cols,
                           new_rows,
                           1,
                           gdal.GDT_Float32)

    #writting output raster
    dst_ds.GetRasterBand(1).WriteArray( data )

    #setting extension of output raster
    # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
    dst_ds.SetGeoTransform(new_transform)

    wkt = dataset.GetProjection()

    # setting spatial reference of output raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dst_ds.SetProjection( srs.ExportToWkt() )

    #Close output raster dataset
    dst_ds = None

    dataset = None
    
    rt_file_name=output_file
  
    return rt_file_name

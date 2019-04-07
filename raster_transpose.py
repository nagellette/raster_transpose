from osgeo import gdal, osr
import numpy as np

## read the original raster and it's tranformation parameters
original_raster = gdal.Open("./data/output_trajectory.tif")
original_raster_geo_transform = original_raster.GetGeoTransform()

## get the raster dimensions
raster_x_size = original_raster.RasterXSize
raster_y_size = original_raster.RasterYSize

## get raster band count
raster_band_count = original_raster.RasterCount

## create empty raster with 4 bands to produce final raster
output_raster = gdal.GetDriverByName('GTiff').Create('./data/output_trajectory_new.tif', raster_y_size, raster_x_size, raster_band_count,
                                                     gdal.GDT_Float32)
output_raster.SetGeoTransform(original_raster_geo_transform)
srs = osr.SpatialReference()
srs.ImportFromEPSG(32650)
output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file


for i in range(0, raster_band_count):
    ## read the raster bands
    band_np = np.array(original_raster.GetRasterBand(i+1).ReadAsArray())

    ## transpose the bands
    band_np = np.transpose(band_np)

    ## pass transposed np arrays as bands
    output_raster.GetRasterBand(i+1).WriteArray(band_np)

## close the rasters
original_raster = None
output_raster = None
from osgeo import gdal, osr
import numpy as np

## read the original raster and it's tranformation parameters
original_raster = gdal.Open("./data/output_trajectory.tif")
original_raster_geo_transform = original_raster.GetGeoTransform()

## get the raster dimensions
raster_x_size = original_raster.RasterXSize
raster_y_size = original_raster.RasterYSize

## create empty raster with 4 bands to produce final raster
output_raster = gdal.GetDriverByName('GTiff').Create('./data/output_trajectory_new.tif', raster_y_size, raster_x_size, 4,
                                                     gdal.GDT_Float32)
output_raster.SetGeoTransform(original_raster_geo_transform)
srs = osr.SpatialReference()
srs.ImportFromEPSG(32650)
output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file

## read the raster bands
band1_np = np.array(original_raster.GetRasterBand(1).ReadAsArray())
band2_np = np.array(original_raster.GetRasterBand(2).ReadAsArray())
band3_np = np.array(original_raster.GetRasterBand(3).ReadAsArray())
band4_np = np.array(original_raster.GetRasterBand(4).ReadAsArray())

## transpose the bands
band1_np = np.transpose(band1_np)
band2_np = np.transpose(band2_np)
band3_np = np.transpose(band3_np)
band4_np = np.transpose(band4_np)

## pass transposed np arrays as bands
output_raster.GetRasterBand(1).WriteArray(band1_np)
output_raster.GetRasterBand(2).WriteArray(band2_np)
output_raster.GetRasterBand(3).WriteArray(band3_np)
output_raster.GetRasterBand(4).WriteArray(band4_np)

output_raster = None
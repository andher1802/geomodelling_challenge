library(raster)

RasterTemplate <- raster('nederland_1000.tif')
RasterTemplate_Proj <- projectRaster(RasterTemplate, crs = CRS("+proj=longlat +datum=WGS84"))
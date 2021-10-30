from satsearch import Search
from datetime import datetime, timedelta
from pyproj import Transformer
from json import load
from rasterio.features import bounds
from osgeo import ogr, osr, gdal
import rasterio
import numpy as np
import os
import geopandas as gpd
import json

from utils.set_user_input import set_arguments_pipeline


def read_input_geometry(filename, geom_pos=-1):
    """
    Function that read a geojson file and return the last contained geometry.
    """
    file_path = filename
    input_geojson = gpd.read_file(file_path)
    if len(input_geojson) > 1:
        geometry = json.loads(input_geojson.dissolve().to_json())["features"][0]["geometry"]
    else:
        geometry = json.loads(input_geojson.to_json())["features"][0]["geometry"]
    return geometry


def read_url_image(url_ref, input_geometry):
    """
    returns a matrix from an image located in the url_ref
    and makes sure the adjust it to the input geometry bounds and crs.
    """
    with rasterio.open(url_ref) as geo_fp:
        bbox = bounds(input_geometry)
        coord_transformer = Transformer.from_crs("epsg:4326", geo_fp.crs)
        coord_upper_left = coord_transformer.transform(bbox[3], bbox[0])
        coord_lower_right = coord_transformer.transform(bbox[1], bbox[2])
        pixel_upper_left = geo_fp.index(coord_upper_left[0], coord_upper_left[1])
        pixel_lower_right = geo_fp.index(coord_lower_right[0], coord_lower_right[1])
        for pixel in pixel_upper_left + pixel_lower_right:
            if pixel < 0:
                print("Provided geometry extends available datafile.")
                print("Provide a smaller area of interest to get a result.")
                exit()
        window = rasterio.windows.Window.from_slices(
            (pixel_upper_left[0], pixel_lower_right[0]),
            (pixel_upper_left[1], pixel_lower_right[1]),
        )
        return geo_fp.read(1, window=window)


def array2raster(input_array, input_geometry, raster_template_path):
    """
    This function takes an np array, an input geometry and a raster template
    and creates a raster with the values from the array.
    input array and raster_template sizes should match.
    """
    array_df = input_array
    bbox = bounds(input_geometry)
    output_path = set_arguments_pipeline()["folder"]
    filename = "_".join([raster_template_path.split("/")[-2], "_NDVI.tif"])
    filename_path = os.path.join(output_path, filename)
    if os.path.exists(filename_path):
        print(
            "file {0} already exists in output folder {1}, continuing without errors".format(
                filename, output_path
            )
        )
    else:
        with rasterio.open(raster_template_path) as geo_fp:
            coord_transformer = Transformer.from_crs("epsg:4326", geo_fp.crs)
            xmin, ymax = coord_transformer.transform(bbox[3], bbox[0])
            xmax, ymin = coord_transformer.transform(bbox[1], bbox[2])
            ncols = array_df.shape[1]
            nrows = array_df.shape[0]
            xres = (xmax - xmin) / float(ncols)
            yres = (ymax - ymin) / float(nrows)
            geotransform = (xmin, xres, 0, ymax, 0, -yres)
            output_raster = gdal.GetDriverByName("GTiff").Create(
                filename_path, ncols, nrows, 1, gdal.GDT_Float32
            )
            output_raster.SetGeoTransform(geotransform)
            srs = osr.SpatialReference()
            crs_target = str(geo_fp.crs)
            crs_target_int = int(crs_target.split(":")[1])
            # srs.ImportFromEPSG(32632)
            srs.ImportFromEPSG(crs_target_int)
            output_raster.SetProjection(srs.ExportToWkt())
            output_raster.GetRasterBand(1).WriteArray(array_df)
            output_raster.FlushCache()

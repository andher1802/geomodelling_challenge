from data_collection.read_sentinel import pair_imagenames
from utils.set_user_input import set_arguments_pipeline
from utils.raster_helper import read_url_image, read_input_geometry, array2raster

import numpy as np
import rasterio


def compute_ndvi(band_inf, bands=["red", "nir"]):
    """
    This function computes the ndvi (normalized difference vegetation index)
    from the image resulting of the data catalog search.
    """
    input_geometry = read_input_geometry(set_arguments_pipeline()["input_geometry"])
    post_fix = "_band_info"
    red_band = band_inf[bands[0] + post_fix]
    nir_band = band_inf[bands[1] + post_fix]
    imagepairs_url_list = pair_imagenames(red_band, nir_band)
    ndvi_results = {}
    progress_counter = 0
    for image_pair in imagepairs_url_list:
        band_red_url = [
            red_url for red_url in imagepairs_url_list[image_pair] if "B04" in red_url
        ][0]
        band_nir_url = [
            red_url for red_url in imagepairs_url_list[image_pair] if "B08" in red_url
        ][0]
        band_red_image = read_url_image(band_red_url, input_geometry).astype(float)
        band_nir_image = read_url_image(band_nir_url, input_geometry).astype(float)
        ndvi_result = np.empty(band_red_image.shape, dtype=rasterio.float32)
        check = np.logical_or(band_red_image > 0, band_nir_image > 0)
        ndvi_result = np.where(
            check,
            (band_nir_image - band_red_image) / (band_nir_image + band_red_image),
            -999,
        )
        array2raster(ndvi_result, input_geometry, band_red_url)
        ndvi_results[image_pair] = [ndvi_result]
        progress_counter += 1
        print(
            "{0} of {1} images processed".format(
                progress_counter, len(imagepairs_url_list)
            )
        )
    return ndvi_results

from satsearch import Search
from datetime import datetime, timedelta
from pyproj import Transformer
from json import load
from utils.set_user_input import set_arguments_pipeline

def read_input_geometry(filename, geom_pos=-1):
    """
    Function that read a geojson file and return the last contained geometry.
    """
    file_path = filename
    with open(file_path,"r") as fp:
        file_content = load(fp)
    geometry = file_content["features"][geom_pos]["geometry"]
    return geometry

def search_sentinel_api(input_arguments, collection_name="sentinel-s2-l2a-cogs", min_cloud_cover_pct=10):
    """
    This function uses the sat-search package to search publicly available satellite imagery 
    we set the api to the element84 for searching of sentinel 2 data, and the collection for
    cloud optimized images.
    inputs: 
    - input arguments: dates of start and end date for the search
    - collection: collection of the datacatalog to search
    - min_cloud_cover_pct: minimum threshold of cloudcover for the returned images
    """
    input_geometry = read_input_geometry(input_arguments["input_geometry"])
    query = { "eo:cloud_cover": { "lt": min_cloud_cover_pct } }
    search = Search(
        url="https://earth-search.aws.element84.com/v0",
        intersects=input_geometry,
        datetime=input_arguments["start_date"] + "/" + input_arguments["end_date"],
        collections=[collection_name],
        query=query
    )
    return search

def get_sentinel_urls(bands=["red", "nir"]):
    """
    This function executes the search using the input parameters
    and returns a dictionary with the urls for downloading.
    inputs:
    - data bands that corresponds to the sentinel datasets from the satsearch.
    """
    search_scenes = search_sentinel_api(set_arguments_pipeline())
    urls = {}
    try: 
        items = search_scenes.items()
        items_dates = items.dates()
        band_info = {}
        for band in bands:
            for item in items:
                if band + "_band_info" not in band_info:
                    band_info[band + "_band_info"] = [item.asset(band)["href"]]
                else:
                    band_info[band + "_band_info"].append(item.asset(band)["href"])
        band_info["dates"] = items_dates
        return band_info
    except Exception as e:
        raise Exception("error in search scenes: ", e)
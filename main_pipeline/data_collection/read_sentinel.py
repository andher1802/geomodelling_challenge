from satsearch import Search
from datetime import datetime, timedelta
from pyproj import Transformer
from json import load
from utils.set_user_input import set_arguments_pipeline

def read_input_geometry(filename, geom_pos = 1):
    file_path = filename
    with open(file_path,"r") as fp:
        file_content = load(fp)
    geometry = file_content["features"][geom_pos]["geometry"]
    return geometry

def search_sentinel_api(input_arguments):
    input_geometry = read_input_geometry(input_arguments['input_geometry'])
    query = { "eo:cloud_cover": { "lt": 20 } }
    search = Search(
        url='https://earth-search.aws.element84.com/v0',
        intersects=input_geometry,
        datetime=input_arguments['start_date'] + "/" + input_arguments['end_date'],
        collections=['sentinel-s2-l2a-cogs'],
        query=query
    )
    return search

def get_sentinel_red_nir_urls():
    search_scenes = search_sentinel_api(set_arguments_pipeline())
    urls = {}
    try: 
        items = search_scenes.items()
        items_dates = items.dates()
        red_band_info = []
        nir_band_info = []
        for item in items:
            red_band_info.append(item.asset('red')["href"])
            nir_band_info.append(item.asset('nir')["href"])
        return {"red_band_info": red_band_info, "nir_band_info": nir_band_info, "dates": items_dates}
    except Exception as e:
        raise Exception("error in search scenes")
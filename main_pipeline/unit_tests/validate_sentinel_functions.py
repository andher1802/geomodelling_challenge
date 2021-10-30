import sys, os
import datetime
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
from utils.set_user_input import args_validation, set_arguments_values
from data_collection.read_sentinel import search_sentinel_api, get_sentinel_urls
from utils.raster_helper import read_input_geometry

@pytest.mark.parametrize(
    "input_parameters, expected_output_urls",
    [
        (
            {
                "start_date": "10-10-2021",
                "end_date": "28-10-2021",
                "input_geometry": "./main_pipeline/input_geometries/doberitz_multipolygon.geojson"
            }
         ,            
            {
                'red_band_info': [
                    'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/32/U/QD/2021/10/S2A_32UQD_20211010_0_L2A/B04.tif', 
                    'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/33/U/UU/2021/10/S2A_33UUU_20211010_0_L2A/B04.tif'
                ], 
                'nir_band_info': [
                    'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/32/U/QD/2021/10/S2A_32UQD_20211010_0_L2A/B08.tif', 
                    'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/33/U/UU/2021/10/S2A_33UUU_20211010_0_L2A/B08.tif'
                ], 
                'dates': [datetime.date(2021, 10, 10)]}
        )
    ]
)
def test_sample(input_parameters, expected_output_urls):
    start_date = input_parameters["start_date"]
    end_date = input_parameters["end_date"]
    input_geometry = input_parameters["input_geometry"]
    start_date_raw = datetime.datetime.strptime(start_date, "%d-%m-%Y")
    start_date_formatted = start_date_raw.strftime("%Y-%m-%d")
    end_date_raw = datetime.datetime.strptime(end_date, "%d-%m-%Y")
    end_date_formatted = start_date_raw.strftime("%Y-%m-%d")
    input_arguments = {"start_date":start_date_formatted,"end_date":end_date_formatted ,"input_geometry": input_geometry}
    search_scenes = search_sentinel_api(input_arguments)
    bands = ["red", "nir"]
    tif_urls = get_sentinel_urls(search_scenes, bands) 
    assert (expected_output_urls == tif_urls)
  

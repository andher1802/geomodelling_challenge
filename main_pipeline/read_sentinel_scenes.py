import rasterio
from rasterio.features import bounds

from satsearch import Search
from datetime import datetime, timedelta
from pyproj import Transformer
from json import load
from utils.set_user_input import set_arguments_pipeline

def read_sentinel_scenes():
    input_arguments = set_arguments_pipeline()
    print(input_arguments)

   

    
    
def main():
    read_sentinel_scenes()
    
if __name__ == '__main__':
    main()
from data_collection.read_sentinel import get_sentinel_urls, download_sentinel_data, search_sentinel_api
from utils.set_user_input import set_arguments_pipeline



def main():
    bands = ["red", "nir"]
    search_scenes = search_sentinel_api(set_arguments_pipeline())
    tif_urls = get_sentinel_urls(search_scenes, bands)
    download_sentinel_data(tif_urls)


if __name__ == "__main__":
    main()

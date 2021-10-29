from data_collection.read_sentinel import get_sentinel_urls, download_sentinel_data
from data_processing.compute_raster_features import compute_ndvi


def main():
    bands = ["red", "nir"]
    tif_urls = get_sentinel_urls(bands)
    # download_sentinel_data(tif_urls)
    ndvi_results = compute_ndvi(tif_urls)


if __name__ == "__main__":
    main()

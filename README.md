# README

The goal of this challenge is to create a Python script to search for Sentinel-2 scenes within a provided geometry and compute an average NDVI (Normalized Difference Vegetation Index).
This project is structured in different modules: data_collection, data_processing, and utils.

## Utils Module

Utils module provides all the helper functions that are used to provide a more friendly use of the package. It contains the user input handler and some methods to read and save raster data resulting from the processing stage.

## Data Collection

Data collection is the module that search for the Sentinel-2 scenes using the Element84 APi STAC catalog. It consists of 3 main methods:

- **search_sentinel_api**: performs a lazy search using satsearch and the Element84 APi STAC catalog.
- **get_sentinel_urls**: Excecutes the search and returns the urls for the resulting scenes, bands can be adjusted but by default are set to red and nir bands.
- **download_sentinel_data**: This method uses the urls from the previous step and downloads the scenes from the catalog. (This step is not required and not recommended for NDVI computation)

## Data Processing

This module contains all the processing steps for the package. Currently only has the NDVI computation using the urls from the `get_sentinel_urls` method.

# How to use this module

This project is designed to have a modular workflow. This design allows users/developers to create easy workflows located in the main_pipeline folder to reuse the methods written in the Data Collection and Data processing modules. Currently there are 2 workflows prepared for computing the NDVI of images that intersect an input geometry in a given period of time, and other that downloads the sentinel images that also intersect the time/region specifications.

The workflows only use 3 methods:

1. Prepare the user input validation.
2. Collect and retrieve the urls from the data catalog.
3. Process the images and store the result.

This is an example of the workflow for computing the NDVI.

```python
   from data_collection.read_sentinel import get_sentinel_urls, download_sentinel_data, search_sentinel_api
   from data_processing.compute_raster_features import compute_ndvi
   from utils.set_user_input import set_arguments_pipeline

   def main():
      bands = ["red", "nir"]
      search_scenes = search_sentinel_api(set_arguments_pipeline()) # prepare input arguments and use them for search the sentinel catalog
      tif_urls = get_sentinel_urls(search_scenes, bands) # get the urls from the search result
      ndvi_results = compute_ndvi(tif_urls) # computes the NDVI and store the results
```

The following are the instructions for installing and running these worflows.

## Install the dependencies

There are two options for installing this package:

### Option 1. Using the module in the local computer

You can use this module by creating a virtual environment and install the required dependencies that are located in the requirement.txt file.

Before you install the dependencies make sure the dependencies of gdal (libgdal-dev, etc.) are installed depending your OS.

1. go to the root folder (geomodelling_challenge-main)
2. in a terminal window type:
   - `virtualenv "name-virtual-env"`
   - `source "name-virtual-env"/bin/activate`
   - `pip install -r requirements.txt`
3. set the STAC_API_URL environment by typing
   - `export STAC_API_URL="https://earth-search.aws.element84.com/v0"`

### Option 2. Using the docker image

If you do not want to install all dependencies, and have docker installed in your computer, you can use the dockerfile that is located on the root folder of this project. Then access the modules from the jupyter lab that is set by the container. For doing this run in your terminal the following commands (from the root folder of this project):

- `docker build -t geo-modelling-challenge .` (geo-modelling-challenge is the name of the image, you can change it accordingly your preferences).
- `docker run -p 8888:8888 geo-modelling-challenge` (port mapping for the jupyter lab)

Once you access the jupyter lab you can go to the terminal inside the jupyter IDE, activate the conda geo_pipeline environment and run the package using the instructions on the next section. For having persistent results you should add a docker volume and set the output folder accordingly.

**IMPORTANT**: The docker image building step requires around 5Gb of disk and lasts around 2 hours in a 8Gb RAM laptop.

## Run the package

There is a main script already prepared for running the workflow of the package in the main_pipeline folder `compute_ndvi_images.py`. This script performs the search on the datacatalog between two dates (time range for the analysis) and an intersected input geometry. Then it computes the NDVI for each resulting image in the catalog, and saves the result in raster format (.tif files with the same crs than the original sentinel image):

To run the script you should open a terminal and from the root folder (geomodelling_challenge-main or root in the case of the docker container) and type:

- `python main_pipeline/compute_ndvi_images.py --start_date <start_date> --end_date <end_date>`

This workflow allows the user to include several input parameters:

- **start_date**: The start date for the search and analysis. Format is dd-mm-yyy (no quotes and with hyphen between day, month and year). Default value is the end_date less 10 days.
- **end_date**: The end date for the search and analysis. Format is dd-mm-yyyy (The input handler does not allow end-dates in the future nor start dates after end dates). Default value is the current date.
- **input geometry**: The relative path to the geojson for the search. (default is ./main_pipeline/input_geometries/doberitz_multipolygon.geojson)
- **folder**: relative path to store the results. (default is ./sentinel_data)

**IMPORTANT**: It is important to run the script from the root folder, taking into account that the default values of the input arguments are relative to this folder. You also can adjust this parameters by providing the appropiate input_geometry and folder paths.

Similarly, there is an alternative workflow that allows to download the image that resulted from the search catalog. (This worflow downloads the large images from sentinel therefore should be used with caution)

- `python main_pipeline/download_sentinel_images.py --start_date <start_date> --end_date <end_date>`

## Results and Clustering Analysis

On the root folder, there is a jupyter notebook to see the results of the NDVI computation and conducts a k-means clustering analysis over the stacked NDVI images located in the folder sentinel_data/NDVI_SEL/ (The selected scenes for our analysis)

To run this notebook, please install jupyter lab and open the `main_workflow.ipynb` file in the jupyter lab environment.
In this notebook also you can visualize the images located in the NDVI_TEST folder. The expected output can be found here [Challenge result](https://andher1802.github.io/geomodelling_challenge/main_workflow.html)

## Unit Testing

This package also contains unit test for the main workflow that uses a known input and tests the expected output resulting from the data catalog search.
This tests is used to check if everything goes as expected after changes made to the main workflow or other methods in the project.

To run the unit test (from the main folder of the application) type on the terminal:

- `pytest main_pipeline/unit_tests/validate_sentinel_functions.py`

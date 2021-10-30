# README

The goal of this challenge is to create a Python script to search for Sentinel-2 scenes within a provided geometry and compute an average NDVI (Normalized Difference Vegetation Index).
This module is structured in different modules: data_collection, data_processing, and utils.

## Utils Module

Utils module provides all the helper functions that are used to provide a more friendly use of the package. It contains the user input handler and some methods to read and save raster data resulting from the processing stage.

## Data Collection

Data collection is the module that search for the Sentinel-2 scenes using the Element84 APi STAC catalog. It consists of 3 main methods:

- **search_sentinel_api**: performs a lazy search using satsearch and the Element84 APi STAC catalog.
- **get_sentinel_urls**: Excecutes the search and returns the urls for the resulting scenes, bands can be adjusted but by default is set to red and nir bands.
- **download_sentinel_data**: This method uses the urls from the previous step and download the scenes from the catalog. (This step is not required and not recommended for NDVI computation)

## Data Processing

This module contains all the processing steps for the package. Currently only has the NDVI computation using the urls from the `get_sentinel_urls` method.

# How to use this module

This project is design to have a modular workflow. This design allows users/developers to create easy workflows located in the main_pipeline folder to reuse the methods written in the Data Collection and Data processing modules. Currently there are 2 workflows prepared for computing the NDVI of images that intersect an input geometry and in a given period of time, and other that downloads the sentinel images that also intersect the time/region specifications.

The workflows only use 3 methods:

1. Prepare the user input validation.
2. Collect and retrieve the urls from the data catalog.
3. Process the images and store the result.

The following are the instructions for installing and running these worflows.

## Install the dependencies

### Using the module in the local computer

You can use this module by creating a virtual environment and install the required dependencies that are located in the requirement.txt file.

Before you install the dependencies make sure the dependencies of gdal (libgdal-dev, etc.) are installed depending your OS.

1. go to the root folder (geomodelling_challenge-main)
2. in a terminal window type:
   - `virtualenv "name-virtual-env"`
   - `source "name-virtual-env"/bin/activate`
   - `pip install -r requirements.txt`
3. set the STAC_API_URL environment by typing
   - `export STAC_API_URL="https://earth-search.aws.element84.com/v0"`

### Using the docker image

A relatively easier installation is to use the dockerfile that is on the root folder of the project, and access the module from the jupyter lab that is set by the container.
For doing this process you have to install docker in your OS, and run the following commands:

- `docker build -t geo-modelling-challenge .` (geo-modelling-challenge is the name of the image, you can change it accordingly your preferences).
- `docker run -p 8888:8888 geo-modelling-challenge` (port mapping for the jupyter lab)

Once you access the jupyter lab you can go to the terminal inside the jupyter environmen, activate the conda geo_pipeline environment and run the package using the instructions on the next section. For having persistent results you should add a docker volume and set the output folder accordingly.

**IMPORTANT**: The docker image building step requires arounf 5Gb of disk and lasts around 2 hours in a 8Gb RAM laptop.

## Run the package

There is a main script already prepared for running the workflow of the package in the main_pipeline folder `compute_ndvi_images.py`. This script do the search on the datacatalog between two dates and an intersect input geometry, computes the NDVI, and save the result int the output folder in raster format (.tif with the same crs than the original sentinel image):

To run the script you should open a terminal and from the root folder (geomodelling_challenge-main) in type:

- `python main_pipeline/compute_ndvi_images.py --start_date <start_date> --end_date <end_date>`

This workflow allows the user to include several input parameters:

- **start_date**: The start date for the search and analysis. Format is dd-mm-yyy (no quotes and with hyphen between day, month and year). Default value is the end_date less 10 days.
- **end_date**: The end date for the search and analysis. Format is dd-mm-yyyy (The input handler does not allow end-dates in the future nor start dates after end dates). Default value is the current date.
- **input geometry**: The relative path to the geojson for the search. (default is ./main_pipeline/input_geometries/doberitz_multipolygon.geojson)
- **folder**: relative path to store the results. (default is ./sentinel_data)

**IMPORTANT**: It is important to run the script from the root folder, taking into account that the default values of the input arguments are relative to this folder. You also can adjust this parameters by providing the appropiate input_geometry and folder paths.

Similarly, there is an alternative workflow that allows to download the image that resulted from the search catalog. (This downloads the large images from sentinel therefore should be used with caution)

- `python main_pipeline/download_sentinel_images.py --start_date <start_date> --end_date <end_date>`

## Results and Clustering Analysis

On the root folder, there is a jupyter notebook to see the results of the analysis and conduct a k-means clustering analysis over the stacked NDVI images located in the folder sentinel_data/NDVI_SEL/ (The selected scenes for our analysis)

To run this notebook, please install jupyter lab and open the notebook in the jupyter lab environment.
In this notebook also you can visualize the images located in the NDVI_TEST folder. The expected output can be found here [Challenge result](https://github.com/andher1802/geomodelling_challenge/blob/main/main_workflow.ipynb)

## Unit Testing

This package provides a unit test for the main workflow that uses a know input to test the expected output of the urls that resulted from the data catalog search.
This tests is used to check if everythig goes as expected after changes to the main workflow of the applications.

To run the unit test (from the main folder of the application) type on the terminal:

- `pytest main_pipeline/unit_tests/validate_sentinel_functions.py`

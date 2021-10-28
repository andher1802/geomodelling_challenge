from data_collection.read_sentinel import *
        
def main():
    bands=["red", "nir"]
    tif_data = get_sentinel_urls(bands)
    
    
       
    print(
        len(tif_data["red_band_info"]),
        len(tif_data["nir_band_info"]),
        len(tif_data["dates"]),
    )
        
    
if __name__ == "__main__":
    main()
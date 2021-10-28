from data_collection.read_sentinel import *
        
def main():
    tif_data = get_sentinel_red_nir_urls()
    print(
        len(tif_data["red_band_info"]),
        len(tif_data["nir_band_info"]),
        len(tif_data["dates"]),
    )
    for date_img in tif_data["dates"]:
        print(date_img.strftime('%Y-%m-%d'))
        
    
if __name__ == '__main__':
    main()
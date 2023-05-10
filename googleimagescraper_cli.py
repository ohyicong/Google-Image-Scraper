import argparse
import concurrent.futures
import os
from patch import webdriver_executable
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper
import sys
 

def worker_thread(search_key):
    print("[INFO] Starting worker thread for search key: {}".format(search_key))
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        searchname,
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    print(max_missed)
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)
    

    #Release resources
    del image_scraper


def list_arg(string):
    """
    Custom action to convert a string argument to a list.
    """
    try:
        # Split the string into a list using a comma
        lst = string.split(',')
        return lst
    except:
        # Raise an error if the string is not valid
        raise argparse.ArgumentTypeError("Invalid list argument: {}".format(string))
    
def tuple_arg(string):
    """
    Custom action to convert a string argument to a tuple.
    """
    try:
        # Split the string into two integers using a comma
        x, y = map(int, string.split(','))
        return x, y
    except:
        # Raise an error if the string is not valid
        raise argparse.ArgumentTypeError("Invalid tuple argument: {}".format(string))


if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'images'))



    #Parameters from argparse
    
    parser = argparse.ArgumentParser(description='Google Image Scraper CLI Tool', usage='%(prog)s [options]')    
    parser.add_argument('--number_of_images', type=int, default=5, help='The number of images to download (default: 5)')
    parser.add_argument('--headless', type=bool, default=False, help='Whether to run in headless mode (default: False)')
    parser.add_argument('--min_resolution', type=tuple_arg, default=(0, 0), help='The minimum desired image resolution (default: (0,0))')
    parser.add_argument('--max_resolution', type=tuple_arg, default=(10000, 10000), help='The maximum desired image resolution (default: (10000,10000))')
    parser.add_argument('--max_missed', type=int, default=10, help='The maximum number of failed images before exiting (default: 10)')
    parser.add_argument('--number_of_workers', type=int, default=1, help='The number of workers to use (default: 1)')
    parser.add_argument('--keep_filenames', type=bool, default=False, help='Whether to keep original URL image filenames (default: False)')
    parser.add_argument('--searchname', type=str, default='search', help='The name of the subfolder in which images will be saved (default: "search")')
    parser.add_argument('--search_keys', type=list_arg, help='The list of search keys to use (default: ["cat","t-shirt"])')
    
    args = parser.parse_args()
    number_of_images = args.number_of_images                # Desired number of images
    headless = args.headless                     # True = No Chrome GUI
    min_resolution = args.min_resolution             # Minimum desired image resolution
    max_resolution = args.max_resolution       # Maximum desired image resolution
    max_missed = args.max_missed                 # Max number of failed images before exit
    number_of_workers = args.number_of_workers             # Number of "workers" used
    keep_filenames = args.keep_filenames            # Keep original URL image filenames
    searchname = args.searchname               # Name of subfolder in which images will be saved
    
    search_keys = args.search_keys
    if not search_keys:
        print("Error: You must provide at least one search key with --search_keys")
        sys.exit(1)

    
    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    #Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.number_of_workers) as executor:
        print("Starting threads...")
        executor.map(worker_thread, search_keys)

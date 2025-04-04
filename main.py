# -*- coding: utf-8 -*-
"""
Google Image Scraper
A script to download images from Google Images based on search terms.
"""

# Import required libraries
import os
import concurrent.futures
import chromedriver_autoinstaller
from GoogleImageScraper import GoogleImageScraper
from patch import webdriver_executable


def worker_thread(search_key):
    """
    Worker thread function that handles image scraping for a single search term
    
    Args:
        search_key (str): The search term to scrape images for
    """
    # Initialize scraper with configuration parameters
    image_scraper = GoogleImageScraper(
        webdriver_path, 
        image_path, 
        search_key, 
        number_of_images, 
        headless, 
        min_resolution, 
        max_resolution, 
        max_missed)
    
    # Get image URLs and save them to disk
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)

    # Release resources
    del image_scraper

if __name__ == "__main__":
    # Auto-install chromedriver for the current Chrome version
    chromedriver_path = chromedriver_autoinstaller.install()
    
    # Create photos directory if it doesn't exist
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))
    os.makedirs(image_path, exist_ok=True)
    
    # Use the detected chromedriver path
    webdriver_path = chromedriver_path

    # Collect search terms from user input
    user_input = input("Enter search terms separated by commas: ")
    search_keys = [term.strip() for term in user_input.split(',') if term.strip()]
    
    # Exit if no valid search terms were provided
    if not search_keys:
        print("No valid search terms provided. Exiting...")
        exit()

    print(f"Will search for: {', '.join(search_keys)}")

    # Configuration parameters
    number_of_images = 10               # Number of images to download per search term
    headless = False                    # Whether to run Chrome in headless mode
    min_resolution = (0, 0)             # Minimum image resolution (width, height)
    max_resolution = (9999, 9999)       # Maximum image resolution (width, height)
    max_missed = 10                     # Maximum number of consecutive download failures before stopping
    number_of_workers = min(len(search_keys), 4)  # Number of parallel threads (max 4)
    keep_filenames = False              # Whether to keep original filenames from URLs

    # Run searches in parallel threads
    # Each thread handles one search term
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
# Import libraries
import os
import concurrent.futures
from typing import List

from GoogleImageScraper import GoogleImageScraper
from google_site_scrapper import GoogleAISiteScrapper
from patch import webdriver_executable
from os.path import join

from services.gspread_service import GoogleSheetsService

def worker_thread_descriptions(search_key):
    description_scraper = GoogleAISiteScrapper(
        webdriver_path,
        description_path,
        search_key,
        number_of_results=1,
        headless=headless
    )
    description = description_scraper.find_product_description()
    print(description)
    del description_scraper

def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path,
        image_path,
        search_key,
        number_of_images,
        headless,
        min_resolution,
        max_resolution,
        max_missed,
        use_brave=True,
    )
    image_urls = image_scraper.find_image_urls()
    # image_scraper.save_images(image_urls, keep_filenames)

    # Release resources
    del image_scraper


def load_search_terms() -> List[str]:
    with open(join("input", "products.txt")) as f:
        terms = f.readlines()
        return [term.replace("\n", "") for term in terms]


if __name__ == "__main__":
    # Define file path
    gs_service = GoogleSheetsService()

    webdriver_path = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", webdriver_executable())
    )
    image_path = os.path.normpath(os.path.join(os.getcwd(), "photos"))

    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    # search_keys = load_search_terms()
    search_keys = gs_service.get_items("Product", "Images found")
    description_path = os.path.normpath(os.path.join(os.getcwd(), 'descriptions'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    # search_keys = load_search_terms()

    #Parameters
    number_of_images = 5                # Desired number of images
    headless = False                     # True = No Chrome GUI
    min_resolution = (0, 0)             # Minimum desired image resolution
    max_resolution = (9999, 9999)       # Maximum desired image resolution
    max_missed = 10                     # Max number of failed images before exit
    number_of_workers = 1              # Number of "workers" used
    keep_filenames = False              # Keep original URL image filenames

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    #Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread_descriptions, search_keys)

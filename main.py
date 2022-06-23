# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
import concurrent.futures
from GoogleImageScrapper import GoogleImageScraper
from patch import webdriver_executable


def worker_thread(search_key):
    image_scrapper = GoogleImageScraper(
        webdriver_path, image_path, search_key, number_of_images, headless, min_resolution, max_resolution)
    image_urls = image_scrapper.find_image_urls()
    image_scrapper.save_images(image_urls)

    #Release resources
    del image_scrapper

if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = ['apple', 't-shirt']

    #Parameters
    number_of_images = 10               # Desired number of images
    headless = True                    # True = No Chrome GUI
    min_resolution = (0, 0)            # Minimum desired image resolution
    max_resolution = (9999, 9999)      # Maximum desired image resolution
    max_missed = 10                    # Max number of failed images before exit
    number_of_workers = 1              # Number of "workers" used

    #Run each search_key in a separate thread
    #Automatically waits for all threads to finish
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        executor.map(worker_thread, search_keys)

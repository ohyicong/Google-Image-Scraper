# Google Image Scraper
 A library to scrap google images
 
 Pre-requisites:
 1. Pip install Selenium Library
 2. Download Google Chrome 
 3. Download Google Webdriver based on your Chrome version
 
 
Usage:

import os

from GoogleImageScrapper import GoogleImageScraper


webdriver_path = os.getcwd()+"\\webdriver\\chromedriver.exe"

image_path = os.getcwd()+"\\photos"

image_scrapper = GoogleImageScraper(webdriver_path,image_path,"cat",10)

image_urls = image_scrapper.find_image_urls()

image_scrapper.save_images(image_urls)

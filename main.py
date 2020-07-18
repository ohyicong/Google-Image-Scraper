# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

T
"""


#pip install selenium
#install chrome
#download chromedriver based on your chrome version

from GoogleImageScrapper import GoogleImageScraper
import os

webdriver_path = os.getcwd()+"\\webdriver\\chromedriver.exe"
image_path = os.getcwd()+"\\photos"
image_scrapper = GoogleImageScraper(webdriver_path,image_path,"cat",10)
image_urls = image_scrapper.find_image_urls()
image_scrapper.save_images(image_urls)

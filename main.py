# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
from GoogleImageScrapper import GoogleImageScraper
from GettyImagesScrapper import GettyImageScraper
from patch import webdriver_executable

if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Website used for scraping: 
    website_list = ['google', 'getty']
    search_site = website_list[1] #change index number here to select the website you are using

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys= ['tugboat']

    #Parameters
    number_of_images = 10
    headless = False
    min_resolution=(0,0)
    max_resolution=(9999,9999)

    #Main program
    #Choose if using Google or Getty Images Scrapper
    for search_key in search_keys:
        if search_site == 'google':
            image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
        else:
            image_scrapper = GettyImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
        image_urls = image_scrapper.find_image_urls()
        image_scrapper.save_images(image_urls)
    
    #Release resources    
    del image_scrapper
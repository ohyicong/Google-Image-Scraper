# Google Image Scraper
A library to scrap google images

## Pre-requisites:
1. Pip install Selenium Library
2. Pip install PIL
3. Download Google Chrome 
4. Download Google Webdriver based on your Chrome version

## Example:
```
run main.py
```

## Usage:
```
#Import libraries (Don't change)
from GoogleImageScrapper import GoogleImageScraper
import os

#Define file path (Don't change)
webdriver_path = os.path.normpath(os.getcwd()+"\\webdriver\\chromedriver.exe")
image_path = os.path.normpath(os.getcwd()+"\\photos")

#Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
search_keys= ["cat","t-shirt"]

#Parameters
number_of_images = 10
headless = True
min_resolution=(0,0)
max_resolution=(1920,1080)

#Main program
for search_key in search_keys:
    image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
    image_urls = image_scrapper.find_image_urls()
    image_scrapper.save_images(image_urls)

```
## Youtube Video:
[![IMAGE ALT TEXT](https://github.com/ohyicong/Google-Image-Scraper/blob/master/youtube_thumbnail.PNG)](https://youtu.be/QZn_ZxpsIw4 "Google Image Scraper")

Do remember to like, share and subscribe!

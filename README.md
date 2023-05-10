# Google Image Scraper
A library created to scrape Google Images.<br>
If you are looking for other image scrapers, JJLimmm has created image scrapers for Gettyimages, Shutterstock, and Bing. <br>
Visit their repo here: https://github.com/JJLimmm/Website-Image-Scraper

## Pre-requisites:
1. Google Chrome
2. Python3 packages (Pillow, Selenium, Requests)
3. Windows OS (Other OS is not tested)

## Setup:
1. Open command prompt
2. Clone this repository (or [download](https://github.com/ohyicong/Google-Image-Scraper/archive/refs/heads/master.zip))
    ```
    git clone https://github.com/ohyicong/Google-Image-Scraper
    ```
3. Install Dependencies
    ```
    pip install -r requirements.txt
    ```
4. Edit your desired parameters in main.py
    ```
    search_keys         = Strings that will be searched for
    number of images    = Desired number of images
    headless            = Chrome GUI behaviour. If True, there will be no GUI
    min_resolution      = Minimum desired image resolution
    max_resolution      = Maximum desired image resolution
    max_missed          = Maximum number of failed image grabs before program terminates. Increase this number to ensure large queries do not exit.
    number_of_workers   = Number of sectioned jobs created. Restricted to one worker per search term and thread.
    ```
4. Run the program
    ```
    python main.py
    ```

## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images.
In the project repository, run:

```
python googleimagescraper_cli.py --search-keys cat
```
Optional arguments:

```
--number_of_images: The number of images to download (default: 5)
--headless:   Whether to run in headless mode (default: False)
--min_resolution: The minimum desired image resolution (default: (0,0))
--max_resolution: The maximum desired image resolution (default: (10000,10000))
--max_missed: The maximum number of failed images before exiting (default: 10)       
--number_of_workers: The number of workers to use (default: 1)
--keep_filenames: Whether to keep original URL image filenames (default: False)
--searchname: The name of the subfolder in which images will be saved (default: "search")
```

Otherwise, define your desired parameters in main.py and run through the command line:
```
python main.py
```

## Youtube Video:
[![IMAGE ALT TEXT](https://github.com/ohyicong/Google-Image-Scraper/blob/master/youtube_thumbnail.PNG)](https://youtu.be/QZn_ZxpsIw4 "Google Image Scraper")


## IMPORTANT:
Although it says so in the video, this program will not run through VSCode. It must be run in the command line.

This program will install an updated webdriver automatically. There is no need to install your own.

### Please like, subscribe, and share if you found my project helpful! 

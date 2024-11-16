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
    uv sync
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
    uv run python main.py
    ```

## Usage:
This project was created to bypass Google Chrome's new restrictions on web scraping from Google Images. 
To use it, define your desired parameters in main.py and run through the command line:
```
python main.py
```
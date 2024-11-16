import os
import patch
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from bs4 import BeautifulSoup


class GoogleAISiteScrapper:
    def __init__(
        self,
        webdriver_path,
        description_path,
        search_key="",
        number_of_results=1,
        headless=True,
    ):
        # check parameter types
        output_path = os.path.join(description_path, search_key)
        if type(number_of_results) != int:
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(output_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(output_path)

        # check if chromedriver is installed
        if not os.path.isfile(webdriver_path):
            is_patched = patch.download_lastest_chromedriver()
            if not is_patched:
                exit(
                    "[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads"
                )

        for i in range(1):
            try:
                # try going to www.google.com
                options = Options()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Chrome(webdriver_path, chrome_options=options)
                driver.set_window_size(1400, 1050)
                driver.get("https://www.google.com")
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "W0wltc"))
                    ).click()
                except Exception as e:
                    continue
            except Exception as e:
                # update chromedriver
                pattern = "(\d+\.\d+\.\d+\.\d+)"
                version = list(set(re.findall(pattern, str(e))))[0]
                is_patched = patch.download_lastest_chromedriver(version)
                if not is_patched:
                    exit(
                        "[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads"
                    )

        self.driver = driver
        self.search_key = search_key
        self.number_of_results = number_of_results
        self.webdriver_path = webdriver_path
        self.image_path = output_path
        self.url = "https://www.google.com/search?q=%s" % (search_key)
        self.headless = headless

    def find_product_description(self):
        """
        This function search and return a list of image urls based on the search key.
        Example:
            google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
            image_urls = google_image_scraper.find_image_urls()

        """
        SLEEP_TIME = 1
        print("[INFO] Gathering image links")
        self.driver.get(self.url)
        image_urls = []
        count = 0
        missed_count = 0
        time.sleep(3)

        while self.number_of_results > count:
            results = self.driver.find_elements(
                by=By.XPATH, value="//h3[contains(@class,'LC20lb MBeuO DKV0Md')]"
            )
            time.sleep(3)
            for result in results:
                result.click()

                url = self.driver.current_url
                website_data = BeautifulSoup(url, "html.parser")
                print(url)

                str_repr = website_data.get_text()
                print(str_repr)

        self.driver.quit()

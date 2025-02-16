import os
import logging
import concurrent.futures
from typing import List

from GoogleImageScraper import GoogleImageScraper
from google_site_scrapper import GoogleAISiteScrapper
from patch import webdriver_executable
from os.path import join

from services.gdrive_service import GoogleDriveService
from services.gspread_service import GoogleSheetsService
from services.openai_service import OpenAIService


def worker_experiment(search_key):
    openai_service = OpenAIService()
    sheets_service = GoogleSheetsService()

    logging.info("retrieving description...")
    description_scraper = GoogleAISiteScrapper(
        webdriver_path,
        description_path,
        search_key,
        number_of_results=1,
        headless=headless,
        use_brave=False,
    )
    description_scraper.find_product_description(openai_service, sheets_service)
    del description_scraper
    logging.info("retrieving images...")

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
    image_scraper.find_image_urls()

    del image_scraper
    del openai_service
    del sheets_service


def worker_thread_descriptions(search_key):
    openai_service = OpenAIService()
    sheets_service = GoogleSheetsService("Inventario", "Inventario")

    description_scraper = GoogleAISiteScrapper(
        webdriver_path,
        description_path,
        search_key,
        number_of_results=1,
        headless=headless,
        use_brave=True,
    )
    description_scraper.find_product_description(openai_service, sheets_service)
    del description_scraper
    del openai_service
    del sheets_service


def worker_thread(search_key):
    sheets_service = GoogleSheetsService("Inventario", "Inventario")
    google_drive_service = GoogleDriveService()

    image_scraper = GoogleImageScraper(
        webdriver_path,
        image_path,
        search_key,
        number_of_images,
        headless,
        min_resolution,
        max_resolution,
        max_missed,
        use_brave=False,
    )
    image_scraper.find_image_urls()
    image_scraper.update_product_images("inventario", sheets_service, google_drive_service)
    del image_scraper
    del sheets_service
    del google_drive_service


def load_search_terms() -> List[str]:
    with open(join("input", "products.txt")) as f:
        terms = f.readlines()
        return [term.replace("\n", "") for term in terms]


if __name__ == "__main__":
    # Define file path
    logging.basicConfig(level=logging.INFO)
    gs_service = GoogleSheetsService("Inventario", "Inventario")

    webdriver_path = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", webdriver_executable())
    )
    image_path = os.path.normpath(os.path.join(os.getcwd(), "photos"))

    # search_keys = load_search_terms()
    search_keys = gs_service.get_items(
        product_list_column="Nombre del artículo",
        done_column="Processed",
        sku_column="ID del artículo",
    )
    logging.info("searching for {} items...".format(len(search_keys)))
    description_path = os.path.normpath(os.path.join(os.getcwd(), "descriptions"))

    # search_keys = load_search_terms()
    num_cores = os.cpu_count()
    logging.info("using {} cores".format(num_cores))

    # Parameters
    number_of_images = 1  # Desired number of images
    headless = False  # True = No Chrome GUI
    min_resolution = (0, 0)  # Minimum desired image resolution
    max_resolution = (9999, 9999)  # Maximum desired image resolution
    max_missed = 10  # Max number of failed images before exit
    number_of_workers = 16  # Number of "workers" used
    keep_filenames = False  # Keep original URL image filenames

    # Run each search_key in a separate thread
    # Automatically waits for all threads to finish
    # Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        executor.map(worker_thread, search_keys)

# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:44:43 2021

@author: Yicong
"""
from sys import platform

import requests
#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
import sys
import os
import re
import zipfile
import stat
import json
import shutil
import platform as sys_platform

def webdriver_executable():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return 'chromedriver'
    return 'chromedriver.exe'


def download_latest_chromedriver(current_chrome_version="130") -> str:
    def get_platform_filename():
        is_64bits = sys.maxsize > 2 ** 32
        platform = sys_platform.system()

        if platform == "linux" or platform == "linux2":
            return 'linux64'

        elif platform == "Darwin":
            machine = sys_platform.machine()
            if machine == "x86_64":
                return 'mac-x64'
            elif machine == "arm64":
                return 'mac-arm64'

        elif platform == "win32":
            return 'win32'

        return filename

    # Find the latest chromedriver, download, unzip, set permissions to executable.

    result = False
    try:
        url = 'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json'

        # Download latest chromedriver.
        stream = requests.get(url)
        # stream = urllib.request.urlopen(url)
        content = stream.json()

        # Parse the latest version.
        driver_url = ""
        if current_chrome_version != "":
            match = re.search(r'\d+', current_chrome_version)
            downloads = content["milestones"][match.group()]

        else:
            for milestone in content["milestones"]:
                downloads = content["milestones"][milestone]

        for download in downloads["downloads"]["chromedriver"]:
            if download["platform"] == get_platform_filename():
                driver_url = download["url"]

        # Download the file.
        print('[INFO] downloading chromedriver ver: %s: %s' % (
        current_chrome_version, driver_url))
        file_name = driver_url.split("/")[-1]
        app_path = os.getcwd()
        download_path = os.path.join(app_path, 'webdriver')
        chromedriver_path = os.path.normpath(
            os.path.join(download_path, webdriver_executable()))
        file_path = os.path.normpath(os.path.join(app_path, 'webdriver', file_name))
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        # urllib.request.urlretrieve(driver_url, file_path)
        with requests.get(driver_url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(
                        chunk_size=8192):  # Download in 8KB chunks
                    file.write(chunk)

        # Unzip the file into folde

        webdriver_path = os.path.normpath(os.path.join(app_path, 'webdriver'))
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue
                source = zip_file.open(member)
                target = open(os.path.join(webdriver_path, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

        st = os.stat(chromedriver_path)
        os.chmod(chromedriver_path, st.st_mode | stat.S_IEXEC)
        print('[INFO] latest chromedriver downloaded')
        # Cleanup.
        os.remove(file_path)
        result = True
    except Exception as e:
        print(e)
        print(
            "[WARN] unable to download lastest chromedriver. the system will use the local version instead.")

    return result

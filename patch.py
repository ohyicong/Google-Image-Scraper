# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:44:43 2021

@author: Yicong
"""
#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
import sys
import os
import urllib.request
import re
import zipfile
import stat
from sys import platform

def webdriver_executable():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return 'chromedriver'
    return 'chromedriver.exe'

def download_lastest_chromedriver(current_chrome_version=""):
    def get_platform_filename():
        filename = ''
        is_64bits = sys.maxsize > 2**32
    
        if platform == "linux" or platform == "linux2":
            # linux
            filename += 'linux'
            filename += '64' if is_64bits else '32'
        elif platform == "darwin":
            # OS X
            filename += 'mac64'
        elif platform == "win32":
            # Windows...
            filename += 'win32'
    
        filename += '.zip'
    
        return filename
    
    # Find the latest chromedriver, download, unzip, set permissions to executable.
    
    result = False
    try:
        url = 'https://chromedriver.chromium.org/downloads'
        base_driver_url = 'https://chromedriver.storage.googleapis.com/'
        file_name = 'chromedriver_' + get_platform_filename()
        pattern = 'https://.*?path=(\d+\.\d+\.\d+\.\d+)'
    
        # Download latest chromedriver.
        stream = urllib.request.urlopen(url)
        content = stream.read().decode('utf8')
    
        # Parse the latest version.
        all_match = re.findall(pattern, content)
        
        if all_match:
            # Find chromedriver 
            if (current_chrome_version!=""):
                all_match = list(set(re.findall(pattern, content)))
                current_chrome_version = ".".join(current_chrome_version.split(".")[:-1])
                version_match = [i for i in all_match if re.search("^%s"%current_chrome_version,i)]
                version = list(set(version_match))[0]
            else:
                version = all_match[1]
            
            driver_url = base_driver_url + version + '/' + file_name    
            # Download the file.
            print('[INFO] downloading chromedriver ver: %s: %s'% (version, driver_url))
            app_path = os.path.dirname(os.path.realpath(__file__))
            chromedriver_path = os.path.normpath(os.path.join(app_path, 'webdriver', webdriver_executable()))
            file_path = os.path.normpath(os.path.join(app_path, 'webdriver', file_name))
            urllib.request.urlretrieve(driver_url, file_path)
    
            # Unzip the file into folder
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.normpath(os.path.join(app_path, 'webdriver')))
            st = os.stat(chromedriver_path)
            os.chmod(chromedriver_path, st.st_mode | stat.S_IEXEC)
            print('[INFO] lastest chromedriver downloaded')
            # Cleanup.
            os.remove(file_path)
            result = True
    except Exception:
        print("[WARN] unable to download lastest chromedriver. the system will use the local version instead.")
    
    return result


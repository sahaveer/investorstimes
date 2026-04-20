from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


import config
import streamlit as st

def getedgedriver():
    # Edge is generally not available on Streamlit Cloud (Linux)
    if config.is_cloud():
        # Fallback to Chrome on cloud
        return getchromedriver()
    
    try:
        driver_path = config.Config.get_driver_path("EDGE") or r'C://Users/sahaveer/PycharmProjects/msedgedriver.exe'
        service = Service(executable_path=driver_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        st.error(f"Error initializing Edge driver: {e}")
        return None

def getchromedriver():
    try:
        options = Options()
        
        if config.is_cloud():
            # Mandatory flags for Streamlit Cloud / Linux
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            
            # Set download directory for headless mode
            download_dir = os.path.abspath("./downloads/")
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
            
            # On Streamlit Cloud, chromium-driver is usually in /usr/bin/chromedriver
            # if installed via packages.txt
            service = Service() # Default service search
        else:
            # Local Mode
            driver_path = config.Config.get_driver_path("CHROME") or r'C://Users/sahaveer/PycharmProjects/chromedriver.exe'
            service = Service(executable_path=driver_path)
            
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        st.error(f"Error initializing Chrome driver: {e}")
        return None

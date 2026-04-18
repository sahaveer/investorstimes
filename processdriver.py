from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


import config
import streamlit as st

def getedgedriver():
    if config.is_cloud():
        st.warning("Webdriver is not available in the cloud environment.")
        return None
    
    try:
        # Local path for development. Consider moving this to a config or environment variable.
        driver_path = getattr(st.secrets, "EDGE_DRIVER_PATH", r'C://Users/sahaveer/PycharmProjects/msedgedriver.exe')
        service = Service(executable_path=driver_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing Edge driver: {e}")
        return None

def getchromedriver():
    if config.is_cloud():
        st.warning("Webdriver is not available in the cloud environment.")
        return None

    try:
        driver_path = getattr(st.secrets, "CHROME_DRIVER_PATH", r'C://Users/sahaveer/PycharmProjects/chromedriver.exe')
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        return None

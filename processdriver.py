from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def getedgedriver():
    try:
        service = Service(executable_path=r'C://Users/sahaveer/PycharmProjects/msedgedriver.exe')
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        print(e)

def getchromedriver():
    service = Service(executable_path=r'C://Users/sahaveer/PycharmProjects/chromedriver.exe')
    options = webdriver.ChromeOptions()
    #options.add_argument("user-data-dir=selenium")
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    # Initialize the Chrome driver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Edge(r"C://Users/sahaveer/PycharmProjects/msedgedriver.exe", )
    return driver

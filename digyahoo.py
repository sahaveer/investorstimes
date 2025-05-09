from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse, parse_qs

def get_yahoocode(browser,isin):
    # Navigate to the Yahoo Finance lookup page
    browser.get("https://finance.yahoo.com/lookup")

    # Wait for the page to load (you can use WebDriverWait for more robust waiting)
    time.sleep(1)

    # Find the search bar by XPath or ID
    search_bar_xpath = '/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/input[1]'
    search_bar_byID = 'yfin-usr-qry'
    search_bar = browser.find_element(by=By.XPATH, value=search_bar_xpath)

    # Enter the ISIN number into the search bar
    search_bar.send_keys(isin)
    # Find and click the submit search button by XPath or ID
    time.sleep(2)

    submit_search = '/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/div[1]/button'
    submit_search_byID = 'header-desktop-search-button'
    # Click the submit button
    submit_button = browser.find_element(by=By.XPATH, value=submit_search)
    submit_button.click()
    # Wait for the search results page to load
    time.sleep(1)

    # Get the URL of the search results page
    parsed = urlparse(browser.current_url)
    try:
        ticker = parse_qs(parsed.query)['p'][0]
        print("Ticker:", ticker)
        return ticker
    except KeyError:
        print("No 'p' parameter in the query string.")
        return None
    # Close the browser when done
    #browser.quit()

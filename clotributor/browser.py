from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

def get_browser(headless=True):
    """
    Initializes and returns a Selenium Chrome WebDriver instance.

    Parameters:
        headless (bool): Whether to run Chrome in headless mode.

    Returns:
        webdriver.Chrome: Configured Selenium Chrome driver.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_path = "./drivers/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
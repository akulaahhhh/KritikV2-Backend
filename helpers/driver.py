from os.path import dirname, abspath, join

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.ie.webdriver import WebDriver
from os.path import join, dirname, abspath
from selenium.webdriver.chrome.service import Service

service = Service(join(dirname(dirname(abspath(__file__))), r"chromedriver-win64\chromedriver.exe"))

def chrome_driver() -> WebDriver:
    # chromedriver-win64\chromedriver.exe
    service = Service(join(dirname(dirname(abspath(__file__))) ,"chromedriver-win64\chromedriver.exe"))
    driver = webdriver.Chrome(service=service)

    return driver
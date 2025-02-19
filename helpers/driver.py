import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

def install_chrome():
    """Install Google Chrome if not available"""
    if not os.path.exists("/usr/bin/google-chrome"):
        os.system("apt update && apt install -y google-chrome-stable")

def chrome_driver():
    install_chrome()  # Install Chrome if not already installed
    chromedriver_autoinstaller.install()  # Install correct ChromeDriver version

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Needed for running in Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes

    service = Service()  # Auto-detect ChromeDriver
    driver = uc.Chrome(service=service, options=chrome_options)  # Use undetected ChromeDriver

    return driver

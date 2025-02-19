from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def chrome_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"  # Path for Nix-installed Chromium
    chrome_options.add_argument("--headless")  # Run without UI

    service = Service("/usr/bin/chromedriver")  # Adjust path if needed
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

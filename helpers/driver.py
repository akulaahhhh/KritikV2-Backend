import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def chrome_driver():
    # Automatically download and install the appropriate ChromeDriver
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure headless mode for server environments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()  # Let Selenium automatically locate ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

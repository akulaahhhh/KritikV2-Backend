from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def chrome_driver():
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # Path to Chrome binary
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")  # Required for running as root
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoids memory issues

        # Set the path to ChromeDriver
        service = Service("/usr/local/bin/chromedriver")  # Path to ChromeDriver

        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        raise  # Re-raise the exception to stop execution
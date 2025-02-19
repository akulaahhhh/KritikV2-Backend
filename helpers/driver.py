from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Use Browserless WebDriver Endpoint
browserless_url = "https://browserless-production-6684.up.railway.app/webdriver?token=0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp"

def chrome_driver():
    driver = webdriver.Remote(
        command_executor=browserless_url,  # Connect to Browserless
        options=chrome_options
    )
    return driver

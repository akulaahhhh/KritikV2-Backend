from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Use Browserless WebDriver Endpoint with token in URL (Replace with your actual token)
browserless_url = "https://0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp@browserless-production-6684.up.railway.app/webdriver"

def chrome_driver():
    driver = webdriver.Remote(
        command_executor=browserless_url,  # Token is included in the URL
        options=chrome_options
    )
    return driver

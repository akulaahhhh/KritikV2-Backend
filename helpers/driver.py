from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome without UI

# Use Browserless WebDriver Endpoint (replace YOUR_TOKEN)
browserless_url = "https://browserless-production-6684.up.railway.app/webdriver?token=0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp"

def chrome_driver():
    driver = webdriver.Remote(
        command_executor=browserless_url,
        options=chrome_options
    )
    return driver

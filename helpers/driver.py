from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Use latest headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes from memory issues
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-features=Translate,NetworkServiceInProcess,BackgroundFetch")
chrome_options.add_argument("--remote-debugging-port=9222")

# Set Browserless token
chrome_options.set_capability("browserless:token", "0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp")

browserless_url = "https://browserless-production-6684.up.railway.app/webdriver"

def chrome_driver():
    driver = webdriver.Remote(
        command_executor=browserless_url,
        options=chrome_options
    )
    return driver

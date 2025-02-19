from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set the token in capabilities
caps = DesiredCapabilities.CHROME.copy()
caps["browserless:token"] = "0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp"

browserless_url = "https://browserless-production-6684.up.railway.app/webdriver"

def chrome_driver():
    driver = webdriver.Remote(
        command_executor=browserless_url,  # No token in URL
        desired_capabilities=caps,
        options=chrome_options
    )
    return driver

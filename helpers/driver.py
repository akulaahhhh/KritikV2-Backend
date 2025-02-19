from selenium import webdriver

def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up remote WebDriver using Browserless
    browserless_url = "wss://browserless-production-6684.up.railway.app?token=0kWaAdmvtQm0zbBL0PHLFIHnKYRJPlJDe07rKOMjprevNqFp"  # Replace with actual URL
    driver = webdriver.Remote(command_executor=browserless_url, options=options)

    return driver

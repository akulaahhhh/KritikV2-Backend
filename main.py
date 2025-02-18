import os
import time
import asyncio
from fastapi import FastAPI, WebSocket
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from helpers.driver import chrome_driver
from providers.nst import NST
from providers.thestar import TheStar
from providers.malaymail import MalayMail
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # Receive data from the frontend (e.g., URL, username, password)
        data = await websocket.receive_json()
        url = data["url"]
        kritik_user = data["username"]
        kritik_pass = data["password"]

        # Send initial processing message
        await websocket.send_text("Processing started...")

        # Identify provider based on URL
        provider = None
        if url.startswith('https://www.nst.com.my/'):
            provider = NST(url)
        elif url.startswith('https://www.thestar.com.my/'):
            provider = TheStar(url)
        elif url.startswith('https://www.malaymail.com/'):
            provider = MalayMail(url)
        else:
            await websocket.send_text("Invalid URL")
            return

        # Send scraping message
        await websocket.send_text("Scraping content...")
        scraped_data = provider.get_data()

        # Set up WebDriver for WordPress login
        driver = chrome_driver()

        # Send login message and log into WordPress
        await websocket.send_text("Logging into WordPress...")
        login(driver, kritik_user, kritik_pass)

        # Insert scraped data into WordPress
        await websocket.send_text("Inserting data into WordPress...")
        insert_data(driver, scraped_data)

        # Send completion message
        await websocket.send_text("Process completed!")
        # driver.quit()
        # Keep the browser window open
        while True:
            try:
                data = await websocket.receive_json()
                url = data["url"]
                kritik_user = data["username"]
                kritik_pass = data["password"]

                await websocket.send_text("Processing started...")

                provider = None
                if url.startswith('https://www.nst.com.my/'):
                    provider = NST(url)
                elif url.startswith('https://www.thestar.com.my/'):
                    provider = TheStar(url)
                elif url.startswith('https://www.malaymail.com/'):
                    provider = MalayMail(url)
                else:
                    await websocket.send_text("Invalid URL")
                    continue  # ✅ Loop back for next request

                await websocket.send_text("Scraping content...")
                scraped_data = provider.get_data()

                driver = chrome_driver()
                await websocket.send_text("Logging into WordPress...")
                login(driver, kritik_user, kritik_pass)

                await websocket.send_text("Inserting data into WordPress...")
                insert_data(driver, scraped_data)

                await websocket.send_text("Process completed!")
                driver.quit()

            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
                print(f"Error: {str(e)}")

    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
        print(f"Error: {str(e)}")


def login(driver, username, password):
    login_url = 'https://kritik.com.my/wp-login.php?redirect_to=https%3A%2F%2Fkritik.com.my%2Fwp-admin%2Fpost-new.php&reauth=1'
    driver.get(login_url)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '#user_login').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '#user_pass').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#wp-submit').click()


def insert_data(driver, data):
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#title').send_keys(data.title)
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '#excerpt').send_keys(data.excerpt)
    time.sleep(0.5)

    driver.execute_script("document.querySelector('#content-html').click()")
    time.sleep(0.5)

    driver.find_element(By.CSS_SELECTOR, '#content').send_keys(data.content)
    time.sleep(0.5)

    driver.find_element(By.CSS_SELECTOR, '#content-tmce').click()

    set_image_btn = driver.find_element(By.CSS_SELECTOR, '#set-post-thumbnail')

    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe#content_ifr'))
    content_body = driver.find_element(By.CSS_SELECTOR, '#tinymce.mce-content-body')

    driver.execute_script("""
    var range = document.createRange();
    range.selectNodeContents(arguments[0]);
    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    """, content_body)

    driver.switch_to.default_content()

    driver.find_element(By.CSS_SELECTOR,'.mce-widget.mce-btn.mce-splitbtn.mce-colorbutton > :nth-child(2)').click()

    driver.find_element(By.CSS_SELECTOR, '[data-mce-color="#000000"]').click()

    time.sleep(1)

    if data.tags is not None:
        tags_input = driver.find_element(By.CSS_SELECTOR, 'input#new-tag-post_tag')
        add_tags_btn = driver.find_element(By.CSS_SELECTOR, 'input.button.tagadd')

        tags_input.send_keys(data.get_tags())
        driver.execute_script("arguments[0].click()", add_tags_btn)
    else:
        print("No tags found, skipping")

    driver.execute_script("arguments[0].click()", set_image_btn)
    time.sleep(1)

    set_featured_image_btn = driver.find_element(By.CSS_SELECTOR,
                                                 'button.media-button-select.media-button.button-primary.button-large')
    image_input = driver.find_element(By.CSS_SELECTOR, ' .moxie-shim.moxie-shim-html5 input[type="file"]')

    image_input.send_keys(data.image)

    WebDriverWait(driver, 60).until(
        lambda d: d.find_element(By.CSS_SELECTOR,
                                 'button.media-button-select.media-button.button-primary.button-large').get_attribute(
            'disabled') is None
    )

    set_featured_image_btn.click()


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

if __name__ == '__main__':
    main()

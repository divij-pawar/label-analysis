import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import asyncio
from playwright.async_api import async_playwright

# itemid = "LKI7W4WLQZ"  # swiggy item ID
# itemid = "Z0Z8P7ZIFM"  # swiggy item ID
itemid_list = ["Z0Z8P7ZIFM","LKI7W4WLQZ","OF7D7T9YPI","EQZI0JZPXT","GQYTBJLIEI","68GN0WY21V","JL2MYS5H4R" ]

def download_images(itemid_list):
    with sync_playwright() as p:
        # Set up Playwright with headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for itemid in itemid_list:
            url = f'https://www.swiggy.com/instamart/item/{itemid}'
            folder = 'swiggy_play/' + itemid

            page.goto(url)
            clickable_elements = page.query_selector_all('[data-testid="image-card-div"]')
            for element in clickable_elements:
                try:
                    element.click()
                    page.wait_for_timeout(1000)  # Wait for images to load, adjust as necessary
                except Exception as e:
                    print(f'Error clicking element: {e}')

            # Get page content after JavaScript is executed
            html = page.content()
            page.close()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            div_tags = soup.find_all('div', {'class': 'kvfysmfp _3PM9L'})

            # Create the folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            # Download each image
            for div in div_tags:
                img_tags = div.find_all('img')
                for img in img_tags:
                    img_url = img.get('src')
                    if img_url:
                        # Ensure the URL is absolute
                        img_url = urljoin(url, img_url)
                        # Get the image response
                        img_response = requests.get(img_url)

                        # Get the image name and save it
                        img_name = os.path.join(folder, os.path.basename(img_url))
                        img_name += ".jpg"
                        with open(img_name, 'wb') as f:
                            f.write(img_response.content)
                        print(f'Downloaded {img_name}')
        browser.close()

download_images(itemid_list)